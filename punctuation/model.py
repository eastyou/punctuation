"""中文标点符号：规则查询、配对检查与练习生成。"""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Sequence, Tuple

MARKS: Dict[str, Dict[str, str]] = {
    "。": {"name": "句号", "usage": "陈述句末尾的停顿", "example": "今天天气真好。"},
    "，": {"name": "逗号", "usage": "句子内部的停顿", "example": "春天来了，小草绿了。"},
    "、": {"name": "顿号", "usage": "并列词语之间的停顿", "example": "我喜欢苹果、香蕉和梨。"},
    "；": {"name": "分号", "usage": "并列分句之间的停顿", "example": "白天读书；晚上写字。"},
    "：": {"name": "冒号", "usage": "提示下文或总结上文", "example": "他带来三样东西：笔、本子、橡皮。"},
    "？": {"name": "问号", "usage": "疑问句末尾", "example": "你叫什么名字？"},
    "！": {"name": "感叹号", "usage": "感叹句或祈使句末尾", "example": "多么美丽的景色啊！"},
    "“": {"name": "左引号", "usage": "引用内容开始", "example": "他说：“我们出发吧。”"},
    "”": {"name": "右引号", "usage": "引用内容结束", "example": "他说：“我们出发吧。”"},
    "（": {"name": "左括号", "usage": "补充说明开始", "example": "李明（班长）负责点名。"},
    "）": {"name": "右括号", "usage": "补充说明结束", "example": "李明（班长）负责点名。"},
    "《": {"name": "左书名号", "usage": "书名、篇名开始", "example": "我读过《西游记》。"},
    "》": {"name": "右书名号", "usage": "书名、篇名结束", "example": "我读过《西游记》。"},
    "——": {"name": "破折号", "usage": "解释说明或话题转折", "example": "他笑了——笑得那么开心。"},
    "……": {"name": "省略号", "usage": "内容省略或话未说完", "example": "天上的星星真多啊……"},
    "·": {"name": "间隔号", "usage": "外国人名或书名各部分之间", "example": "列夫·托尔斯泰"},
}

PAIRS: Tuple[Tuple[str, str, str], ...] = (
    ("“", "”", "引号"),
    ("‘", "’", "单引号"),
    ("（", "）", "括号"),
    ("《", "》", "书名号"),
    ("【", "】", "方括号"),
    ("「", "」", "直角引号"),
)


def _require_text(text: object, name: str = "文本") -> str:
    if not isinstance(text, str):
        raise TypeError("%s 必须是字符串" % name)
    return text


def mark_info(symbol: str) -> Dict[str, str]:
    """查询单个标点的名称、用法和例句。"""
    text = _require_text(symbol, "标点").strip()
    if not text:
        raise ValueError("标点不能为空")
    if text not in MARKS:
        raise ValueError("暂不支持标点：%s" % text)
    info = dict(MARKS[text])
    info["symbol"] = text
    return info


def count_marks(text: str) -> Dict[str, int]:
    """统计文本中各类标点的出现次数（只统计已收录的标点）。"""
    content = _require_text(text)
    counts: Dict[str, int] = {}
    for symbol in MARKS:
        amount = content.count(symbol)
        if amount:
            counts[symbol] = amount
    return counts


def check_pairs(text: str) -> List[str]:
    """检查引号、括号、书名号等是否成对，返回中文问题列表。"""
    content = _require_text(text)
    problems: List[str] = []
    for left, right, name in PAIRS:
        left_count = content.count(left)
        right_count = content.count(right)
        if left_count != right_count:
            problems.append(
                "%s不成对：左%s %d 个，右%s %d 个"
                % (name, left, left_count, right, right_count)
            )
    return problems


