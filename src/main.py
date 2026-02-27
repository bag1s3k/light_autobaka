import logging
from rich.traceback import install
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from dotenv import load_dotenv
from log import logging_setup

# Intialization
install()
logging_setup()
load_dotenv()

from fetch import fetch_data
from calc import calc_marks
from export import export_average
from progress import current_task
from load_config import get_credentials


logger = logging.getLogger(__name__)


with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),               # Samotná čára
    TaskProgressColumn(),      # Procenta
) as progress:
    
    # === SETUP FOR PROGRESS BAR == #    
    total_task = 4
    task = current_task()
    run = progress.add_task("", total=total_task)

    def update_progress() -> None: 
        """Update progress rich bar"""
        progress.update(run, advance=1, description=f"{next(task)}/{total_task}")

    # === LOAD LOGIN DETAILS === #
    username, password = get_credentials("BAKA_USERNAME", "BAKA_PASSWORD")
    update_progress()

    # === GET MARKS === #
    marks = fetch_data(username, password)
    update_progress()

    # === CALCULATE MARKS === #
    average = calc_marks(marks)
    update_progress()

    # === EXPORT RESULTS === #
    export_average(average)
    update_progress()