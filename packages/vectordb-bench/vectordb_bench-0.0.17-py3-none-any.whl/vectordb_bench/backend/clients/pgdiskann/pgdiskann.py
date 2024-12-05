"""Wrapper around the pg_diskann vector database over VectorDB"""

import logging
import pprint
from contextlib import contextmanager
from typing import Any, Generator, Optional, Tuple

import numpy as np
import psycopg
from pgvector.psycopg import register_vector
from psycopg import Connection, Cursor, sql

from ..api import VectorDB
from .config import PgDiskANNConfigDict, PgDiskANNIndexConfig

log = logging.getLogger(__name__)


class PgDiskANN(VectorDB):
    """Use psycopg instructions"""

    conn: psycopg.Connection[Any] | None = None
    coursor: psycopg.Cursor[Any] | None = None

    _filtered_search: sql.Composed
    _unfiltered_search: sql.Composed

    def __init__(
        self,
        dim: int,
        db_config: PgDiskANNConfigDict,
        db_case_config: PgDiskANNIndexConfig,
        collection_name: str = "pg_diskann_collection",
        drop_old: bool = False,
        **kwargs,
    ):
        self.name = "PgDiskANN"
        self.db_config = db_config
        self.case_config = db_case_config
        self.table_name = collection_name
        self.dim = dim

        self._index_name = "pgdiskann_index"
        self._primary_field = "id"
        self._vector_field = "embedding"

        self.conn, self.cursor = self._create_connection(**self.db_config)        

        log.info(f"{self.name} config values: {self.db_config}\n{self.case_config}")
        if not any(
            (
                self.case_config.create_index_before_load,
                self.case_config.create_index_after_load,
            )
        ):
            err = f"{self.name} config must create an index using create_index_before_load or create_index_after_load"
            log.error(err)
            raise RuntimeError(
                f"{err}\n{pprint.pformat(self.db_config)}\n{pprint.pformat(self.case_config)}"
            )

        if drop_old:
            self._drop_index()
            self._drop_table()
            self._create_table(dim)
            if self.case_config.create_index_before_load:
                self._create_index()

        self.cursor.close()
        self.conn.close()
        self.cursor = None
        self.conn = None

    @staticmethod
    def _create_connection(**kwargs) -> Tuple[Connection, Cursor]:
        conn = psycopg.connect(**kwargs)
        conn.cursor().execute("CREATE EXTENSION IF NOT EXISTS pg_diskann CASCADE")
        conn.commit()
        register_vector(conn)
        conn.autocommit = False
        cursor = conn.cursor()

        assert conn is not None, "Connection is not initialized"
        assert cursor is not None, "Cursor is not initialized"

        return conn, cursor

    @contextmanager
    def init(self) -> Generator[None, None, None]:
        self.conn, self.cursor = self._create_connection(**self.db_config)

        # index configuration may have commands defined that we should set during each client session
        session_options: dict[str, Any] = self.case_config.session_param()

        if len(session_options) > 0:
            for setting_name, setting_val in session_options.items():
                command = sql.SQL("SET {setting_name} " + "= {setting_val};").format(
                    setting_name=sql.Identifier(setting_name),
                    setting_val=sql.Identifier(str(setting_val)),
                )
                log.debug(command.as_string(self.cursor))
                self.cursor.execute(command)
            self.conn.commit()
        
        self._filtered_search = sql.Composed(
            [
                sql.SQL(
                    "SELECT id FROM public.{table_name} WHERE id >= %s ORDER BY embedding "
                    ).format(table_name=sql.Identifier(self.table_name)),
                sql.SQL(self.case_config.search_param()["metric_fun_op"]),
                sql.SQL(" %s::vector LIMIT %s::int"),
            ]
        )

        self._unfiltered_search = sql.Composed(
            [
                sql.SQL("SELECT id FROM public.{} ORDER BY embedding ").format(
                    sql.Identifier(self.table_name)
                ),
                sql.SQL(self.case_config.search_param()["metric_fun_op"]),
                sql.SQL(" %s::vector LIMIT %s::int"),
            ]
        )

        try:
            yield
        finally:
            self.cursor.close()
            self.conn.close()
            self.cursor = None
            self.conn = None

    def _drop_table(self):
        assert self.conn is not None, "Connection is not initialized"
        assert self.cursor is not None, "Cursor is not initialized"
        log.info(f"{self.name} client drop table : {self.table_name}")

        self.cursor.execute(
            sql.SQL("DROP TABLE IF EXISTS public.{table_name}").format(
                table_name=sql.Identifier(self.table_name)
            )
        )
        self.conn.commit()

    def ready_to_load(self):
        pass

    def optimize(self):
        self._post_insert()

    def _post_insert(self):
        log.info(f"{self.name} post insert before optimize")
        if self.case_config.create_index_after_load:
            self._drop_index()
            self._create_index()

    def _drop_index(self):
        assert self.conn is not None, "Connection is not initialized"
        assert self.cursor is not None, "Cursor is not initialized"
        log.info(f"{self.name} client drop index : {self._index_name}")

        drop_index_sql = sql.SQL("DROP INDEX IF EXISTS {index_name}").format(
            index_name=sql.Identifier(self._index_name)
        )
        log.debug(drop_index_sql.as_string(self.cursor))
        self.cursor.execute(drop_index_sql)
        self.conn.commit()

    def _set_parallel_index_build_param(self):
        assert self.conn is not None, "Connection is not initialized"
        assert self.cursor is not None, "Cursor is not initialized"

        index_param = self.case_config.index_param()

        if index_param["maintenance_work_mem"] is not None:
            self.cursor.execute(
                sql.SQL("SET maintenance_work_mem TO {};").format(
                    index_param["maintenance_work_mem"]
                )
            )
            self.cursor.execute(
                sql.SQL("ALTER USER {} SET maintenance_work_mem TO {};").format(
                    sql.Identifier(self.db_config["user"]),
                    index_param["maintenance_work_mem"],
                )
            )
            self.conn.commit()

        if index_param["max_parallel_workers"] is not None:
            self.cursor.execute(
                sql.SQL("SET max_parallel_maintenance_workers TO '{}';").format(
                    index_param["max_parallel_workers"]
                )
            )
            self.cursor.execute(
                sql.SQL(
                    "ALTER USER {} SET max_parallel_maintenance_workers TO '{}';"
                ).format(
                    sql.Identifier(self.db_config["user"]),
                    index_param["max_parallel_workers"],
                )
            )
            self.cursor.execute(
                sql.SQL("SET max_parallel_workers TO '{}';").format(
                    index_param["max_parallel_workers"]
                )
            )
            self.cursor.execute(
                sql.SQL(
                    "ALTER USER {} SET max_parallel_workers TO '{}';"
                ).format(
                    sql.Identifier(self.db_config["user"]),
                    index_param["max_parallel_workers"],
                )
            )
            self.cursor.execute(
                sql.SQL(
                    "ALTER TABLE {} SET (parallel_workers = {});"
                ).format(
                    sql.Identifier(self.table_name),
                    index_param["max_parallel_workers"],
                )
            )
            self.conn.commit()

        results = self.cursor.execute(
            sql.SQL("SHOW max_parallel_maintenance_workers;")
        ).fetchall()
        results.extend(
            self.cursor.execute(sql.SQL("SHOW max_parallel_workers;")).fetchall()
        )
        results.extend(
            self.cursor.execute(sql.SQL("SHOW maintenance_work_mem;")).fetchall()
        )
        log.info(f"{self.name} parallel index creation parameters: {results}")
    def _create_index(self):
        assert self.conn is not None, "Connection is not initialized"
        assert self.cursor is not None, "Cursor is not initialized"
        log.info(f"{self.name} client create index : {self._index_name}")

        index_param: dict[str, Any] = self.case_config.index_param()
        self._set_parallel_index_build_param()

        options = []
        for option_name, option_val in index_param["options"].items():
            if option_val is not None:
                options.append(
                    sql.SQL("{option_name} = {val}").format(
                        option_name=sql.Identifier(option_name),
                        val=sql.Identifier(str(option_val)),
                    )
                )
        
        if any(options):
            with_clause = sql.SQL("WITH ({});").format(sql.SQL(", ").join(options))
        else:
            with_clause = sql.Composed(())

        index_create_sql = sql.SQL(
            """
            CREATE INDEX IF NOT EXISTS {index_name} ON public.{table_name} 
            USING {index_type} (embedding {embedding_metric})
            """
        ).format(
            index_name=sql.Identifier(self._index_name),
            table_name=sql.Identifier(self.table_name),
            index_type=sql.Identifier(index_param["index_type"].lower()),
            embedding_metric=sql.Identifier(index_param["metric"]),
        )
        index_create_sql_with_with_clause = (
            index_create_sql + with_clause
        ).join(" ")
        log.debug(index_create_sql_with_with_clause.as_string(self.cursor))
        self.cursor.execute(index_create_sql_with_with_clause)
        self.conn.commit()

    def _create_table(self, dim: int):
        assert self.conn is not None, "Connection is not initialized"
        assert self.cursor is not None, "Cursor is not initialized"

        try:
            log.info(f"{self.name} client create table : {self.table_name}")

            self.cursor.execute(
                sql.SQL(
                    "CREATE TABLE IF NOT EXISTS public.{table_name} (id BIGINT PRIMARY KEY, embedding vector({dim}));"
                ).format(table_name=sql.Identifier(self.table_name), dim=dim)
            )
            self.conn.commit()
        except Exception as e:
            log.warning(
                f"Failed to create pgdiskann table: {self.table_name} error: {e}"
            )
            raise e from None

    def insert_embeddings(
        self,
        embeddings: list[list[float]],
        metadata: list[int],
        **kwargs: Any,
    ) -> Tuple[int, Optional[Exception]]:
        assert self.conn is not None, "Connection is not initialized"
        assert self.cursor is not None, "Cursor is not initialized"

        try:
            metadata_arr = np.array(metadata)
            embeddings_arr = np.array(embeddings)

            with self.cursor.copy(
                sql.SQL("COPY public.{table_name} FROM STDIN (FORMAT BINARY)").format(
                    table_name=sql.Identifier(self.table_name)
                )
            ) as copy:
                copy.set_types(["bigint", "vector"])
                for i, row in enumerate(metadata_arr):
                    copy.write_row((row, embeddings_arr[i]))
            self.conn.commit()

            if kwargs.get("last_batch"):
                self._post_insert()

            return len(metadata), None
        except Exception as e:
            log.warning(
                f"Failed to insert data into table ({self.table_name}), error: {e}"
            )
            return 0, e

    def search_embedding(
        self,
        query: list[float],
        k: int = 100,
        filters: dict | None = None,
        timeout: int | None = None,
    ) -> list[int]:
        assert self.conn is not None, "Connection is not initialized"
        assert self.cursor is not None, "Cursor is not initialized"

        q = np.asarray(query)
        if filters:
            gt = filters.get("id")
            result = self.cursor.execute(
                    self._filtered_search, (gt, q, k), prepare=True, binary=True
                    )
        else:
            result = self.cursor.execute(
                    self._unfiltered_search, (q, k), prepare=True, binary=True
                    )

        return [int(i[0]) for i in result.fetchall()]
