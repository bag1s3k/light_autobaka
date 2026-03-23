from core.bootstrap import initialize
initialize()

import logging

from utils.constants import IS_GITHUB_ACTIONS
from core.fetch import  fetch_data
from core.calc import calc_marks

logger = logging.getLogger(__name__)


if not IS_GITHUB_ACTIONS:
    from utils.output import display_results
    from utils.models.export import Export
    from utils.models.progress_config import progress_bar

    with progress_bar:
        marks = fetch_data()
        average = calc_marks(marks)

        Export(average).results()

    display_results(average)
else:
    from ui.generate_html import create_html

    marks = fetch_data()
    average = calc_marks(marks)

    create_html(average)




