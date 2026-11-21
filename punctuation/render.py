"""标点符号练习页与规则表渲染。"""

from __future__ import annotations

import html
from typing import Dict, Sequence

from .model import MARKS, mark_info

LETTERS = ("A", "B", "C", "D")


def _safe(text: object) -> str:
    return html.escape(str(text), quote=True)


def rules_html() -> str:
    rows = []
    for symbol, info in MARKS.items():
        rows.append(
            "<tr><td class=\"sym\">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (
                _safe(symbol),
                _safe(info["name"]),
                _safe(info["usage"]),
                _safe(info["example"]),
            )
        )
    return (
        "<table><thead><tr><th>标点</th><th>名称</th><th>用法</th><th>例句</th></tr>"
        "</thead><tbody>%s</tbody></table>" % "".join(rows)
    )


def answer_key_html(questions: Sequence[Dict[str, object]]) -> str:
    if not questions:
        raise ValueError("至少需要一道题")
    items = []
    for index, question in enumerate(questions, start=1):
        items.append(
            "<li>第 %d 题：<strong>%s</strong>（%s）</li>"
            % (
                index,
                _safe(question["answer"]),
                _safe(question.get("explain", "")),
            )
        )
    return "<ol class=\"key\">%s</ol>" % "".join(items)


def quiz_html(
    questions: Sequence[Dict[str, object]],
    title: str = "标点符号练习",
    include_answers: bool = True,
) -> str:
    """生成带选项的练习单，可附答案页。"""
    if not questions:
        raise ValueError("至少需要一道题")
    safe_title = _safe(title or "标点符号练习")
    blocks = []
    for index, question in enumerate(questions, start=1):
        choices = list(question["choices"])  # type: ignore[arg-type]
        options = "".join(
            "<label class=\"opt\"><input type=\"radio\" name=\"q%d\"> %s. %s</label>"
            % (index, LETTERS[position % len(LETTERS)], _safe(choice))
            for position, choice in enumerate(choices)
        )
        blocks.append(
            "<div class=\"q\"><p>%d. %s</p><div class=\"opts\">%s</div></div>"
            % (index, _safe(question["sentence"]), options)
        )
    answers = answer_key_html(questions) if include_answers else ""
    return (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>%s</title>\n<style>\n"
        "body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;"
        "background:#f0f9ff;margin:0;padding:24px;color:#0f172a}\n"
        ".card{max-width:760px;margin:0 auto 20px;background:#fff;border-radius:16px;"
        "padding:24px;box-shadow:0 10px 24px rgba(15,23,42,.1)}\n"
        "h1{font-size:21px;margin:0 0 14px}h2{font-size:16px;margin:0 0 10px}\n"
        ".q{margin-bottom:16px}.q p{margin:0 0 6px;font-size:15px}\n"
        ".opts{display:flex;flex-wrap:wrap;gap:12px;color:#334155}\n"
        ".opt{font-size:14px;background:#f8fafc;border-radius:8px;padding:4px 10px}\n"
        ".key{line-height:1.9;font-size:14px;color:#0f172a}\n"
        "table{width:100%%;border-collapse:collapse;font-size:14px}\n"
        "th,td{border-bottom:1px solid #e2e8f0;padding:8px;text-align:left}\n"
        ".sym{font-size:18px;text-align:center;width:64px}\n"
        "footer{font-size:12px;color:#64748b;margin-top:14px}\n"
        "</style>\n</head>\n<body>\n"
        "<section class=\"card\"><h1>%s</h1>%s"
        "<footer>由 punctuation 生成 · 共 %d 题</footer></section>\n"
        "%s\n</body>\n</html>"
        % (
            safe_title,
            safe_title,
            "".join(blocks),
            len(questions),
            "<section class=\"card\"><h2>参考答案</h2>%s</section>" % answers
            if include_answers
            else "",
        )
    )


def info_card_html(symbol: str) -> str:
    """输出单个标点的知识卡片。"""
    info = mark_info(symbol)
    return (
        "<div class=\"mark-card\"><div class=\"big\">%s</div>"
        "<div><h2>%s</h2><p>%s</p><p class=\"eg\">例：%s</p></div></div>"
        % (
            _safe(info["symbol"]),
            _safe(info["name"]),
            _safe(info["usage"]),
            _safe(info["example"]),
        )
    )
