"""punctuation 核心逻辑测试。"""

import unittest

from punctuation.model import (
    MARKS,
    QUESTIONS,
    check_pairs,
    count_marks,
    grade,
    make_quiz,
    mark_info,
)


class MarkInfoTests(unittest.TestCase):
    def test_every_mark_is_queryable(self):
        for symbol in MARKS:
            with self.subTest(symbol=symbol):
                info = mark_info(symbol)
                self.assertEqual(info["symbol"], symbol)
                self.assertTrue(info["name"])
                self.assertTrue(info["usage"])
                self.assertTrue(info["example"])

    def test_full_stop(self):
        info = mark_info("。")
        self.assertEqual(info["name"], "句号")

    def test_question_mark(self):
        self.assertEqual(mark_info("？")["name"], "问号")

    def test_strips_spaces(self):
        self.assertEqual(mark_info("  ！ ")["name"], "感叹号")

    def test_unknown_mark(self):
        with self.assertRaises(ValueError):
            mark_info("$")

    def test_empty_mark(self):
        with self.assertRaises(ValueError):
            mark_info("   ")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            mark_info(1)  # type: ignore[arg-type]

    def test_returns_copy(self):
        info = mark_info("。")
        info["name"] = "改坏了"
        self.assertEqual(MARKS["。"]["name"], "句号")


class CountTests(unittest.TestCase):
    def test_counts_common_marks(self):
        counts = count_marks("春天来了，小草绿了。")
        self.assertEqual(counts["，"], 1)
        self.assertEqual(counts["。"], 1)

    def test_counts_repeats(self):
        counts = count_marks("苹果、香蕉、梨。")
        self.assertEqual(counts["、"], 2)

    def test_empty_text(self):
        self.assertEqual(count_marks(""), {})

    def test_ignores_unknown_symbols(self):
        self.assertEqual(count_marks("abc"), {})

    def test_counts_quotes(self):
        counts = count_marks("他说：“走吧。”")
        self.assertEqual(counts["“"], 1)
        self.assertEqual(counts["”"], 1)

    def test_non_string(self):
        with self.assertRaises(TypeError):
            count_marks(None)  # type: ignore[arg-type]


class PairTests(unittest.TestCase):
    def test_balanced(self):
        self.assertEqual(check_pairs("他说：“走吧。”"), [])

    def test_unbalanced_quote(self):
        problems = check_pairs("他说：“走吧。")
        self.assertEqual(len(problems), 1)
        self.assertIn("引号", problems[0])

    def test_unbalanced_bracket(self):
        problems = check_pairs("李明（班长负责点名。")
        self.assertIn("括号", problems[0])

    def test_unbalanced_book_title(self):
        problems = check_pairs("我读过《西游记。")
        self.assertIn("书名号", problems[0])

    def test_multiple_problems(self):
        problems = check_pairs("《书名（注释")
        self.assertEqual(len(problems), 2)

    def test_empty_text(self):
        self.assertEqual(check_pairs(""), [])

    def test_non_string(self):
        with self.assertRaises(TypeError):
            check_pairs(123)  # type: ignore[arg-type]


class QuizTests(unittest.TestCase):
    def test_count(self):
        self.assertEqual(len(make_quiz(4, seed=1)), 4)

    def test_deterministic(self):
        first = make_quiz(5, seed=7)
        second = make_quiz(5, seed=7)
        self.assertEqual(
            [q["sentence"] for q in first], [q["sentence"] for q in second]
        )

    def test_answer_is_in_choices(self):
        for question in make_quiz(5, seed=3):
            with self.subTest(question=question["sentence"]):
                self.assertIn(question["answer"], question["choices"])

    def test_choices_have_four_options(self):
        for question in make_quiz(5, seed=3):
            self.assertEqual(len(question["choices"]), 4)

    def test_zero_count(self):
        with self.assertRaises(ValueError):
            make_quiz(0)

    def test_too_many(self):
        with self.assertRaises(ValueError):
            make_quiz(len(QUESTIONS) + 1)

    def test_negative_count(self):
        with self.assertRaises(ValueError):
            make_quiz(-2)

    def test_float_count(self):
        with self.assertRaises(TypeError):
            make_quiz(2.5)  # type: ignore[arg-type]

    def test_bool_count(self):
        with self.assertRaises(TypeError):
            make_quiz(True)  # type: ignore[arg-type]


class GradeTests(unittest.TestCase):
    def setUp(self):
        self.questions = make_quiz(3, seed=11)

    def test_all_correct(self):
        answers = [str(q["answer"]) for q in self.questions]
        result = grade(self.questions, answers)
        self.assertEqual(result, {"correct": 3, "total": 3, "score": 100})

    def test_all_wrong(self):
        answers = ["。", "。", "。"]
        wrong = sum(1 for q in self.questions if q["answer"] != "。")
        result = grade(self.questions, answers)
        self.assertEqual(result["correct"], 3 - wrong)

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            grade(self.questions, ["。"])

    def test_empty_questions(self):
        with self.assertRaises(ValueError):
            grade([], [])

    def test_non_string_answer(self):
        with self.assertRaises(TypeError):
            grade(self.questions, [1, 2, 3])  # type: ignore[list-item]

    def test_strips_answer(self):
        answers = [" %s " % q["answer"] for q in self.questions]
        self.assertEqual(grade(self.questions, answers)["correct"], 3)


class QuestionBankTests(unittest.TestCase):
    def test_bank_not_empty(self):
        self.assertGreaterEqual(len(QUESTIONS), 16)

    def test_each_answer_in_choices(self):
        for question in QUESTIONS:
            with self.subTest(sentence=question["sentence"]):
                self.assertIn(question["answer"], question["choices"])

    def test_each_has_explanation(self):
        for question in QUESTIONS:
            self.assertTrue(question["explain"])

    def test_sentences_have_blank(self):
        for question in QUESTIONS:
            self.assertIn("___", str(question["sentence"]))


if __name__ == "__main__":
    unittest.main()
