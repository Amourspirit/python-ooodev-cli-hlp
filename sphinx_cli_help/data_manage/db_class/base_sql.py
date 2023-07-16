from __future__ import annotations
from abc import abstractmethod, ABC


class BaseSql(ABC):
    def __init__(self, connect_str: str) -> None:
        self._conn_str = connect_str

    @property
    def conn_str(self) -> str:
        """Gets connect_str value"""
        return self._conn_str

    @abstractmethod
    def get_row_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def remove_all(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def has_data(self) -> bool:
        raise NotImplementedError
