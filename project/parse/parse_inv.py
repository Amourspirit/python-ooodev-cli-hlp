from __future__ import annotations
from typing import List
from sphobjinv.inventory import Inventory as Inv
from sphinx_cli_help.data_class import Inventory
from sphinx_cli_help.data_class import SphinxInfo
from sphinx_cli_help.data_manage.db_class.db_connect import DbConnect
from sphinx_cli_help.data_manage.db_class.tbl_inventory import TblInventory
from sphinx_cli_help.data_manage.db_class.tbl_sphinx_info import TblSphinxInfo


class ParseInv:
    """Parses inv file and writes to database"""

    def __init__(self, fnm: str, prefix_index: int) -> None:
        """
        Constructor

        Args:
            fnm (str): Path to inv file
            prefix_index (int): Indx of prefix_index field.
        """
        self._fnm = fnm
        self._inv_lst: List[Inventory] = []
        self._conn = DbConnect()
        self._prefix_index = prefix_index
        self._sphinx_info = None

    def _read_inv(self) -> None:
        inv = Inv(fname_zlib=str(self._fnm))  # type: ignore
        self._sphinx_info = SphinxInfo(-1, project=inv.project, version=inv.version, idx=self._prefix_index)
        for itm in inv.objects:
            inv_itm = Inventory(
                as_rst=itm.as_rst,
                data_line_fmt=itm.data_line_fmt,
                dispname=itm.dispname,
                dispname_abbrev=itm.dispname_abbrev,
                dispname_contracted=itm.dispname_contracted,
                dispname_expanded=itm.dispname_expanded,
                domain=itm.domain,
                name=itm.name,
                role=itm.role,
                priority=itm.priority,
                rst_fmt=itm.rst_fmt,
                uri=itm.uri,
                uri_abbrev=itm.uri_abbrev,
                uri_contracted=itm.uri_contracted,
                uri_expanded=itm.uri_expanded,
                prefix_index=self._prefix_index,
            )
            self._inv_lst.append(inv_itm)

    def _write_all(self) -> None:
        self._inv_lst.clear()
        self._read_inv()
        tbl_inv = TblInventory(connect_str=self._conn.connection_str)
        tbl_inv.insert(data=self._inv_lst)
        if self._sphinx_info:
            tbl_sphinx_info = TblSphinxInfo(connect_str=self._conn.connection_str)
            tbl_sphinx_info.insert(data=self._sphinx_info)

    def update(self) -> None:
        """
        Writes all data to database.
        """
        self._write_all()
