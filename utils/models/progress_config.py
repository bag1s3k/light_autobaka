import functools
from typing import Any, Callable
from typing import Generator
import logging

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

from utils.constants import IS_GITHUB_ACTIONS

logger = logging.getLogger(__name__)

class ProgressConfig:
    """Configuration for the progress update function"""

    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            transient=True
        )

        # create task
        self.task_id = self.progress.add_task("Initializing", total=self.total_steps)

        # Init generator
        self.counter = self._step_counter()

    def __enter__(self):
        self.progress.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.stop()

    def update_progress(self, description: str = "") -> None:
            """Update progress rich bar"""
            self.progress.update(
                self.task_id,
                advance=1,
                description=f"{next(self.counter)}/{self.total_steps} {description}..."
            )

    @staticmethod
    def _step_counter() -> Generator[int]:
        """Return number of current task"""
        count = 0

        while True:
            yield count
            count += 1

if not IS_GITHUB_ACTIONS:
    STEPS = [
        "Initializing",
        "Config exists"
        "Logging",
        "Load config",
        "Calculating",
        "Fetching",
        "Export",
        "Export2"
    ]
    progress_bar = ProgressConfig(len(STEPS))

def update_progress(description: str):
    """Decorator used for updating rich progress bar"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:

            if not IS_GITHUB_ACTIONS:
                try:
                    progress_bar.update_progress(description)
                except Exception as e:
                    logger.error(f"Progress update failed: {e}")

            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator