import os
import logging

from dotenv import load_dotenv

from utils.constants import USERNAME_ENV_TAG, PASSWORD_ENV_TAG

logger = logging.getLogger(__name__)

class LoginDetails:
    def __init__(self):
        load_dotenv()
        self.username = self._get_required(USERNAME_ENV_TAG)
        self.password = self._get_required(PASSWORD_ENV_TAG)
        logger.info("Login details loaded successful")

    @staticmethod
    def _get_required(key: str) -> str:
        """
        Load and validate env variables

        Args:
            key (str): name of env variable
        """
        if (value := os.getenv(key)) is None:
            raise ValueError(f"Failed to load {key.split("_")[1].lower()}")
        return value

login_details = LoginDetails()