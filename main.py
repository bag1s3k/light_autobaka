from core.bootstrap import initialize
initialize()

import logging

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

from utils import ProgressConfig, display_results, Export
from core import fetch_data, calc_marks

logger = logging.getLogger(__name__)


# TODO: make progress bar updatable global
# TODO: possible to add more than few checkpoints (a lot of is happening in the background)
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

    progress_config.update_progress() # temporary represents loading configuration

    marks = fetch_data()
    progress_config.update_progress()

    average = calc_marks(marks)
    progress_config.update_progress()

    Export(average).results()
    progress_config.update_progress()

display_results(average)
