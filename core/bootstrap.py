import logging

from utils.constants import IS_GITHUB_ACTIONS
from utils.models.progress_config import update_progress

@update_progress("Initializing")
def initialize() -> None:
    """
    Initialize the application by setting up:
    - rich traceback
    - logging
    - setup app configuration
    - loading environment variables
    - and logging setup.
    """

    # === Non-CI environment === #
    if not IS_GITHUB_ACTIONS:
        # TODO: issue traceback has no effect to pydantic's error
        from rich.traceback import install
        install()

        from utils.config_exists import config_exists
        config_exists()

    from logs.log import logging_setup
    logging_setup()

    import utils.models.env_vars

    logger = logging.getLogger(__name__)
    logger.debug(f"System initialized via bootstrap CI-Environment: {IS_GITHUB_ACTIONS}")
