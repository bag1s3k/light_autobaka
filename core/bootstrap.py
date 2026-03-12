import logging

def initialize() -> None:
    """
    Initialize the application by setting up:
    - rich traceback
    - logging
    - loading environment variables
    - and logging setup.
    """

    # Setup rich tracebacks
    # TODO: issue traceback has no effect to pydantic's error
    from rich.traceback import install
    install()

    # Setup configuration of and app (config + login details)
    from utils.config_exists import config_exists
    config_exists()
    import utils.models.login_details

    # Setup logging (rich handler + file handle)
    from logs.log import logging_setup
    logging_setup()

    logger = logging.getLogger(__name__)
    logger.debug("System initialized via bootstrap")
