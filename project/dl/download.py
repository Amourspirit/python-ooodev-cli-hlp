from __future__ import annotations
import requests
from pathlib import Path
from sphinx_cli_help.cfg import AppConfig


def download_file(url: str, dest: str = "") -> Path:
    """
    Download file from url and save to dest. If dest is not specified, save to tmp directory in project root.

    Args:
        url (str): url of file to download
        dest (str, optional): destination path to save file..

    Returns:
        Path: Path to downloaded file.
    """
    myfile = requests.get(url)
    root_path = AppConfig.root_path.parent

    if not dest:
        p_dest = root_path / "tmp" / url.split("/")[-1]
    else:
        p_dest = Path(dest)
    if not p_dest.is_absolute():
        p_dest = p_dest.resolve()

    p_dest.parent.mkdir(parents=True, exist_ok=True)
    with open(p_dest, "wb") as f:
        f.write(myfile.content)
    return p_dest
