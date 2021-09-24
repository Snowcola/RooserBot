from argparse import ArgumentParser

from utils.add_commands import (
    play,
    register_all,
    register_at_all_guilds,
    register_at_guild,
    register_one,
)


parser = ArgumentParser()
subparsers = parser.add_subparsers(help="commands", dest="commands")
register_commands_parser = subparsers.add_parser("reg")
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
    dest="global",
    action="store_true",
    help="Registers only global commands",
    required=False,
)
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
    # print(args)
    pass


if __name__ == "__main__":
    main(args)
    print(register_one(play))
