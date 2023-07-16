# coding: utf-8
from dataclasses import asdict
from typing import List
from .base_sql_table import BaseSqlTable
from .sql_ctx import SqlCtx
from ...data_class import Inventory


class TblInventory(BaseSqlTable):
    def __init__(self, connect_str: str) -> None:
        super().__init__(connect_str=connect_str)

    def get_table_name(self) -> str:
        """Gets the current table name"""
        return "inventory"

    def insert(self, data: List[Inventory]) -> None:
        """
        Inserts/updates data. Handles inserting and updating

        Args:
            data (List[Inventory]): data to update
        """
        if len(data) == 0:
            return
        # SQLite UPSERT / UPDATE OR INSERT
        # https://stackoverflow.com/questions/15277373/sqlite-upsert-update-or-insert
        values = [asdict(itm) for itm in data]
        query = """INSERT INTO inventory
        VALUES (
            :as_rst,
            :data_line_fmt,
            :dispname,
            :dispname_abbrev,
            :dispname_contracted,
            :dispname_expanded,
            :domain,
            :name, 
            :role,
            :priority,
            :rst_fmt,
            :uri,
            :uri_abbrev,
            :uri_contracted,
            :uri_expanded,
            :prefix_index
        )
        ON CONFLICT(as_rst) 
        DO UPDATE SET 
        data_line_fmt=excluded.data_line_fmt,
        dispname=excluded.dispname,
        dispname_abbrev=excluded.dispname_abbrev,
        dispname_contracted=excluded.dispname_contracted,
        dispname_expanded=excluded.dispname_expanded,
        domain=excluded.domain,
        name=excluded.name,
        role=excluded.role,
        priority=excluded.priority,
        rst_fmt=excluded.rst_fmt,
        uri=excluded.uri,
        uri_abbrev=excluded.uri_abbrev,
        uri_contracted=excluded.uri_contracted,
        uri_expanded=excluded.uri_expanded,
        prefix_index=excluded.prefix_index;
        """
        with SqlCtx(self.conn_str) as db:
            with db.connection:
                db.cursor.executemany(query, values)

    def update(self, data: List[Inventory]) -> None:
        """
        Updates data. Handles updating

        Args:
            data (List[Inventory]): data to update
        """
        # self.remove_all()
        self.insert(data)

    def _create_table_if_not_exist(self) -> None:
        """Create Table if it does not exist"""
        raise NotImplementedError
