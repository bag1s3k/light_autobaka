import logging

from rich.traceback import install
install()

from config.load_config import isconfig_exists
isconfig_exists()

from dotenv import load_dotenv
load_dotenv()

from logs.log import logging_setup
logging_setup()


logger = logging.getLogger(__name__)

logger.debug("System initialized via bootstrap")