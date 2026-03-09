import logging
from rich.logging import RichHandler

from config import appconfig

def _show_only_warning(record):
    """Filter for rich console handler to show only WARNINGS logs"""
    return record.levelname == "WARNING"

def logging_setup():
    """
    Setup loggers
    Output format: ERROR %d.%m.%Y %H:%M:%S - name - message

    Handlers:
        file handler: log everything
        console handler: log warning and higher
    """

    formatter_file = logging.Formatter(
        fmt="{levelname:8} {asctime} {name} - {message}",
        datefmt="%H:%M:%S",
        style="{"
    )

    formatter_rich = logging.Formatter(
        fmt="[dark_red]{name}[/] {message}",
        datefmt="%H:%M:%S",
        style="{"
    )

    # === FILE HANDLER === #
    file_handler = logging.FileHandler(appconfig.path.log, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter_file)

    # === CONSOLE HANDLER === #
    rich_handler = RichHandler(
        level=logging.WARNING,
        rich_tracebacks=True,
        omit_repeated_times=False,
        markup=True
    )
    rich_handler.addFilter(_show_only_warning)
    rich_handler.setFormatter(formatter_rich)

    # === ROOT LOGGER === #
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(rich_handler)
