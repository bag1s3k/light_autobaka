import logging
from collections import defaultdict

from .models import Mark


logger = logging.getLogger(__name__)


def calc_marks(marks: list[Mark]) -> dict[str, tuple[float, list[tuple[float, int]]]]:
    """Calculate weighted averages for numeric marks in each subject."""
    grouped: dict[str, list[tuple[float, int]]] = defaultdict(list)
    for mark in marks:
        if mark.mark > 0:
            grouped[mark.subject].append((mark.mark, mark.weight))

    if not marks:
        logger.warning("No marks to calculate")

    return {
        subject: (
            round(sum(value * weight for value, weight in subject_marks)
                  / sum(weight for _, weight in subject_marks), 2),
            subject_marks,
        )
        for subject, subject_marks in grouped.items()
    }
