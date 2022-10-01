#!/usr/bin/env python
# coding: utf-8
# region imports
import sys
import argparse

from oooscript.build.build import Builder
from oooscript.build.build import BuilderArgs
from oooscript import __version__
# endregion imports

# region Parser

# region    parser setup
def _create_parser(name: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description=name)


def _parse_args(parser: argparse.ArgumentParser):
    parser = _create_parser("main")
    subparser = parser.add_subparsers(dest="command")
    cmd_compile = subparser.add_parser(name="compile", help="Compile scripts for LibreOffice usage")
    _ = subparser.add_parser(name="version", help="Version information")

    _args_cmd_compile(parser=cmd_compile)

    if len(sys.argv) <= 1:
        parser.print_help()
        return None
    return parser.parse_args()


def _args_cmd_compile(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-c", "--config", required=True, type=str, help="config.json file")
    parser.add_argument(
        "-e",
        "--embed",
        action="store_true",
        default=False,
        help="Determines if script is embedded in a LibreOffice Document",
    )
    parser.add_argument("-d", "--embed-doc", type=str, default=None, help="Opional, LibreOffice document to embed script into.")

# endregion  parser setup

# region        process arg command
def _args_action_compile(a_parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    args = BuilderArgs(config_json=args.config, embed_in_doc=args.embed, embed_doc=args.embed_doc)
    builder = Builder(args)
    builder.build()


def _args_action_version(a_parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    print(__version__)


def _args_process_cmd(a_parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if not hasattr(args, "command"):
        a_parser.print_help()
        return
    if args.command == "compile":
        _args_action_compile(a_parser=a_parser, args=args)
    elif args.command == "version":
        _args_action_version(a_parser=a_parser, args=args)
    else:
        a_parser.print_help()


# endregion     process arg command

# endregion Parser

# region Main
def main():
    parser = argparse.ArgumentParser()
    args = _parse_args(parser)
    _args_process_cmd(a_parser=parser, args=args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# endregion Main