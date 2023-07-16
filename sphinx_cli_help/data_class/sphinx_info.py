from dataclasses import dataclass


@dataclass
class SphinxInfo:
    id: int
    project: str
    version: str
    idx: int
