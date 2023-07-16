from pathlib import Path
from .config import read_config_default


AppConfig = read_config_default()
AppConfig.root_path = Path(__file__).parent.parent

__all__ = ["AppConfig"]
