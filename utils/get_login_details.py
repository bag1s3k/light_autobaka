import os
import logging

logger = logging.getLogger(__name__)

def get_login_details(username_tag, password_tag) -> tuple[str, str]:
    """
    Load login details

    Args:
        username_tag (str): name of username env variable
        password_tag (str): name of password env variable
    Returns:
        tuple[str, str]: username, password
    """
    if (username := os.getenv(username_tag)) is None:
        raise Exception("Failed to load username")
    if (password := os.getenv(password_tag)) is None:
        raise Exception("Failed to load password")

    logger.info("Login details loaded successful")
    return username, password