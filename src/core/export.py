from config.load_config import appconfig
import json
import logging

logger = logging.getLogger(__name__)

def export_json(data: dict) -> None:
    """
    Export raw fetched data converted to json

    Args:
        data (dict): raw marks
    """
    if not data:
        logger.warning("No json data to export")
        return
    
    try:
        with open(appconfig.path.raw_marks, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        logger.info("Export json data succesfull")

    except Exception as e:
        logger.exception("Exporting json data failed")



def export_average(data: dict) -> None:
    """
    Export subject and it's average

    Args:
        data (dict): averages
    """
    if not data:
        logger.warning("No marks to export")
        return

    try:
        with open(appconfig.path.results, "w", encoding="utf-8") as f:
            for s, a in data.items():
                f.write(f"{s:30} {a}\n")
        logger.info("Export result succesfull")

    except:
        logger.error("Export result failed")
