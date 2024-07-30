"""Pathfinding package."""

import logging
import time


def log_debug(
    logger: logging.Logger,
    message: str,
    start_time: float | None = None,
) -> None:
    """Add DEBUG log entry; optionally include elapsed time."""
    _log(
        logger=logger,
        level=logging.DEBUG,
        message=message,
        start_time=start_time,
    )


def log_info(
    logger: logging.Logger,
    message: str,
    start_time: float | None = None,
) -> None:
    """Add INFO log entry; optionally include elapsed time."""
    _log(
        logger=logger,
        level=logging.INFO,
        message=message,
        start_time=start_time,
    )


def _log(
    *,
    logger: logging.Logger,
    level: int,
    message: str,
    start_time: float | None,
) -> None:
    """Add log entry; optionally include elapsed time."""
    log_message = f" {message}"
    if start_time:
        elapsed_time = time.time() - start_time
        log_message = f" Elapsed time: {elapsed_time:.2f} s. {log_message}"
    logger.log(level=level, msg=log_message)
