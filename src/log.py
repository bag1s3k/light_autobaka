import logging
import sys

def logging_setup():
    """
    Setup loggers
    Output format: ERROR %d.%m.%Y %H:%M:%S - name - message

    Hanlders:
        file handler: log everything
        console handler: log error and higher and in this case program will be execute
    """
    formatter = logging.Formatter(
        fmt="%(levelname)-8s %(asctime)s - %(name)s - %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S"
    )

    # === FILE HANDLER === #
    file_handler = logging.FileHandler("logs.log", mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # === CONSOLE HANLDER === #
    class ExitHandler(logging.StreamHandler):
        def emit(self, record):
            super().emit(record)
            if record.levelno in (logging.ERROR, logging.CRITICAL):
                sys.exit(1)
    console_handler = ExitHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)