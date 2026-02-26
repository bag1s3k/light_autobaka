from load_config import JSON_MARKS, RESULT_MARKS
import json
import logging

logger = logging.getLogger(__name__)

def export_json(data: dict) -> None:
    """
    Export raw fetched data converted to json

    Args:
        data (dict): marks
    """
    with open(JSON_MARKS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    logger.info("Export json data succesfull")


def export_average(data: dict) -> None:
    """
    Export subject and it's average

    Args:
        data (dict): averages
    """
    with open(RESULT_MARKS, "w", encoding="utf-8") as f:
        for s, a in data.items():
            f.write(f"{s:30} {a}\n")

    logger.info("Export result succesfull")