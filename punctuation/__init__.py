"""punctuation：中文标点符号学习与练习工具。"""

from .model import (
    MARKS,
    QUESTIONS,
    check_pairs,
    count_marks,
    grade,
    make_quiz,
    mark_info,
)
from .render import answer_key_html, info_card_html, quiz_html, rules_html

__all__ = [
    "MARKS",
    "QUESTIONS",
    "check_pairs",
    "count_marks",
    "grade",
    "make_quiz",
    "mark_info",
    "answer_key_html",
    "info_card_html",
    "quiz_html",
    "rules_html",
]

__version__ = "0.1.0"
