from __future__ import annotations
from typing import List, Any
from ..db_class.base_sql import BaseSql
from ..db_class.sql_ctx import SqlCtx
from ...data_class import Inventory
from ...cfg import AppConfig


_FIELDS_STR = """
inventory.as_rst,
inventory.data_line_fmt,
inventory.dispname,
inventory.dispname_abbrev,
inventory.dispname_contracted,
inventory.dispname_expanded,
inventory.domain,
inventory.name,
inventory.priority,
inventory.role,
inventory.rst_fmt,
inventory.uri,
inventory.uri_abbrev,
inventory.uri_contracted,
inventory.uri_expanded,
inventory.prefix_index
"""


class QryInv(BaseSql):
    def __init__(self, connect_str: str) -> None:
        super().__init__(connect_str=connect_str)

    def get_inventory(self, key: str) -> Inventory | None:
        """
        Gets Inventory instance for a given as_rst value

        Args:
            full_ns (str): full namespace used for match.

        Returns:
            Union[Component, None]: Component instance if ``full_ns`` is a match; Otherwise, ``None``
        """
        qry_str = f"""SELECT {_FIELDS_STR} from inventory WHERE inventory.as_rst like  :key Limit 1;"""

        args = {"key": key}
        result = None
        with SqlCtx(self.conn_str) as db:
            db.cursor.execute(qry_str, args)
            for row in db.cursor:
                result = self._populate_inventory(row)

        return result

    def qry_by_name(
        self,
        search_name: str | List[str],
        *,
        exclude: str | List[str] = "",
        domain: str = "",
        role: str = "",
        limit: int = 10,
        case_sensitive: bool = False,
        help_index: int = -1,
        escape: str = "",
    ) -> List[Inventory]:
        if not search_name:
            return []
        args = {}
        qry_str = f"SELECT {_FIELDS_STR}\nfrom inventory WHERE inventory.name LIKE :search_name0"

        if isinstance(search_name, list):
            for i, name in enumerate(search_name):
                args[f"search_name{i}"] = name.strip()
                if i > 0:
                    qry_str += f" OR inventory.name LIKE :search_name{i}"
        else:
            args["search_name0"] = search_name.strip()
        result: List[Inventory] = []

        if isinstance(exclude, str):
            excludes = [exclude] if exclude else []
        else:
            excludes = exclude

        if domain:
            qry_str += f" AND inventory.domain LIKE :domain"
            args["domain"] = domain
        if role:
            qry_str += f" AND inventory.role LIKE :role"
            args["role"] = role
        if help_index >= 0:
            qry_str += f" AND inventory.prefix_index = :help_index"
            args["help_index"] = help_index
        if excludes:
            nots = [f"'{itm}'" for itm in excludes]
            nots.insert(0, "")
            qry_str += " AND inventory.name NOT LIKE ".join(nots)
        if AppConfig.db_not_name:
            nots = [f"'{itm}'" for itm in AppConfig.db_not_name]
            nots.insert(0, "")
            qry_str += " AND inventory.name NOT LIKE ".join(nots)
        if AppConfig.db_not_domain:
            nots = [f"'{itm}'" for itm in AppConfig.db_not_domain]
            nots.insert(0, "")
            qry_str += " AND inventory.domain NOT LIKE ".join(nots)
        if AppConfig.db_not_role:
            nots = [f"'{itm}'" for itm in AppConfig.db_not_role]
            nots.insert(0, "")
            qry_str += " AND inventory.role NOT LIKE ".join(nots)
        if escape:
            qry_str += f" ESCAPE '{escape[0]}'"
        if limit > 0:
            qry_str += f" LIMIT {limit};"
        # print()
        # print(qry_str)
        # print()
        with SqlCtx(self.conn_str) as db:
            if case_sensitive:
                db.connection.execute(f"PRAGMA case_sensitive_like = {'ON' if case_sensitive else 'OFF'};")
            db.cursor.execute(qry_str, args)
            for row in db.cursor:
                result.append(self._populate_inventory(row))
        return result

    def qry_domains(self) -> List[str]:
        """Gets list of unique domains from the database"""
        qry_str = "SELECT DISTINCT inventory.domain from inventory;"
        result: List[str] = []
        with SqlCtx(self.conn_str) as db:
            db.cursor.execute(qry_str)
            for row in db.cursor:
                result.append(row["domain"])
        return result

    def qry_roles(self) -> List[str]:
        """Gets list of unique roles from the database"""
        qry_str = "SELECT DISTINCT inventory.role from inventory;"
        result: List[str] = []
        with SqlCtx(self.conn_str) as db:
            db.cursor.execute(qry_str)
            for row in db.cursor:
                result.append(row["role"])
        return result

    def _populate_inventory(self, row: Any) -> Inventory:
        """Populates inventory table"""
        return Inventory(
            as_rst=row["as_rst"],
            data_line_fmt=row["data_line_fmt"],
            dispname=row["dispname"],
            dispname_abbrev=row["dispname_abbrev"],
            dispname_contracted=row["dispname_contracted"],
            dispname_expanded=row["dispname_expanded"],
            domain=row["domain"],
            name=row["name"],
            priority=row["priority"],
            role=row["role"],
            rst_fmt=row["rst_fmt"],
            uri=row["uri"],
            uri_abbrev=row["uri_abbrev"],
            uri_contracted=row["uri_contracted"],
            uri_expanded=row["uri_expanded"],
            prefix_index=row["prefix_index"],
        )

    def get_row_count(self) -> int:
        raise NotImplementedError

    def remove_all(self) -> None:
        raise NotImplementedError

    def has_data(self) -> bool:
        raise NotImplementedError
