from typing import Generator

def current_task() -> Generator[int]:
    """Return number of current task"""
    count = 1

    while True:
        yield count
        count += 1