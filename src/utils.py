from typing import Generator
from rich.table import Table
from rich.console import Console
from rich import box
import logging
from typing import Annotated
from pydantic import BeforeValidator, Field

logger = logging.getLogger(__name__)

class ProgressConfig:
    """Configuration for the progress update function"""

    def __init__(self, total_task, progress, step: int = 1):
        self.progress = progress
        self.total_task = total_task
        self.step = step

        # create task
        self.task_id = self.progress.add_task("", total=self.total_task)

        # Init generator
        self.counter = self._current_task()
        self.description = f"{next(self.counter)}/{total_task}"

    def update_progress(self) -> None: 
            """Update progress rich bar"""
            self.progress.update(
                self.task_id,
                advance=1,
                description=f"{next(self.counter)}/{self.total_task}"
            )

    def _current_task(self) -> Generator[int]:
        """Return number of current task"""
        count = 0

        while True:
            yield count
            count += 1


def display_results(data: dict[str, float]) -> None:
    """ 
    Display results (subject and it's average)

    Args:
        data (dict): marks to display
    """
    if not data:
        return

    table = Table(box=box.SIMPLE)

    table.add_column("Subject")
    table.add_column("Average", style="cyan")

    for s, a in data.items():
        table.add_row(s, str(a))

    console = Console()
    console.print(table)

# === HELP FUNCS TO VALIDATIONS === #
def clean_mark(m: str) -> float:
    """
    Convert str to int & from '1-' (which is not number) make '-1'

    Args:
        m (str): mark to check
    Returns:
        int | str: correct mark
    """

    m = m.strip()

    if len(m) > 1:
        return float(m[0]) + 0.5
    
    if m.isnumeric():
        return float(m)
    else:
        return 0.0

def is_empty(s) -> str:
    """Tell me if there is missing value"""
    
    if s is None:
        logger.warning("Field is empty")
    
    return s

# === OWN ANNOTATED === #
MissingDescription = Annotated[
    str | None,
    BeforeValidator(is_empty),
    Field(default="Missing")
]

MarkValue = Annotated[
    float,
    BeforeValidator(clean_mark),
    Field(alias="MarkText")
]