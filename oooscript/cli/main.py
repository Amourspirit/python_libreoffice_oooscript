#!/usr/bin/env python
# coding: utf-8
# region imports
import sys
import argparse

from oooscript.build.build import Builder as Builder1
from oooscript.build.build import BuilderArgs as BuilderArgs1
from oooscript.build.build2 import Builder2
from oooscript.build.build2 import BuilderArgs as BuilderArgs2
from oooscript import __version__

# endregion imports

# region Parser


# region    parser setup
def _create_parser(name: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description=name)


def _parse_args(parser: argparse.ArgumentParser):
    parser = _create_parser("main")
    subparser = parser.add_subparsers(dest="command")
    cmd_compile = subparser.add_parser(
        name="compile", help="Compile scripts for LibreOffice usage"
    )
    _ = subparser.add_parser(name="version", help="Version information")

    _args_cmd_compile(parser=cmd_compile)

    if len(sys.argv) <= 1:
        parser.print_help()
        return None
    return parser.parse_args()


def _args_cmd_compile(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-c", "--config", required=True, type=str, help="config.json file"
    )
    parser.add_argument(
        "-e",
        "--embed",
        action="store_true",
        default=False,
        help="Determines if script is embedded in a LibreOffice Document",
    )
    parser.add_argument(
        "-d",
        "--embed-doc",
        type=str,
        default=None,
        dest="embed_doc",
        help="Optional, LibreOffice document to embed script into.",
    )
    parser.add_argument(
        "-b",
        "--build-dir",
        default=None,
        dest="build_dir",
        help="Optional, build directory to place compiled script. Can be relative or absolute path. Will override the build directory set by environment and .env file.",
    )
    parser.add_argument(
        "-z",
        "--pyz-out",
        action="store_true",
        help="Package Library as binary file (recommended).",
    )


# endregion  parser setup


# region        process arg command
def _args_action_compile(
    a_parser: argparse.ArgumentParser, args: argparse.Namespace
) -> None:
    if args.pyz_out:
        builder_args = BuilderArgs2(
            config_json=args.config,
            embed_in_doc=args.embed,
            embed_doc=args.embed_doc,
            build_dir=args.build_dir,
            pyz_out=True,
        )
        builder = Builder2(builder_args)
        builder.build()
        return

    builder_args = BuilderArgs1(
        config_json=args.config,
        embed_in_doc=args.embed,
        embed_doc=args.embed_doc,
        build_dir=args.build_dir,
    )
    builder = Builder1(builder_args)
    builder.build()


def _args_action_version(
    a_parser: argparse.ArgumentParser, args: argparse.Namespace
) -> None:
    print(__version__)


def _args_process_cmd(
    a_parser: argparse.ArgumentParser, args: argparse.Namespace
) -> None:
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
