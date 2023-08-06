#!/usr/bin/env python3

"""Markup Editor
"""

import importlib.metadata
import logging
import shutil
import sys
from argparse import ArgumentParser
from argparse import Namespace as Args
from collections.abc import Sequence
from contextlib import suppress
from pathlib import Path

from medit.misc import setup_logging
from medit.ui import main as ui_main


def parse_args(argv: Sequence[str] | None = None) -> Args:
    """Cool git like multi command argument parser"""
    parser = ArgumentParser(__doc__)
    parser.add_argument("--verbose", "-v", action="store_true")

    parser.set_defaults(func=fn_ui)
    subparsers = parser.add_subparsers(help="available commands", metavar="CMD")

    parser_help = subparsers.add_parser("help")
    parser_help.set_defaults(func=lambda *_: parser.print_help())

    parser_ui = subparsers.add_parser("ui")
    parser_ui.set_defaults(func=fn_ui)

    return parser.parse_args(argv)


def logger() -> logging.Logger:
    """Named logger"""
    return logging.getLogger("medit.cli")


def extract_version() -> str:
    """Returns either the version of installed package or the one
    found in nearby pyproject.toml"""
    with suppress(FileNotFoundError, StopIteration):
        with open(
            Path(__file__).parent.parent / "pyproject.toml", encoding="utf-8"
        ) as pyproject_toml:
            version = (
                next(line for line in pyproject_toml if line.startswith("version"))
                .split("=")[1]
                .strip("'\"\n ")
            )
            return f"{version}-dev"
    return importlib.metadata.version(__name__.split(".", maxsplit=1)[0])


__version__ = extract_version()


def shorten_home(path: Path | str) -> Path:
    """Reverse of expanduser"""
    return Path(Path(path).as_posix().replace(str(Path.home()), "~"))


def fn_info(_args: Args) -> None:
    """Entry point `info`"""
    print(f"Version: {__version__} (at {shorten_home(Path(__file__).parent)})")
    print(
        f"Python: {'.'.join(map(str, sys.version_info[:3]))}"
        f" (at {shorten_home(sys.executable)})"
    )


def fn_ui(_args: Args) -> None:
    ui_main()


def main() -> int:
    """Entry point for everything else"""
    (args := parse_args()).func(args)
    return 0


if __name__ == "__main__":
    main()
