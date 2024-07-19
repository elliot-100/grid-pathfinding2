"""Pathfinding package."""

import logging
import time


def log_debug(
    logger: logging.Logger,
    message: str,
    start_time: float,
) -> None:
    """Add DEBUG log entry, with elapsed time since `start_time`."""
    _log(logger=logger, level=logging.DEBUG, message=message, start_time=start_time)


def log_info(
    logger: logging.Logger,
    message: str,
    start_time: float,
) -> None:
    """Add INFO log entry, with elapsed time since `start_time`."""
    _log(logger=logger, level=logging.INFO, message=message, start_time=start_time)


def _log(
    *,
    logger: logging.Logger,
    level: int,
    message: str,
    start_time: float,
) -> None:
    """Add log entry, with elapsed time since `start_time`."""
    elapsed_time = time.time() - start_time
    log_message = f" Elapsed time: {elapsed_time:.2f} s. {message}"
    logger.log(level=level, msg=log_message)
