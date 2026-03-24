import logging
from datetime import datetime

from jinja2 import Template
import pytz

from config.set_config import appconfig
from utils.output import style_marks

logger = logging.getLogger(__name__)

def create_html(context: dict["str", float]) -> None:
    """Generate HTML file with the results"""
    if not context:
        return
    try:
        with open(appconfig.path.html_template, "r", encoding="utf-8") as f:
            template_html = f.read()
    except FileNotFoundError:
        raise FileNotFoundError("File with HTML template not found")

    template = Template(template_html)

    with open(appconfig.path.html_output, "w", encoding="utf-8") as f:
        czech_tz = pytz.timezone("Europe/Prague")
        html_content = template.render(
            data=context,
            title="Bakalari Averages",
            style_marks=style_marks,
            last_update=datetime.now(tz=czech_tz).strftime("%Y-%m-%d %H:%M:%S")
        )
        f.write(html_content)

    logger.debug(f"HTML file create on path: {appconfig.path.html_output}")