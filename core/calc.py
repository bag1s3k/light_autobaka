import logging
from typing import TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from utils import Mark

logger = logging.getLogger(__name__)

def _create_hashmap(marks: list["Mark"]) -> dict[str, list[tuple[int, int]]]:
    """
    Create hashmap
        
    Returns:
        dict: A dictionary where keys are subject names and values are lists of tuples containing (mark, weight)
    Example:
        {"math": [(1, 5), (3, 7)], "english": [(5, 3), (1, 7), (2, 4)]}
    """
    hashmap = defaultdict(list)
    for m in marks:
        subject = m.subject
        mark = m.mark
        weight = m.weight
        if mark > 0.0:
            hashmap[subject].append((mark, weight))
    return hashmap

def _calc_average(ms: list[tuple]) -> float:
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
        dict: Subjects and it's average
    """
    if not marks:
        logger.warning("No marks to calculate")
        return {}

    hashmap = _create_hashmap(marks)

    averages = {}
    for s, m in hashmap.items():
        averages[s] = _calc_average(m)
    logger.info("Subjects and it's average successfully calculated")
    return averages
