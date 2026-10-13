# -*- coding: utf-8 -*-
"""
ChenXing-AI 单一事实源生成器（零重写 · 集大成）
生成：
  data/layer10.json   —— 1024 条微指令（机器可检）
  layer10/L10-C{cc}.md —— 16 个类别文档
  index.html          —— 单文件零依赖架构控制台
作者：晨星
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
LAYER10 = os.path.join(ROOT, "layer10")

# ---- 16 类别，每类 8 维度 = 128 维度；× 8 操作 = 1024 微指令 ----
CATEGORIES = {
    "01": "数值与张量核心", "02": "算力与硬件调度", "03": "模型与算法",
    "04": "推理服务", "05": "训练与微调", "06": "智能体编排",
    "07": "检索与记忆", "08": "数据质量", "09": "可观测与安全",
    "10": "提示工程", "11": "工具与协议", "12": "缓存与性能",
    "13": "部署运维", "14": "评估基准", "15": "合规许可", "16": "文档交付闭环",
}

DIMS = {
    "01": ["梯度检验(自动微分)", "logsumexp 数值稳定", "Cholesky/病态矩阵求解", "特征分解 Jacobi",
           "SVD 秩截断(Eckart-Young)", "采样分布守恒", "Kahan 求和精度", "量化舍入误差界"],
    "02": ["Triton 核融合", "NCCL 拓扑感知通信", "PagedAttention 显存分页", "3D 并行切分",
           "Roofline 瓶颈判定", "混合精度 AMP", "算子调度器", "功耗-吞吐权衡"],
    "03": ["FlashAttention 替换", "RoPE/YaRN 外推", "MoE 路由与负载", "MLA/共享专家",
           "采样链 top-k/p/min-p", "量化 AWQ/GPTQ", "KV Cache 压缩", "tokenizer 一致性"],
    "04": ["continuous batching", "前缀缓存 RadixAttention", "约束解码 JSON grammar", "推测解码 EAGLE",
           "流式 SSE 输出", "多模型路由", "降级与熔断", "吞吐/时延基准"],
    "05": ["ZeRO/FSDP 切分", "QLoRA 配置", "数据课程排序", "梯度累积与裁剪",
           "checkpoint 断点续训", "DPO 对齐", "评估早停", "灾难性遗忘检测"],
    "06": ["LangGraph 状态图", "检查点回放", "工具 schema 校验", "人在环审批",
           "多智能体消息协议", "重试幂等", "循环终止条件", "失败降级链"],
    "07": ["向量索引 HNSW", "BM25 词法路", "混合融合 RRF", "重排 reranker",
           "GraphRAG 多跳", "记忆写入与衰减", "分块策略", "召回基准 BeIR"],
    "08": ["采集溯源", "清洗规则", "MinHash 去重", "质量门禁 GE",
           "类别平衡审计", "标注一致性 κ", "版本快照 DVC", "数据卡生成"],
    "09": ["OTel trace 埋点", "成本计量", "PII 检测", "prompt-injection 检测",
           "Llama Guard 护栏", "红队用例集", "告警阈值", "事故复盘"],
    "10": ["DSPy 指标编译", "few-shot 选择", "结构化输出模板", "上下文压缩",
           "prompt 版本管理", "A/B 评测", "注入对抗测试", "多语言一致性"],
    "11": ["MCP 服务器接入", "JSON Schema 校验", "权限最小化", "超时与重试",
           "幂等键", "沙箱执行", "速率限制", "协议兼容矩阵"],
    "12": ["KV Cache 复用", "语义缓存", "结果 memoization", "热点预取",
           "性能剖析 cProfile", "内存泄漏检测", "延迟预算分配", "端到端压测"],
    "13": ["容器化封装", "CI/CD 流水线", "蓝绿发布", "回滚脚本",
           "密钥管理", "环境矩阵", "健康检查", "容量规划"],
    "14": ["lm-eval-harness 复跑", "回归基线", "人工抽检协议", "盲测设计",
           "统计显著性 bootstrap", "失败案例分析", "基准防污染", "排行榜记录"],
    "15": ["SBOM 生成", "许可证扫描", "三方归因声明", "模型许可条款",
           "数据许可", "出口合规", "隐私合规", "风险免责声明"],
    "16": ["README 完整性", "可复现脚本", "单文件 HTML 交付", "中文文档规范",
           "API 参考", "变更日志", "署名晨星", "开源发布检查"],
}

# ---- 8 操作类型（每类通用，参数化维度）----
OPS = [
    ("verify", "校验",
     "按世界最优标准复跑「{d}」校验并记录真实数字",
     "校验报告(PASS/FAIL,含量化误差值)",
     "同机复跑两次结果一致，量化误差 ≤ 文档记录阈值"),
    ("benchmark", "基准",
     "为「{d}」构建可复现基准并独立运行 3 次",
     "吞吐/精度基准数字表",
     "三次运行 P50 波动 ≤ 10% 且数值跨机可复现"),
    ("reuse", "复用",
     "检索「{d}」领域当前 SOTA 开源实现并接入既有栈",
     "接入说明 + 功能等价测试",
     "功能等价测试全绿且本动作自写核心代码行数 = 0"),
    ("compose", "组合",
     "将「{d}」最优解与现有管线组合为端到端服务",
     "组合后服务与对接契约",
     "组合后端到端指标 ≥ 各组件单独指标之积的下界"),
    ("optimize", "优化",
     "对「{d}」做性能/精度优化并保留前后对照",
     "优化前后对照表",
     "优化后 ≥ 优化前且完整回归测试全绿"),
    ("harden", "容错",
     "向「{d}」注入故障并验证 SLO 内恢复",
     "故障注入与恢复报告",
     "故障注入后系统在 SLO 内恢复且数据零丢失"),
    ("document", "文档",
     "为「{d}」补齐文档与一键可复制示例",
     "文档 + 可运行示例",
     "示例一键运行成功且输出与文档声明一致"),
    ("surpass", "超越",
     "明确「{d}」超越点并实现，附可复现佐证",
     "超越点基准数字",
     "超越点有可复现基准数字佐证且严格优于基线"),
]

def build_entries():
    entries = []
    for cc, cname in CATEGORIES.items():
        dims = DIMS[cc]
        n = 0
        for di, d in enumerate(dims):
            for oi, (key, olabel, act_t, out_t, inv_t) in enumerate(OPS):
                n += 1
                nn = f"{n:02d}"
                entries.append({
                    "id": f"L10-C{cc}-{nn}",
                    "category_code": cc,
                    "category": cname,
                    "dim": d,
                    "op_key": key,
                    "op": olabel,
                    "name": f"{olabel}·{d}",
                    "input": f"「{d}」现状 / 需求描述",
                    "action": act_t.format(d=d),
                    "output": out_t,
                    "invariant": inv_t.format(d=d),
                    "tags": [cname, d, olabel],
                })
    return entries

def write_json(entries):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "layer10.json"), "w", encoding="utf-8") as f:
        json.dump({"total": len(entries), "generated_by": "晨星",
                   "entries": entries}, f, ensure_ascii=False, indent=2)

def write_markdown(entries):
    os.makedirs(LAYER10, exist_ok=True)
    by_cat = {}
    for e in entries:
        by_cat.setdefault(e["category_code"], []).append(e)
    for cc, cname in CATEGORIES.items():
        path = os.path.join(LAYER10, f"L10-C{cc}.md")
        rows = by_cat[cc]
        lines = [f"# L10-C{cc} · {cname}", "",
                 f"> 类别 {cc}｜共 {len(rows)} 项微指令｜ID 区间 `L10-C{cc}-01` ~ `L10-C{cc}-64`", "",
                 "| ID | 操作 | 微指令 | 输入 | 动作 | 输出 | 验证不变量 |",
                 "|---|---|---|---|---|---|---|"]
        for e in rows:
            lines.append("| `{id}` | {op} | {name} | {input} | {action} | {output} | {invariant} |".format(
                id=e["id"], op=e["op"], name=e["name"], input=e["input"],
                action=e["action"], output=e["output"], invariant=e["invariant"]))
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

HTML_TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ChenXing-AI · 十层架构控制台</title>
<style>
:root{{--bg:#f6f8fb;--card:#fff;--ink:#1a2233;--mut:#64708a;--acc:#2b6cff;--ok:#1aa86b;--line:#e3e8f0;}}
*{{box-sizing:border-box}}
body{{margin:0;font:14px/1.6 -apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink)}}
header{{padding:18px 22px;background:linear-gradient(100deg,#0b1e3f,#15366e);color:#fff}}
header h1{{margin:0;font-size:20px;letter-spacing:.5px}}
header p{{margin:6px 0 0;color:#bcd0ff;font-size:13px}}
.wrap{{max-width:1100px;margin:0 auto;padding:18px 22px 60px}}
.stats{{display:flex;gap:14px;flex-wrap:wrap;margin:16px 0}}
.stat{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;flex:1;min-width:140px}}
.stat b{{display:block;font-size:22px;color:var(--acc)}}
.stat span{{color:var(--mut);font-size:12px}}
.controls{{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0 18px}}
input,select{{padding:9px 12px;border:1px solid var(--line);border-radius:9px;background:var(--card);color:var(--ink);font-size:13px}}
input{{flex:1;min-width:220px}}
.catgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px;margin-bottom:22px}}
.cat{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:11px 13px;cursor:pointer;transition:.15s}}
.cat:hover{{border-color:var(--acc);transform:translateY(-2px)}}
.cat b{{color:var(--acc)}} .cat small{{color:var(--mut);display:block}}
table{{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}}
th,td{{text-align:left;padding:9px 11px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{background:#eef2f9;color:var(--mut);font-weight:600;position:sticky;top:0}}
tr:hover td{{background:#f0f5ff}}
.idc{{font-family:ui-monospace,Menlo,Consolas,monospace;color:var(--acc);white-space:nowrap}}
.pill{{display:inline-block;background:#e9f0ff;color:var(--acc);border-radius:6px;padding:1px 7px;font-size:12px}}
footer{{color:var(--mut);font-size:12px;text-align:center;padding:20px}}
.empty{{padding:30px;text-align:center;color:var(--mut)}}
</style></head>
<body>
<header><h1>✦ ChenXing-AI 十层架构控制台</h1>
<p>零重写 · 集大成 · 闭环交付　|　作者 晨星　|　第十层 1024 项微指令运行时</p></header>
<div class="wrap">
  <div class="stats">
    <div class="stat"><b id="s-total">0</b><span>微指令总数</span></div>
    <div class="stat"><b>16</b><span>类别</span></div>
    <div class="stat"><b>8</b><span>操作类型</span></div>
    <div class="stat"><b>64</b><span>每类条数</span></div>
  </div>
  <div class="catgrid" id="catgrid"></div>
  <div class="controls">
    <input id="q" placeholder="搜索：维度 / 操作 / 关键词（如 量化、MCP、KV）">
    <select id="cat"><option value="">全部类别</option></select>
    <select id="op"><option value="">全部操作</option></select>
  </div>
  <table><thead><tr><th>ID</th><th>操作</th><th>微指令</th><th>输入</th><th>动作</th><th>输出</th><th>验证不变量</th></tr></thead>
  <tbody id="rows"></tbody></table>
  <div class="empty" id="empty" style="display:none">无匹配结果</div>
  <footer>单一事实源 data/layer10.json ｜ 生成 scripts/build.py ｜ 自检 scripts/selftest.py ｜ MIT © 2026 晨星</footer>
</div>
<script>
const DATA = {json};
const E = DATA.entries;
document.getElementById('s-total').textContent = DATA.total;
const cats = {{}}, ops = {{}};
E.forEach(e=>{{cats[e.category_code]=e.category; ops[e.op]=1;}});
const cg = document.getElementById('catgrid');
Object.keys(cats).sort().forEach(cc=>{{
  const n = E.filter(e=>e.category_code===cc).length;
  const d = document.createElement('div'); d.className='cat';
  d.innerHTML = `<b>C${{cc}}</b> <small>${{cats[cc]}}</small><small>${{n}} 项</small>`;
  d.onclick = ()=>{{document.getElementById('cat').value=cc; render();}};
  cg.appendChild(d);
}});
const selC=document.getElementById('cat'), selO=document.getElementById('op');
Object.keys(cats).sort().forEach(cc=>{{const o=document.createElement('option');o.value=cc;o.textContent='C'+cc+' '+cats[cc];selC.appendChild(o);}});
Object.keys(ops).forEach(o=>{{const x=document.createElement('option');x.value=o;x.textContent=o;selO.appendChild(x);}});
function render(){{
  const q=(document.getElementById('q').value||'').toLowerCase();
  const cc=selC.value, op=selO.value;
  const rows=document.getElementById('rows'); rows.innerHTML='';
  let n=0;
  E.forEach(e=>{{
    if(cc&&e.category_code!==cc) return;
    if(op&&e.op!==op) return;
    const hay=(e.id+' '+e.name+' '+e.dim+' '+e.action+' '+e.invariant).toLowerCase();
    if(q&&hay.indexOf(q)<0) return;
    n++;
    const tr=document.createElement('tr');
    tr.innerHTML=`<td class="idc">${{e.id}}</td><td><span class="pill">${{e.op}}</span></td><td>${{e.name}}</td><td>${{e.input}}</td><td>${{e.action}}</td><td>${{e.output}}</td><td>${{e.invariant}}</td>`;
    rows.appendChild(tr);
  }});
  document.getElementById('empty').style.display = n? 'none':'block';
}}
document.getElementById('q').oninput=render; selC.onchange=render; selO.onchange=render;
render();
</script></body></html>"""

def write_html(entries):
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(HTML_TPL.format(json=json.dumps({"total": len(entries), "entries": entries}, ensure_ascii=False)))

if __name__ == "__main__":
    entries = build_entries()
    assert len(entries) == 1024, f"expected 1024, got {len(entries)}"
    write_json(entries)
    write_markdown(entries)
    write_html(entries)
    print(f"OK generated {len(entries)} entries -> data/layer10.json, layer10/*.md, index.html")
