#!/usr/bin/env python3

"""Stuff that doesn't go anywhere else
"""

import asyncio
import logging
import os
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import NoReturn


def logger() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("medit.misc")


def watchdog(
    afunc: Callable[..., Coroutine[object, object, object]]
) -> Callable[..., Coroutine[object, object, object]]:
    """Watch for async functions to throw an unhandled exception"""

    @wraps(afunc)
    async def run(*args: object, **kwargs: object) -> object:
        """Run wrapped function and handle exceptions"""
        try:
            return await afunc(*args, **kwargs)
        except asyncio.CancelledError:
            logger().info("Task cancelled: `%s`", afunc.__name__)
        except KeyboardInterrupt:
            logger().info("KeyboardInterrupt in `%s`", afunc.__name__)
        except Exception:  # pylint: disable=broad-except
            logger().exception("Exception in `%s`:", afunc.__name__)
            asyncio.get_event_loop().stop()
        return None

    return run


def setup_logging(level: str | int = logging.DEBUG) -> None:
    '''
    def thread_id_filter(record):
        """Inject thread_id to log records"""
        record.thread_id = threading.get_native_id()
        return record

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(thread_id)s | %(message)s")
    )
    handler.addFilter(thread_id_filter)
    logger().addHandler(handler)
    logging.getLogger().setLevel(level)
    '''
    use_col = "TERM" in os.environ
    col_terminator = "\033[0m" if use_col else ""
    logging.basicConfig(
        format=f"%(levelname)s %(asctime)s.%(msecs)03d %(name)-12s│ %(message)s{col_terminator}",
        datefmt="%H:%M:%S",
        level=getattr(logging, level) if isinstance(level, str) else level,
    )
    for name, color in (
        ("DEBUG", "\033[32m"),
        ("INFO", "\033[36m"),
        ("WARNING", "\033[33m"),
        ("ERROR", "\033[31m"),
        ("CRITICAL", "\033[37m"),
    ):
        logging.addLevelName(
            getattr(logging, name),
            f"{color if use_col else ''}({name[0] * 2})",
        )


def throw(exc: Exception) -> NoReturn:
    """Make raising an exception functional"""
    raise exc