QUESTIONS: Tuple[Dict[str, object], ...] = (
    {
        "sentence": "你今天怎么没来上学___",
        "answer": "？",
        "choices": ("。", "？", "！", "，"),
        "explain": "疑问句末尾用问号。",
    },
    {
        "sentence": "多么壮观的瀑布啊___",
        "answer": "！",
        "choices": ("。", "？", "！", "；"),
        "explain": "感叹句末尾用感叹号。",
    },
    {
        "sentence": "我们明天去公园春游___",
        "answer": "。",
        "choices": ("。", "？", "！", "、"),
        "explain": "陈述句末尾用句号。",
    },
    {
        "sentence": "我喜欢的水果有苹果___香蕉和梨。",
        "answer": "、",
        "choices": ("，", "、", "；", "："),
        "explain": "并列词语之间用顿号。",
    },
    {
        "sentence": "图书馆里静悄悄的___",
        "answer": "。",
        "choices": ("。", "！", "？", "……"),
        "explain": "陈述句末尾用句号。",
    },
    {
        "sentence": "这朵花真香啊___",
        "answer": "！",
        "choices": ("。", "？", "！", "，"),
        "explain": "感叹句末尾用感叹号。",
    },
    {
        "sentence": "你写完作业了吗___",
        "answer": "？",
        "choices": ("。", "？", "！", "；"),
        "explain": "疑问句末尾用问号。",
    },
    {
        "sentence": "春天来了___小草绿了。",
        "answer": "，",
        "choices": ("、", "，", "；", "。"),
        "explain": "句子内部停顿用逗号。",
    },
    {
        "sentence": "他带来了三样东西___笔、本子和橡皮。",
        "answer": "：",
        "choices": ("，", "；", "：", "、"),
        "explain": "提示下文用冒号。",
    },
    {
        "sentence": "白天读书___晚上写字。",
        "answer": "；",
        "choices": ("，", "；", "：", "。"),
        "explain": "并列分句之间用分号。",
    },
    {
        "sentence": "我读过___西游记》这本书。",
        "answer": "《",
        "choices": ("《", "“", "（", "【"),
        "explain": "书名前面用左书名号。",
    },
    {
        "sentence": "天上的星星真多啊___",
        "answer": "……",
        "choices": ("……", "——", "。", "！"),
        "explain": "内容省略用省略号。",
    },
    {
        "sentence": "他说___“我们出发吧。”",
        "answer": "：",
        "choices": ("，", "：", "；", "、"),
        "explain": "引用别人的话前用冒号。",
    },
    {
        "sentence": "列夫___托尔斯泰是俄国作家。",
        "answer": "·",
        "choices": ("·", "、", "，", "。"),
        "explain": "外国人名各部分之间用间隔号。",
    },
    {
        "sentence": "请你把窗户关上___",
        "answer": "。",
        "choices": ("。", "？", "！", "；"),
        "explain": "语气平缓的祈使句末尾用句号。",
    },
    {
        "sentence": "你是三年级的学生吗___",
        "answer": "？",
        "choices": ("。", "？", "！", "，"),
        "explain": "疑问句末尾用问号。",
    },
    {
        "sentence": "他笑了___笑得那么开心。",
        "answer": "——",
        "choices": ("——", "……", "；", "、"),
        "explain": "解释说明可用破折号。",
    },
    {
        "sentence": "请把书放在桌子上___",
        "answer": "。",
        "choices": ("。", "？", "！", "、"),
        "explain": "语气平缓的祈使句末尾用句号。",
    },
)


def make_quiz(count: int = 5, seed: Optional[int] = None) -> List[Dict[str, object]]:
    """生成练习题，选项顺序与题目顺序都可复现。"""
    if isinstance(count, bool) or not isinstance(count, int):
        raise TypeError("题目数量必须是整数")
    if count <= 0:
        raise ValueError("题目数量必须大于 0")
    if count > len(QUESTIONS):
        raise ValueError("题目数量不能超过 %d" % len(QUESTIONS))
    rng = random.Random(seed)
    picked = rng.sample(list(QUESTIONS), count)
    quiz: List[Dict[str, object]] = []
    for item in picked:
        choices = list(item["choices"])  # type: ignore[arg-type]
        rng.shuffle(choices)
        quiz.append(
            {
                "sentence": item["sentence"],
                "answer": item["answer"],
                "choices": choices,
                "explain": item["explain"],
            }
        )
    return quiz


def grade(questions: Sequence[Dict[str, object]], answers: Sequence[str]) -> Dict[str, int]:
    """按顺序批改练习，返回正确数、总数和百分制得分。"""
    if not questions:
        raise ValueError("没有可批改的题目")
    if len(questions) != len(answers):
        raise ValueError("答案数量与题目数量不一致")
    correct = 0
    for question, answer in zip(questions, answers):
        if not isinstance(answer, str):
            raise TypeError("答案必须是字符串")
        if answer.strip() == str(question["answer"]).strip():
            correct += 1
    total = len(questions)
    return {"correct": correct, "total": total, "score": round(correct * 100 / total)}
