from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from fetch import Mark

def calc_marks(marks: List["Mark"]) -> dict[str, float]:

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
    def calc_average(s: str, ms: List[tuple]) -> float:
        weighted_sum = sum(m[0] * m[1] for m in ms)
        total_weight = sum(m[1] for m in ms)

        return round(weighted_sum / total_weight, 2)
    
    result = hashmap.copy()
    for s, m in hashmap.items():
        result[s] = calc_average(s, m)
    
    return result