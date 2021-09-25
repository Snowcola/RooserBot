from argparse import ArgumentParser
import pprint

from utils.add_commands import (
    commands,
    stop,
    pause,
    register_all,
    register_at_all_guilds,
    register_at_guild,
    register_one,
    get_global_commands,
)

pp = pprint.PrettyPrinter(indent=2)


parser = ArgumentParser()
subparsers = parser.add_subparsers(help="commands", dest="commands")
register_commands_parser = subparsers.add_parser("reg")
get_commands_parser = subparsers.add_parser("get-commands")
group_reg_types = register_commands_parser.add_mutually_exclusive_group()
group_reg_types.add_argument(
    "-a",
    "--all",
    dest="all",
    action="store_true",
    help="Registers all commands",
    required=False,
)
group_reg_types.add_argument(
    "-g",
    "--global",
    dest="reg_global",
    action="store_true",
    help="Registers only global commands",
    required=False,
)
group_get_types = get_commands_parser.add_mutually_exclusive_group()
group_get_types.add_argument("-g", "--global", dest="get_global", action="store_true", required=False)
args = parser.parse_args()


def create_all_global():
    """registers all global commands with the discord API"""
    pass


def create_all_guild():
    """registers all guild commands with the discord API"""
    pass


def create_all():
    """registers all commands for guilds and global with the discrod API"""
    pass


def main(args):
    if args.commands == "get-commands" and args.get_global:
        globals = get_global_commands()
        pp.pprint(globals)
        pp.pprint([item["name"] for item in globals])
    pass


if __name__ == "__main__":
    main(args)
    print(register_one(stop, update=True, id=891170499932094464))
    # print(register_one(pause, update=True, id=891170500817084436))
