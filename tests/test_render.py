"""punctuation 渲染测试。"""

import unittest

from punctuation.model import make_quiz
from punctuation.render import answer_key_html, info_card_html, quiz_html, rules_html

QUESTIONS = make_quiz(3, seed=5)


class RulesTests(unittest.TestCase):
    def test_renders_table(self):
        table = rules_html()
        self.assertIn("<table>", table)
        self.assertIn("句号", table)

    def test_contains_symbols(self):
        table = rules_html()
        self.assertIn("。", table)
        self.assertIn("？", table)

    def test_contains_usage(self):
        self.assertIn("疑问句", rules_html())


class AnswerKeyTests(unittest.TestCase):
    def test_lists_answers(self):
        key = answer_key_html(QUESTIONS)
        self.assertIn("<ol", key)
        for index in range(1, 4):
            self.assertIn("第 %d 题" % index, key)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            answer_key_html([])


class QuizHtmlTests(unittest.TestCase):
    def test_full_document(self):
        page = quiz_html(QUESTIONS)
        self.assertTrue(page.startswith("<!DOCTYPE html>"))
        self.assertIn("</html>", page)

    def test_contains_question(self):
        page = quiz_html(QUESTIONS)
        self.assertIn(str(QUESTIONS[0]["sentence"]), page)

    def test_contains_options(self):
        page = quiz_html(QUESTIONS)
        self.assertIn("<input type=\"radio\"", page)

    def test_contains_answers_by_default(self):
        page = quiz_html(QUESTIONS)
        self.assertIn("参考答案", page)

    def test_can_hide_answers(self):
        page = quiz_html(QUESTIONS, include_answers=False)
        self.assertNotIn("参考答案", page)

    def test_custom_title(self):
        page = quiz_html(QUESTIONS, title="期末专项练习")
        self.assertIn("期末专项练习", page)

    def test_escapes_title(self):
        page = quiz_html(QUESTIONS, title="<b>练习</b>")
        self.assertNotIn("<b>", page)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            quiz_html([])

    def test_question_count_footer(self):
        page = quiz_html(QUESTIONS)
        self.assertIn("共 3 题", page)


class InfoCardTests(unittest.TestCase):
    def test_contains_name(self):
        card = info_card_html("，")
        self.assertIn("逗号", card)

    def test_contains_example(self):
        card = info_card_html("？")
        self.assertIn("例", card)

    def test_unknown_symbol(self):
        with self.assertRaises(ValueError):
            info_card_html("@")


if __name__ == "__main__":
    unittest.main()
