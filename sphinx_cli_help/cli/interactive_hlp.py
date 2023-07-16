"""
This file can be used in an interactive python session.
It behaves similar to the cli-hlp command line tool.

Usage:

``from sphinx_cli_help.cli.interactive_hlp import interactive_hlp as hlp``

``hlp("-s <search string> -d <domain> -r <role> -i <help index>")``

"""
import os, sys
from pathlib import Path
import platform


def interactive_hlp(s="", cmd="hlp"):
    """
    Generate a help url for a given search string and open it in a browser.

    For usage in an interactive python session.

    Args:
        s (str, optional): Search Parameters. See cli-hlp hlp --help for details..
        cmd (str, optional): cli-hlp command. Defaults to "hlp".
    """
    venv = os.environ.get("VIRTUAL_ENV", "")
    if not venv:
        ex_path = Path(sys.executable)
        venv = str(ex_path.parent.parent)
    if platform.system() == "Windows":
        os.system(f"{sys.executable} {venv}\\Scripts\\cli-hlp.exe {cmd} {s}")
    else:
        os.system(f"{sys.executable} {venv}/bin/cli-hlp {cmd} {s}")
