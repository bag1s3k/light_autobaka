import logging
from typing import TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from utils.models.mark import Mark

logger = logging.getLogger(__name__)

def _group_marks_by_subject(marks: list["Mark"]) -> dict[str, list[tuple[int, int]]]:
    """
    Group marks into a dictionary by subject name
        
    Returns:
        dict: A dictionary where keys are subject names and values are lists of tuples containing (mark, weight)
    Example:
        {"math": [(1, 5), (3, 7)], "english": [(5, 3), (1, 7), (2, 4)]}
    """
    marks_by_subject = defaultdict(list)
    for m in marks:
        subject = m.subject
        mark = m.mark
        weight = m.weight
        if mark > 0.0:
            marks_by_subject[subject].append((mark, weight))
    return marks_by_subject

def _calc_weighted_average(ms: list[tuple]) -> float:
    """
    Help method to calculate average of current subject

    Args:
        ms (List[tuple]): one tuple represents one mark (mark, weight)
    Returns:
        float: average of subject
    """
    weighted_sum = sum(m[0] * m[1] for m in ms)
    total_weight = sum(m[1] for m in ms)
    return round(weighted_sum / total_weight, 2)

def calc_marks(marks: list["Mark"]) -> dict[str, float]:
    """
    Calculate the weighted average grade per subject

    Returns:
        dict: Subjects and its average
    """
    if not marks:
        logger.warning("No marks to calculate")
        return {}

    marks_by_subject = _group_marks_by_subject(marks)

    averages = {}
    for subject, subject_marks in marks_by_subject.items():
        averages[subject] = _calc_weighted_average(subject_marks)
        
    logger.info("Subjects and it's average successfully calculated")
    return averages
