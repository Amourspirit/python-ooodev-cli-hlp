from __future__ import annotations
import sys
import argparse
from sphinx_cli_help.cfg import AppConfig
from sphinx_cli_help.data_manage.controller.database_controller import DatabaseController
from sphinx_cli_help.data_manage.qry.qry_inv import QryInv
from sphinx_cli_help.data_manage.db_class.db_connect import DbConnect
from project.controllers.controller_inv import ControllerInv
from project.dl.download import download_file
from project.builder import build_pkg


# region    Question Yes No
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    # https://tinyurl.com/yyg38fp2
    # https://tinyurl.com/y2pv2cdh
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


# endregion Question Yes No


# region Parser
# region    create parser
def _create_parser(name: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description=name)


# endregion create parser


# region    commands
def _args_process_cmd(args: argparse.Namespace) -> None:
    if args.command == "data":
        _args_process_data_cmd_data(args=args)
    elif args.command == "build":
        build_pkg.main()


# endregion commands


# region    data
def _args_process_data_cmd_data(args: argparse.Namespace) -> None:
    if args.command_data == "init":
        _args_action_db_init(args=args)
    elif args.command_data == "update":
        _args_action_db_update(args=args)
    elif args.command_data == "roles":
        _args_action_db_roles(args=args)
    elif args.command_data == "domains":
        _args_action_db_domains(args=args)
    elif args.command_data == "info":
        _args_action_db_info(args=args)


def _args_add_data_init(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-i", "--init-db", help="Initialize database", action="store_true", dest="init_db", default=False
    )


def _args_add_data_info(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-i", "--idx", help="Index of info to retreive", action="store", dest="idx", default=0, required=False
    )


def _args_action_db_init(args: argparse.Namespace) -> None:
    dbc = DatabaseController(init_db=args.init_db)
    if args.init_db:
        if not query_yes_no(
            f"Are you sure you want initialize the database '{AppConfig.db_name}'?\n  Args: {args}\n ", "no"
        ):
            return
    dbc.results()


def _args_action_db_info(args: argparse.Namespace) -> None:
    dbc = DatabaseController(get_info=True, idx=args.idx)
    print(dbc.results())


# endregion data

# region    Update


def _args_action_db_update(args: argparse.Namespace) -> None:
    if not query_yes_no(
        f"Are you sure you want to read inv file and write data in database?\n  Args: {args}\n ", "no"
    ):
        return
    if args.inv_url:
        fnm = str(download_file(url=args.inv_url))
    elif args.inv_file:
        fnm = args.inv_file
    else:
        fnm = ""
    inv_ctl = ControllerInv(fnm=fnm, write_all=True, prefix_index=args.prefix_index)
    inv_ctl.results()


def _args_action_db_roles(args: argparse.Namespace) -> None:
    conn = DbConnect()
    qry = QryInv(connect_str=conn.connection_str)
    roles = qry.qry_roles()
    q_roles = [f'"{role}"' for role in roles]
    print()
    print(",\n".join(q_roles))


def _args_action_db_domains(args: argparse.Namespace) -> None:
    conn = DbConnect()
    qry = QryInv(connect_str=conn.connection_str)
    domains = qry.qry_domains()
    q_domains = [f'"{domain}"' for domain in domains]
    print()
    print(",\n".join(q_domains))


def _args_data_update(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-u",
        "--url",
        help="Optional: URL to the objects.inv file",
        action="store",
        dest="inv_url",
        default=None,
    )
    group.add_argument(
        "-f",
        "--file",
        help="Optional: Path to the objects.inv file",
        action="store",
        dest="inv_file",
        default=None,
    )
    parser.add_argument(
        "-p",
        "--prefix-index",
        help="The Index of the prefix to use. Default is 0. This is the index of the url_prefix in the config.json file. (default: %(default)s)",
        action="store",
        dest="prefix_index",
        default=0,
        required=False,
    )


# endregion Update

# endregion Parser


def _main() -> int:
    # for debugging
    sys.argv.extend(["data", "update", "-f", "tmp/objects.inv"])
    return main()


def main() -> int:
    # region create parsers
    parser = _create_parser("main")
    subparser = parser.add_subparsers(dest="command")
    # endregion create parsers

    _ = subparser.add_parser(name="build", help="Build the package using Poetry in a custom environment.")
    data_subparser = subparser.add_parser(name="data", help="Various database commands and queries.")
    data = data_subparser.add_subparsers(dest="command_data")
    data_init = data.add_parser(
        name="init",
        help=f"Create a new database if it does not yet exits. Default location is '{AppConfig.resource_dir}/{AppConfig.db_name}'.",
    )
    data_update = data.add_parser(
        name="update",
        help=f"Read data from object.inv file into '{AppConfig.resource_dir}/{AppConfig.db_name}' database. Will add data if not existing.",
    )
    _ = data.add_parser(
        name="roles",
        help=f"Get the unique roles from database. These are the roles that should be added to the config.json file.",
    )
    _ = data.add_parser(
        name="domains",
        help=f"Get the unique roles from database. These are the roles that should be added to the config.json file.",
    )

    data_info = data.add_parser(
        name="info",
        help="Gets the info from the database.",
    )

    # region data args
    _args_add_data_init(parser=data_init)
    _args_data_update(parser=data_update)
    _args_add_data_info(parser=data_info)
    # endregion data args

    # region Read Args
    args = parser.parse_args()
    # endregion Read Args

    _args_process_cmd(args=args)
    return 0


if __name__ == "__main__":
    # _touch()
    SystemExit(main())
