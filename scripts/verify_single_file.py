#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""情绪树洞 · 单文件自检

检查 index.html 是否仍然是「一个文件、零依赖、零外链」：
  1. 文件存在且体积/行数在预期量级
  2. 没有 <script src> / <link rel=stylesheet> 之类的外部资源
  3. 没有 http(s) 网络地址（XML 命名空间 http://www.w3.org/... 除外）
  4. 没有埋点、第三方 SDK 的痕迹
  5. 5 个 localStorage 键名仍然齐全

用法：
    python scripts/verify_single_file.py
    python scripts/verify_single_file.py path/to/index.html

全部通过返回 0，有问题返回 1。
"""

import io
import re
import sys
import os

STORAGE_KEYS = [
    "coze-mood-tree-v1",
    "coze-mood-users-v1",
    "coze-mood-board-v1",
    "coze-mood-current",
    "mood-theme",
]

# 这些是合法的 XML 命名空间，不会发起请求
NAMESPACE_OK = re.compile(r"http://www\.w3\.org/[A-Za-z0-9/._#-]*")

# 不允许出现的外部资源写法
FORBIDDEN_PATTERNS = [
    (r"<script[^>]+src\s*=", "<script src> 外链脚本"),
    (r"<link[^>]+rel\s*=\s*[\"']stylesheet", "<link rel=stylesheet> 外链样式"),
    (r"@import\s+", "CSS @import"),
    (r"\bfetch\s*\(", "fetch() 网络请求"),
    (r"XMLHttpRequest", "XMLHttpRequest"),
    (r"navigator\.sendBeacon", "sendBeacon 埋点"),
    (r"https?://[^\s\"'<>]+", "http(s) 外部地址（命名空间除外）"),
]

TRACKER_HINTS = ["apmPlus", "code.coze", "volccdn", "coze-coding-badge"]


def fail(msg):
    print("FAIL: " + msg)
    return 1


def main():
    default = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")
    path = sys.argv[1] if len(sys.argv) > 1 else default

    if not os.path.isfile(path):
        return fail("找不到文件：" + path)

    raw = io.open(path, "rb").read()
    size = len(raw)
    text = io.open(path, encoding="utf-8").read()
    lines = text.count("\n") + 1

    errors = []

    # 1. 体积与行数
    print("文件      : " + path)
    print("体积      : {:,} 字节".format(size))
    print("行数      : {:,} 行".format(lines))
    print("字符数    : {:,}".format(len(text)))
    if size < 40_000:
        errors.append("体积偏小（{:,} 字节），可能被截断".format(size))

    # 2. 结构完整性
    for token in ["<!DOCTYPE html>", "<html", "</html>", "<style", "<script", "</script>"]:
        if token.lower() not in text.lower():
            errors.append("缺少结构片段：" + token)

    # 3. 外链与请求
    for pattern, label in FORBIDDEN_PATTERNS:
        hits = []
        for m in re.finditer(pattern, text, re.IGNORECASE):
            snippet = m.group(0)
            if label.startswith("http(s)") and NAMESPACE_OK.fullmatch(snippet):
                continue
            line_no = text.count("\n", 0, m.start()) + 1
            hits.append("第 {} 行 {}".format(line_no, snippet[:60]))
        if hits:
            errors.append("发现{}：{}".format(label, hits[0]))
            for extra in hits[1:5]:
                print("      另有：" + extra)

    # 4. 埋点痕迹
    for hint in TRACKER_HINTS:
        if hint in text:
            errors.append("发现第三方痕迹：" + hint)

    # 5. 存储键
    print()
    print("localStorage 键：")
    for key in STORAGE_KEYS:
        count = text.count(key)
        print("  {:24s} {}".format(key, "OK" if count else "缺失"))
        if count == 0:
            errors.append("缺少存储键：" + key)

    # 6. 关键交互点仍在
    checks = [
        ("switchTab", "面板切换函数"),
        ("data-tab=\"home\"", "树洞 tab"),
        ("maxlength=\"1200\"", "1200 字上限"),
        ("<dialog", "原生弹窗"),
        ("speechSynthesis", "呼吸语音朗读"),
    ]
    print()
    print("关键实现：")
    for token, label in checks:
        ok = token in text
        print("  {:28s} {}".format(label, "OK" if ok else "缺失"))
        if not ok:
            errors.append("缺少实现：" + label)

    print()
    if errors:
        for e in errors:
            print("FAIL: " + e)
        print("\n共 {} 项未通过".format(len(errors)))
        return 1

    print("PASS: 单文件、零依赖、零外链、5 个存储键齐全")
    return 0


if __name__ == "__main__":
    sys.exit(main())
