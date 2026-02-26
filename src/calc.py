from typing import List, TYPE_CHECKING
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from fetch import Mark

def calc_marks(marks: List["Mark"]) -> dict[str, float]:
    """
    Calculate average of each mark

    Args:
        marks (Mark): list of all marks
    Return:
        dict[str, float]: Subjects and it's average
    """

    # === CREATE HASHMAP === #
    hashmap = dict()
    for m in marks:
        subject = m.subject
        mark = m.mark
        weight = m.weight

        if subject not in hashmap:
            hashmap[subject] = []

        hashmap[subject].append((mark, weight))

    def calc_average(ms: List[tuple]) -> float:
        """
        Help method to calculate average of mark

        Arg:
            ms (List[tuple]): one tuple is mark (mark, weight)
        Return:
            float: average of subject
        """

        weighted_sum = sum(m[0] * m[1] for m in ms)
        total_weight = sum(m[1] for m in ms)

        return round(weighted_sum / total_weight, 2)

    # === CALCULATE AVERAGE === #    
    result = hashmap.copy()
    for s, m in hashmap.items():
        result[s] = calc_average(m)
    
    logger.info("Subjects and it's average succesfully calculated")
    return result