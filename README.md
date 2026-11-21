# punctuation

[![CI](https://github.com/eastyou/punctuation/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/punctuation/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

中文标点符号学习工具：规则查询、引号括号配对检查、标点统计和练习单生成。

## 功能

- 收录 16 个常用中文标点，含名称、用法和例句
- 检查引号、单引号、括号、书名号、方括号、直角引号是否成对
- 统计句子中各类标点的出现次数
- 内置 18 道单空练习题，覆盖句号、问号、感叹号、顿号、分号、冒号、书名号、破折号、省略号和间隔号
- 随机抽取题目、打乱选项，支持固定随机种子复现
- 自动批改并生成百分制成绩
- 生成含选项与答案页的单文件 HTML 练习

## 安装

```bash
pip install -e .
```

也可以直接运行 `python -m punctuation`。

## 使用

```bash
punctuation info 。                       # 句号 / 用法 / 例句
punctuation check "他说：“走吧。”"        # 配对检查通过
punctuation check "他说：“走吧。"          # 输出问题并返回退出码 1
punctuation count "苹果、香蕉、梨。"       # 共 3 个标点
punctuation rules                         # 列出全部规则

# 生成 8 道练习
punctuation quiz --count 8 --seed 7 -o examples/sheet.html
```

## 作为库使用

```python
from punctuation import check_pairs, make_quiz, grade

assert check_pairs("他说：“走吧。”") == []
questions = make_quiz(3, seed=1)
answers = [question["answer"] for question in questions]
assert grade(questions, answers)["score"] == 100
```

## 示例

[examples/sheet.html](examples/sheet.html) 是 8 道题的练习页，附参考答案和解析。

## 测试

```bash
python -m unittest discover -s tests -v
```

共 72 项单元测试，覆盖每个标点的信息、配对检查、题目数据一致性、批改逻辑、HTML 转义和命令行退出码。CI 覆盖 Python 3.9 ~ 3.13 与 Linux/macOS/Windows。

## 许可

MIT © 2026 eastyou
