# coding: utf-8
from __future__ import annotations
from dataclasses import asdict
from typing import List
from .base_sql_table import BaseSqlTable
from .sql_ctx import SqlCtx
from ...data_class import SphinxInfo


class TblSphinxInfo(BaseSqlTable):
    def __init__(self, connect_str: str) -> None:
        super().__init__(connect_str=connect_str)

    def get_table_name(self) -> str:
        """Gets the current table name"""
        return "inventory"

    def insert(self, data: SphinxInfo) -> None:
        """
        Inserts/updates data. Handles inserting
        Args:
            data (LSphinxInfo): data to update
        """
        # Auto Increment https://www.sqlite.org/autoinc.html
        values = asdict(data)
        query = """INSERT INTO sphinx_info
        VALUES (
            null,
            :project,
            :version,
            :idx
        )
        """
        with SqlCtx(self.conn_str) as db:
            with db.connection:
                db.cursor.execute(query, values)

    def update(self, data: SphinxInfo) -> None:
        """
        Updates data. Handles updating

        Args:
            data (SphinxInfo): data to update
        """
        # self.remove_all()
        values = asdict(data)
        query = """UPDATE sphinx_info
        SET projcet = :project,
            version = :version,
            idx = :idx
        WHERE id = :id
        """
        with SqlCtx(self.conn_str) as db:
            with db.connection:
                db.cursor.execute(query, values)

    def get_info(self, id: int) -> SphinxInfo | None:
        """
        Gets SphinxInfo instance for a given id

        Args:
            id (int): Row id

        Returns:
            SphinxInfo | None: Info if found; Otherwise, None
        """
        qry_str = f"""SELECT * from sphinx_info WHERE id = :id Limit 1;"""
        with SqlCtx(self.conn_str) as db:
            db.cursor.execute(qry_str, {"id": id})
            for row in db.cursor:
                return SphinxInfo(**row)
        return None

    def get_info_by_idx(self, idx: int) -> SphinxInfo | None:
        """
        Gets SphinxInfo instance for a given idx

        Args:
            idx (int): Index value

        Returns:
            SphinxInfo | None: Info if found; Otherwise, None
        """
        qry_str = f"""SELECT * from sphinx_info WHERE idx = :idx Limit 1;"""
        with SqlCtx(self.conn_str) as db:
            db.cursor.execute(qry_str, {"idx": idx})
            for row in db.cursor:
                return SphinxInfo(**row)
        return None

    def _create_table_if_not_exist(self) -> None:
        """Create Table if it does not exist"""
        raise NotImplementedError
