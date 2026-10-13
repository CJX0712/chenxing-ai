# -*- coding: utf-8 -*-
"""
ChenXing-AI 闭环自检（零重写 · 集大成）
校验：总数=1024 / ID 唯一 / 格式规范 / 四元组完整 / 16 类各 64 / 三端一致
作者：晨星
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "layer10.json")
INDEX = os.path.join(ROOT, "index.html")
LAYER10 = os.path.join(ROOT, "layer10")

def fail(msg):
    print("FAIL:", msg); sys.exit(1)

def main():
    if not os.path.exists(DATA): fail("data/layer10.json 缺失")
    j = json.load(open(DATA, encoding="utf-8"))
    E = j["entries"]
    n = len(E)
    if n != 1024: fail(f"总数应为 1024，实际 {n}")

    ids = [e["id"] for e in E]
    if len(set(ids)) != n: fail("存在重复 ID")
    for i in ids:
        if not re.fullmatch(r"L10-C\d{2}-\d{2}", i): fail(f"ID 格式非法: {i}")

    for key in ("input", "action", "output", "invariant"):
        if any(not e.get(key) for e in E): fail(f"存在缺失字段: {key}")

    from collections import Counter
    cc = Counter(e["category_code"] for e in E)
    if len(cc) != 16: fail(f"类别数应为 16，实际 {len(cc)}")
    for k, v in cc.items():
        if v != 64: fail(f"类别 {k} 应为 64 条，实际 {v}")

    # 三端一致：HTML 内嵌总数
    html_ok = f'"total": {n}' in open(INDEX, encoding="utf-8").read()
    if not html_ok: fail("index.html 内嵌总数不一致")

    # markdown 文件齐全
    import glob
    md = glob.glob(os.path.join(LAYER10, "L10-C*.md"))
    if len(md) != 16: fail(f"layer10 markdown 应为 16 份，实际 {len(md)}")

    print(f"PASS ✅ 微指令总数={n} ｜ ID 唯一={len(set(ids))} ｜ 16 类×64 ｜ 四元组完整 ｜ HTML/MD/JSON 三端一致")

if __name__ == "__main__":
    main()
