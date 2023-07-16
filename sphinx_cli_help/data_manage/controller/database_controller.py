from __future__ import annotations
from typing import Any
from ...cfg import AppConfig
from ..db_class.init_db import InitDb
from ..db_class.db_connect import DbConnect
from ..db_class.tbl_sphinx_info import TblSphinxInfo


class DatabaseController:
    def __init__(self, **kwargs) -> None:
        self._init_db = bool(kwargs.pop("init_db", False))
        self._get_info = bool(kwargs.pop("get_info", False))
        self._kwargs = kwargs
        self._conn = DbConnect()

    def results(self) -> Any:
        if self._init_db:
            self._init_database()
            return None
        if self._get_info:
            tbl = TblSphinxInfo(connect_str=self._conn.connection_str)
            if "id" in self._kwargs:
                return tbl.get_info(id=int(self._kwargs["id"]))
            if "idx" in self._kwargs:
                return tbl.get_info_by_idx(idx=int(self._kwargs["idx"]))
        return None

    def _init_database(self) -> None:
        db = InitDb(self._conn.connection_str)
        db.init_db()
