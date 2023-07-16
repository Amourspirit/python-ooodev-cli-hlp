from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast, List, Dict


@dataclass
class UrlPrefix:
    index: int
    url: str
    name: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UrlPrefix":
        return cls(index=data["index"], url=data["url"], name=data.get("name", ""))


@dataclass
class Config:
    url_prefix: List[UrlPrefix]
    resource_dir: str
    open_in_browser: bool
    print_url: bool
    db_name: str
    roles: List[str]
    domains: List[str]
    max_results_default: int
    db_version: str  # version that database is set to during creation.
    db_not_name: List[str]
    db_not_domain: List[str]
    db_not_role: List[str]
    root_path: Path = cast(Path, None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        url_prefix = [UrlPrefix.from_dict(item) for item in data["url_prefix"]]
        roles = data["roles"]
        domains = data["domains"]
        db_not_name = data["db_not_name"]
        db_not_domain = data["db_not_domain"]
        db_not_role = data["db_not_role"]
        return cls(
            url_prefix=url_prefix,
            resource_dir=data["resource_dir"],
            open_in_browser=data["open_in_browser"],
            print_url=data["print_url"],
            db_name=data["db_name"],
            roles=roles,
            domains=domains,
            max_results_default=data["max_results_default"],
            db_version=data["db_version"],
            db_not_name=db_not_name,
            db_not_domain=db_not_domain,
            db_not_role=db_not_role,
        )


def read_config(config_file: str) -> Config:
    """
    Gets config for given config file

    Args:
        config_file (str): Config file to load

    Returns:
        AppConfig: Configuration object
    """
    with open(config_file, "r") as file:
        data = json.load(file)
        return Config.from_dict(data)


def read_config_default() -> Config:
    """
    Loads default configuration ``config.json``

    Returns:
        AppConfig: Configuration Object
    """
    root = Path(__file__).parent.parent
    config_file = Path(root, "config.json")
    return read_config(str(config_file))
