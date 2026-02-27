from typing import Generator

class ProgressConfig:
    """Configuration for the progress update function"""

    def __init__(self, total_task, progress, step: int = 1):
        self.progress = progress
        self.total_task = total_task
        self.step = step
        self.description = f"{next(self.counter)}/{total_task}"

        # create task
        self.task_id = self.progress.add_task("", total=self.total_task)

        # Init generator
        self.counter = self._current_task()

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