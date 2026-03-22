import os
import logging

from dotenv import load_dotenv

from utils.constants import USERNAME_ENV_TAG, PASSWORD_ENV_TAG, IS_GITHUB_ACTIONS

logger = logging.getLogger(__name__)

class EnvVariables:
    def __init__(self):
        load_dotenv()
        self.username = self._get_required(USERNAME_ENV_TAG)
        self.password = self._get_required(PASSWORD_ENV_TAG)

        if IS_GITHUB_ACTIONS:
            from utils.constants import SCHOOL_DATA_TAG
            self.school_data = self._get_required(SCHOOL_DATA_TAG)

        logger.info("Env variables were loaded successfully")

    @staticmethod
    def _get_required(key: str) -> str:
        """
        Load and validate env variables

        Args:
            key (str): name of env variable
        """
        if (value := os.getenv(key)) is None:
            raise ValueError(f"Failed to load {key}")
        return value

env_variables = EnvVariables()