from __future__ import annotations
from pathlib import Path
from ..parse.parse_inv import ParseInv


class ControllerInv:
    """Manages converting Inventory file to database."""

    def __init__(self, fnm: str = "", **kwargs) -> None:
        """
        Constructor

        Args:
            fnm (str, optional): File path to ``objects.inv``. Defaults to ``project/data/objects.inv``.
            prefix_index (int, optional): Index of prefix_index field. Defaults to 0.
            write_all (bool, optional): Write all data to database. Defaults to False.

        Raises:
            FileNotFoundError: _description_
        """
        self._write_all = bool(kwargs.get("write_all", False))
        if fnm == "":
            p_file = Path(__file__).parent.parent / "data" / "objects.inv"
        else:
            p_file = Path(fnm)
        if not p_file.is_absolute():
            p_file = p_file.resolve()
        if not p_file.exists():
            raise FileNotFoundError(f"File not found: {p_file}")
        self._prefix_index = int(kwargs.get("prefix_index", 0))
        self._parser = ParseInv(fnm=str(p_file), prefix_index=self._prefix_index)

    def results(self) -> None:
        """Takes action based on arguments."""
        if self._write_all:
            self._parser._write_all()
