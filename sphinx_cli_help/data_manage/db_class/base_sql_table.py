from __future__ import annotations
from abc import abstractmethod
from .base_sql import BaseSql
from .sql_ctx import SqlCtx


class BaseSqlTable(BaseSql):
    def __init__(self, connect_str: str) -> None:
        super().__init__(connect_str=connect_str)

    def get_row_count(self) -> int:
        if self.has_data is False:
            return 0
        query = "SELECT count() FROM " + self.get_table_name()
        with SqlCtx(self._conn_str) as db:
            db.cursor.execute(query)
            num_of_rows = db.cursor.fetchone()[0]
        return num_of_rows

    def remove_all(self) -> None:
        self._drop_table_if_exist()
        self._create_table_if_not_exist()

    def has_data(self) -> bool:
        query = f"SELECT * FROM {self.get_table_name()} limit 1"
        has_data = False
        with SqlCtx(self._conn_str) as db:
            db.cursor.execute(query)
            for _ in db.cursor:
                has_data = True
        return has_data

    @abstractmethod
    def _create_table_if_not_exist(self) -> None:
        """Create Table if it does not exist"""
        raise NotImplementedError

    def _drop_table_if_exist(self) -> None:
        query = f"DROP TABLE IF EXISTS {self.get_table_name()}"
        with SqlCtx(self._conn_str) as db:
            with db.connection:
                db.cursor.execute(query)

    @abstractmethod
    def get_table_name(self) -> str:
        """Table Name"""
        raise NotImplementedError
