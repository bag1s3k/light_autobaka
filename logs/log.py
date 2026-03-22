import logging
from rich.logging import RichHandler

from config.set_config import appconfig
from utils.constants import IS_GITHUB_ACTIONS

def logging_setup():
    """
    CI environment + file output format: 'DEBUG %d.%m.%Y %H:%M:%S - name - message'
    Non-CI environment output format: 'WARNING %H:%M:%S - name - message'
    """

    # === ROOT LOGGER === #
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="{levelname:8} {asctime} {name} - {message}",
        datefmt="%d.%m.%Y %H:%M:%S",
        style="{"
    )

    # === Non-CI environment === #
    # Create file and console handler (console is rich handler).
    if not IS_GITHUB_ACTIONS:
        # === FILE HANDLER === #
        file_handler = logging.FileHandler(appconfig.path.log, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # === CONSOLE RICH HANDLER === #
        formatter_rich = logging.Formatter(
            fmt="[dark_red]{name}[/] {message}",
            datefmt="%H:%M:%S",
            style="{"
        )

        rich_handler = RichHandler(
            level=logging.WARNING,
            rich_tracebacks=True,
            omit_repeated_times=False,
            markup=True
        )
        rich_handler.setFormatter(formatter_rich)

        logger.addHandler(file_handler)
        logger.addHandler(rich_handler)

        logger.info("Logging setup to Non-CI use-case")

    # === CI environment === #
    # No need to create file handler and heave rich handler.
    # Suffices only basic console handler.
    else:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        logger.info("Logging setup to CI use-case")
