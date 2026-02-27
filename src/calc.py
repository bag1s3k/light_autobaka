import logging
from typing import TYPE_CHECKING

from utils import calc_average

if TYPE_CHECKING:
    from utils import Mark


logger = logging.getLogger(__name__)

def calc_marks(marks: list["Mark"]) -> dict[str, float]:
    """
    Calculate average of each mark

    Args:
        marks (Mark): list of all marks
    Return:
        dict[str, float]: Subjects and it's average
    """

    if not marks:
        logger.warning("No marks to calculate")
        return {}

    # === CREATE HASHMAP === #
    hashmap = dict()
    for m in marks:
        subject = m.subject
        mark = m.mark
        weight = m.weight

        if subject not in hashmap:
            hashmap[subject] = []

        hashmap[subject].append((mark, weight))

    # === CALCULATE AVERAGE === #    
    result = hashmap.copy()
    for s, m in hashmap.items():
        result[s] = calc_average(m)
    
    logger.info("Subjects and it's average succesfully calculated")
    return result