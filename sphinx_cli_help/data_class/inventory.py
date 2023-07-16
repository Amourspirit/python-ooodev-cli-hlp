from dataclasses import dataclass


@dataclass
class Inventory:
    as_rst: str
    data_line_fmt: str
    dispname: str
    dispname_abbrev: str
    dispname_contracted: str
    dispname_expanded: str
    domain: str
    name: str
    role: str
    priority: int
    rst_fmt: str
    uri: str
    uri_abbrev: str
    uri_contracted: str
    uri_expanded: str
    prefix_index: int
