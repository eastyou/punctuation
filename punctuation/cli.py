"""punctuation 命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .model import MARKS, check_pairs, count_marks, make_quiz, mark_info
from .render import quiz_html


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="punctuation", description="中文标点：规则查询、配对检查与练习生成"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    info = sub.add_parser("info", help="查询一个标点的用法")
    info.add_argument("symbol", help="要查询的标点，例如 ，")

    check = sub.add_parser("check", help="检查引号、括号是否成对")
    check.add_argument("text", help="待检查的句子")

    count = sub.add_parser("count", help="统计标点数量")
    count.add_argument("text", help="待统计的句子")

    sub.add_parser("rules", help="列出全部标点规则")

    quiz = sub.add_parser("quiz", help="生成标点练习单")
    quiz.add_argument("--count", type=int, default=8, help="题目数量")
    quiz.add_argument("--seed", type=int, default=None, help="随机种子")
    quiz.add_argument("-o", "--output", required=True, help="输出 HTML 路径")
    quiz.add_argument("--no-answers", action="store_true", help="不附答案页")

    return parser


def _run(args: argparse.Namespace) -> int:
    if args.command == "info":
        info = mark_info(args.symbol)
        print("%s  %s" % (info["symbol"], info["name"]))
        print("用法：%s" % info["usage"])
        print("例句：%s" % info["example"])
        return 0
    if args.command == "check":
        problems = check_pairs(args.text)
        if not problems:
            print("配对检查通过：引号、括号、书名号均成对。")
            return 0
        for index, problem in enumerate(problems, start=1):
            print("问题 %d：%s" % (index, problem))
        return 1
    if args.command == "count":
        counts = count_marks(args.text)
        if not counts:
            print("未发现已收录的标点。")
            return 0
        total = sum(counts.values())
        print("共 %d 个标点：" % total)
        for symbol, amount in counts.items():
            print("  %s %s × %d" % (symbol, MARKS[symbol]["name"], amount))
        return 0
    if args.command == "rules":
        print("共收录 %d 个标点：" % len(MARKS))
        for symbol, info in MARKS.items():
            print("%s  %s：%s" % (symbol, info["name"], info["usage"]))
        return 0
    if args.command == "quiz":
        questions = make_quiz(args.count, args.seed)
        Path(args.output).write_text(
            quiz_html(questions, include_answers=not args.no_answers),
            encoding="utf-8",
        )
        print("已生成练习：%s（%d 题）" % (args.output, len(questions)))
        return 0
    raise ValueError("未知命令：%s" % args.command)


def _ensure_utf8_console() -> None:
    """Windows 控制台默认编码可能无法输出中文，尽量切换为 UTF-8。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            continue


def main(argv: Optional[Sequence[str]] = None) -> int:
    _ensure_utf8_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return _run(args)
    except (TypeError, ValueError) as exc:
        print("错误：%s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
