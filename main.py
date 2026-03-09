from core import initialize
initialize()

import logging

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

from utils import ProgressConfig, display_results, get_login_details, Export
from core import fetch_data, calc_marks

logger = logging.getLogger(__name__)

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeRemainingColumn(),
    transient=True
) as progress:
    
    STEPS = ["Load Credentials", "Fetch Data", "Calculate Marks", "Export Results"]
    progress_config = ProgressConfig(len(STEPS), progress)

    username, password = get_login_details("BAKA_USERNAME", "BAKA_PASSWORD")
    progress_config.update_progress()

    marks = fetch_data(username, password)
    progress_config.update_progress()

    average = calc_marks(marks)
    progress_config.update_progress()

    Export(average).results()
    progress_config.update_progress()

display_results(average)
