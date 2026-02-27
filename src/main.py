import logging

from rich.traceback import install
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from dotenv import load_dotenv

from log import logging_setup

# Intialization
install()
logging_setup()
load_dotenv()

from fetch import fetch_data
from calc import calc_marks
from export import export_average
from utils import ProgressConfig, display_results, get_credentials


logger = logging.getLogger(__name__)


with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeRemainingColumn(),
    transient=True
) as progress:
    
    # === SETUP FOR PROGRESS BAR == #
    config = ProgressConfig(4, progress)

    # === LOAD LOGIN DETAILS === #
    username, password = get_credentials("BAKA_USERNAME", "BAKA_PASSWORD")
    config.update_progress()

    # === GET MARKS === #
    marks = fetch_data(username, password)
    config.update_progress()

    # === CALCULATE MARKS === #
    average = calc_marks(marks)
    config.update_progress()

    # === EXPORT RESULTS === #
    export_average(average)
    config.update_progress()

# === OUTPUT === #
display_results(average)