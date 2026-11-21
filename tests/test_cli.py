"""punctuation 命令行测试。"""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from punctuation.cli import main


def run(args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(args)
    return code, out.getvalue(), err.getvalue()


class InfoCommandTests(unittest.TestCase):
    def test_info_output(self):
        code, out, _ = run(["info", "。"])
        self.assertEqual(code, 0)
        self.assertIn("句号", out)
        self.assertIn("用法", out)

    def test_info_unknown(self):
        code, _, err = run(["info", "$"])
        self.assertEqual(code, 2)
        self.assertIn("暂不支持", err)


class CheckCommandTests(unittest.TestCase):
    def test_balanced(self):
        code, out, _ = run(["check", "他说：“走吧。”"])
        self.assertEqual(code, 0)
        self.assertIn("通过", out)

    def test_unbalanced(self):
        code, out, _ = run(["check", "他说：“走吧。"])
        self.assertEqual(code, 1)
        self.assertIn("问题 1", out)


class CountCommandTests(unittest.TestCase):
    def test_counts(self):
        code, out, _ = run(["count", "苹果、香蕉、梨。"])
        self.assertEqual(code, 0)
        self.assertIn("共 3 个标点", out)

    def test_empty(self):
        code, out, _ = run(["count", "abc"])
        self.assertEqual(code, 0)
        self.assertIn("未发现", out)


class RulesCommandTests(unittest.TestCase):
    def test_rules(self):
        code, out, _ = run(["rules"])
        self.assertEqual(code, 0)
        self.assertIn("句号", out)
        self.assertIn("问号", out)


class QuizCommandTests(unittest.TestCase):
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "quiz.html"
            code, out, _ = run(["quiz", "--count", "4", "-o", str(output)])
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            self.assertIn("4 题", out)

    def test_seed_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "a.html"
            second = Path(tmp) / "b.html"
            run(["quiz", "--count", "5", "--seed", "9", "-o", str(first)])
            run(["quiz", "--count", "5", "--seed", "9", "-o", str(second)])
            self.assertEqual(
                first.read_text(encoding="utf-8"), second.read_text(encoding="utf-8")
            )

    def test_no_answers(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "quiz.html"
            run(["quiz", "--count", "3", "-o", str(output), "--no-answers"])
            self.assertNotIn("参考答案", output.read_text(encoding="utf-8"))

    def test_too_many_questions(self):
        code, _, err = run(["quiz", "--count", "99", "-o", "unused.html"])
        self.assertEqual(code, 2)
        self.assertIn("不能超过", err)

    def test_requires_output(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main(["quiz", "--count", "3"])
        self.assertEqual(ctx.exception.code, 2)


class ParserTests(unittest.TestCase):
    def test_help(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stdout(io.StringIO()):
                main(["--help"])
        self.assertEqual(ctx.exception.code, 0)

    def test_no_command(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main([])
        self.assertEqual(ctx.exception.code, 2)

    def test_unknown_command(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main(["guess"])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
