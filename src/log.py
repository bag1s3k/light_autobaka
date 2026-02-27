import logging
from rich.logging import RichHandler

def logging_setup():
    """
    Setup loggers
    Output format: ERROR %d.%m.%Y %H:%M:%S - name - message

    Hanlders:
        file handler: log everything
        console handler: log error and higher and in this case program will be execute
    """

    formatter = logging.Formatter(
        fmt="{levelname} {asctime} {name} - {message}",
        datefmt="%H:%M:%S",
        style="{"
    )

    # === FILE HANDLER === #
    file_handler = logging.FileHandler("logs.log", mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # === CONSOLE HANLDER === #
    rich_handler = RichHandler(
        level=logging.WARNING,
        rich_tracebacks=True
    )

    # === ROOT LOGGER === #
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(rich_handler)