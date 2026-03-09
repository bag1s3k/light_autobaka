import sys
import os
sys.path.append(os.getcwd())

from rich import print

from core import calc_marks
from utils import Mark
from logs import logging_setup
logging_setup()

def test_calc_marks_with_zero_marks():
    test_data = [
        {"nazev": "Math", "datum": "2026-03-06T10:21:00+01:00", "vaha": "3", "MarkText": "1", "id":"09648N-W1|"},
        {"nazev": "Czech", "vaha": "3", "MarkText": "N"},
        {"nazev": "Math", "vaha": "3", "MarkText": "A"},
        {"nazev": "Math", "vaha": "3", "MarkText": "2"},
        {"nazev": "Czech", "vaha": "3", "MarkText": "3-"}
    ]

    marks = [Mark(**mark) for mark in test_data]

    averages = calc_marks(marks)

    print(averages)
    print(marks)

if __name__ == "__main__":
    try:
        test_calc_marks_with_zero_marks()
    except Exception as e:
        raise e