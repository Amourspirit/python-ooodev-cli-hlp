# coding: utf-8
from .sql_ctx import SqlCtx
from ...cfg import AppConfig


class InitDb:
    def __init__(self, connect_str: str) -> None:
        self._conn_str = connect_str
        self._is_init = False

    def init_db(self) -> None:
        if self._is_init:
            return
        with SqlCtx(self._conn_str) as db:
            # if AppConfig.db_case_sensitive_like:
            #     # does not work here
            #     db.connection.execute("PRAGMA case_sensitive_like = ON;")
            self._create_table_inventory(db)
            self._create_table_info(db)
            self._create_table_sphinx_info(db)
            # db.cursor.execute("PRAGMA case_sensitive_like=ON;")
        self._insert_version()
        self._is_init = True

    def _create_table_inventory(self, db: SqlCtx) -> None:
        # bool : https://tinyurl.com/y9yocjx5
        query = """CREATE TABLE IF NOT EXISTS inventory (
            as_rst VARCHAR(255) PRIMARY KEY,
            data_line_fmt VARCHAR(255) NOT NULL,
            dispname VARCHAR(255) NOT NULL,
            dispname_abbrev VARCHAR(255) NOT NULL,
            dispname_contracted VARCHAR(255) NOT NULL,
            dispname_expanded VARCHAR(255) NOT NULL,
            domain VARCHAR(100) NOT NULL,
            name VARCHAR(255) NOT NULL,
            role VARCHAR(100) NOT NULL,
            priority INTEGER NOT NULL,
            rst_fmt VARCHAR(100) NOT NULL,
            uri VARCHAR(1024) NOT NULL,
            uri_abbrev VARCHAR(1024) NOT NULL,
            uri_contracted VARCHAR(1024) NOT NULL,
            uri_expanded VARCHAR(1024) NOT NULL,
            prefix_index INTEGER NOT NULL DEFAULT 0
            )"""
        # Create a secondary key on the name column
        createSecondaryIndex = "CREATE INDEX IF NOT EXISTS index_inventory_name ON inventory(name);"
        db.cursor.execute(query)
        db.cursor.execute(createSecondaryIndex)

    def _create_table_info(self, db: SqlCtx) -> None:
        query = """CREATE TABLE IF NOT EXISTS db_info (
            id INTEGER PRIMARY KEY,
            version VARCHAR(50)
            )"""
        db.cursor.execute(query)

    def _create_table_sphinx_info(self, db: SqlCtx) -> None:
        # Auto Increment https://www.sqlite.org/autoinc.html
        query = """CREATE TABLE IF NOT EXISTS sphinx_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project VARCHAR(100) NOT NULL,
            version VARCHAR(50) NOT NULL,
            idx INTEGER NOT NULL DEFAULT 0
            )"""
        db.cursor.execute(query)

    def _insert_version(self) -> None:
        with SqlCtx(self._conn_str) as db:
            if not self.has_data("db_info", db):
                query = f"INSERT INTO db_info (id, version) VALUES (?, ?);"
                db.cursor.execute(query, (0, AppConfig.db_version))

    def has_data(self, table: str, db: SqlCtx) -> bool:
        query = f"SELECT * FROM {table} limit 1"
        has_data = False
        db.cursor.execute(query)
        for _ in db.cursor:
            has_data = True
        return has_data
