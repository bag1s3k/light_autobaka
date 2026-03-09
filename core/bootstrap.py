import logging

def initialize() -> None:
    """
    Initialize the application by setting up:
    - rich traceback
    - logging
    - loading environment variables
    - and logging setup.
    """
    from rich.traceback import install
    install()

    from utils import config_exists
    config_exists()

    from dotenv import load_dotenv
    load_dotenv()

    from logs import logging_setup
    logging_setup()

    logger = logging.getLogger(__name__)
    logger.debug("System initialized via bootstrap")
