from __future__ import annotations
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, cast
from ..web_search import __mod_path__
from ..data_class import Inventory
from ..cfg import AppConfig
from ..data_manage.qry.qry_inv import QryInv
from ..data_manage.db_class.db_connect import DbConnect

# region Internal Func


def _browse(url: str) -> None:
    # opening in subprocess prevents extra output to termnial.
    cmd = [sys.executable, str(Path(__mod_path__, "browse.py")), url]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# endregion Internal Func

# region Terminal Questions


def query_hlp_choice(items: List[Inventory]) -> int | None:
    """
    Ask for a choice of which inventory to open url for.

    Arguments:
        items (List[Inventory]): List of Inventory to choose from.

    Returns:
        (int, None): Integer representing the zero base index within comps or None if canceled.
    """
    # https://tinyurl.com/yyg38fp2
    # https://tinyurl.com/y2pv2cdh
    c_len = len(items)
    # valid is 1 to length of comps + 1 for None
    valid = tuple([i for i in range(1, c_len + 1)])
    question = "Choose an option (default 1):"
    prompt = f'\n{"[0],":<5} Cancel (or press q followed by enter)'
    for i, comp in enumerate(items, 1):
        prompt = prompt + f"\n{f'[{i}],':<5} {comp.name:<64} - {comp.role:<10} - {comp.domain}"
        i += 1
    prompt += "\n"
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice == "":
            return 0
        if choice == "q":
            return None
        if choice.isdigit():
            j = int(choice)
        else:
            j = -1
        if j == 0:
            return None
        if j in valid:
            return j - 1
        else:
            sys.stdout.write(f"Please respond with input from 0 - {c_len}\n")


# endregion Terminal Questions

# region Parser


# region Parser Args
def _args_comp(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-s",
        "--search",
        help="Search phrase. Multiple -s are permitted.",
        action="append",
        dest="search",
        required=True,
    )
    parser.add_argument(
        "-b", "--no-before", help="No leading wildcard in search", action="store_false", dest="leading", default=True
    )
    parser.add_argument(
        "-a", "--no-after", help="No trailing wildcard in search", action="store_false", dest="trailing", default=True
    )
    parser.add_argument(
        "-c",
        "--case-sensitive",
        help="Case sensitive search",
        action="store_true",
        dest="case_sensitive",
        default=False,
    )
    parser.add_argument(
        "-m",
        "--max-results",
        help="Limits the number of results returned: Default (default: %(default)s)",
        action="store",
        dest="limit",
        type=int,
        default=AppConfig.max_results_default,
    )
    parser.add_argument(
        "-x",
        "--exclude",
        help="Optional: excludes from match. Multiple -x are permitted.",
        action="append",
        dest="exclude",
        required=False,
    )
    if len(AppConfig.domains) > 1:
        parser.add_argument(
            "-d",
            "--domain",
            default="any",
            const="any",
            nargs="?",
            dest="domain",
            choices=AppConfig.domains,
            help="Select type of domain",
        )
    if len(AppConfig.roles) > 1:
        parser.add_argument(
            "-r",
            "--role",
            default="any",
            const="any",
            nargs="?",
            dest="role",
            choices=AppConfig.roles,
            help="Select type of role",
        )
    idx_prefix = [str(prefix.index) for prefix in AppConfig.url_prefix if prefix.name != ""]
    if len(idx_prefix) > 1:
        idx_prefix_help = ", ".join(
            [f'{prefix.index} for "{prefix.name}"' for prefix in AppConfig.url_prefix if prefix.name != ""]
        )
        parser.add_argument(
            "-i",
            "--help-index",
            default="any",
            const="any",
            nargs="?",
            dest="help_index",
            choices=idx_prefix,
            help=f"Optional: Limit search to a specific Help set. {idx_prefix_help}",
        )
    parser.add_argument(
        "-e",
        "--escape",
        help="Escape Character. Used to escape %% and _ characters in search. The value normally used when needed is \\",
        action="store",
        dest="escape",
        default="",
        required=False,
    )


# endregion Parser Args

# region Parser Command Process


def _args_process_cmd(args: argparse.Namespace) -> int:
    if args.command == "hlp":
        return _args_hlp_action(args)
    return 0


# endregion Parser Command Process


# region Parser Actions


def _args_hlp_action(args: argparse.Namespace) -> int:
    searches = cast(List[str], args.search[:])
    if args.leading:
        searches = [f"%{search}" for search in searches]
    if args.trailing:
        searches = [f"{search}%" for search in searches]
    if hasattr(args, "role") and args.role != "any":
        role = args.role
    else:
        role = ""
    if hasattr(args, "domain") and args.domain != "any":
        domain = args.domain
    else:
        domain = ""
    if hasattr(args, "help_index") and args.help_index != "any":
        help_index = int(args.help_index)
    else:
        help_index = -1

    conn = DbConnect()
    results = QryInv(conn.connection_str).qry_by_name(
        searches,
        domain=domain,
        role=role,
        limit=args.limit,
        case_sensitive=args.case_sensitive,
        help_index=help_index,
        exclude=args.exclude,
    )
    if len(results) == 0:
        print("Search produced no results")
        return 0
    choice = query_hlp_choice(results)
    if choice is not None:
        url = AppConfig.url_prefix[results[choice].prefix_index].url + results[choice].uri_expanded
        if AppConfig.print_url:
            print(url)
        if AppConfig.open_in_browser:
            _browse(url)
    return 0


# endregion Parser Actions

# endregion Parser


def main() -> int:
    parser = argparse.ArgumentParser(description="main")
    subparser = parser.add_subparsers(dest="command")
    cmd_comp = subparser.add_parser(name="hlp", help="Search by name")

    _args_comp(cmd_comp)

    if len(sys.argv) <= 1:
        parser.print_help()
        return 0

    args = parser.parse_args()
    print(args)
    print()
    _args_process_cmd(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
