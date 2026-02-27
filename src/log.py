import logging

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
        datefmt="[%d.%m.%Y %H:%M:%S]"
    )

    # === FILE HANDLER === #
    file_handler = logging.FileHandler("logs.log", mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # === CONSOLE HANLDER === #
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)

    # === ROOT LOGGER === #
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)