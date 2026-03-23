import json
import logging

from utils.models.progress_config import update_progress

logger = logging.getLogger(__name__)

# TODO: maybe do it on new thread, and pickle??
class Export:
    def __init__(self, data) -> None:
        self.data: dict = self._ensure_data_exists(data)

    @update_progress("Exporting")
    def fetched_data(self) -> None:
        """Export raw fetched data converted to JSON"""
        if not self.data:
            return
        
        from config.set_config import appconfig

        try:
            with open(appconfig.path.raw_marks, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)

            logger.info("Export raw fetched data in json format successful")
        except(IsADirectoryError, PermissionError):
            logger.error(f"Attempt to export failed: '{appconfig.path.raw_marks}' is a FOLDER not a file!")
        except Exception as e:
            logger.exception(e)

    @update_progress("Exporting")
    def results(self) -> None:
        """Export subject and its average"""
        if not self.data:
            return
        
        from config.set_config import appconfig

        try:
            with open(appconfig.path.results, "w", encoding="utf-8") as f:
                for s, a in self.data.items():
                    f.write(f"{s:30} {a}\n")

            logger.info("Export results successful")
        except (IsADirectoryError, PermissionError):
            logger.error(f"Attempt to export failed: '{appconfig.path.results}' is a FOLDER not a file!")
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def _ensure_data_exists(data: dict) -> dict:
        if not data:
            logger.warning(f"No data to export")
            return {}
        
        return data