# ChenXing-AI ✦ 十层分解架构 · 世界最优解集大成

> **作者：晨星 | 原则：零重写 · 集大成 · 闭环交付**

锻造世界顶级 AI 的工程路径不是从零造轮子，而是：**每一层都站在世界顶级成果之上——直接复用、组合、超越。**

本仓库是一份**可执行蓝图**：

- `docs/ARCHITECTURE.md` —— 十层架构完整定义，每层映射当前世界最优开源方案
- `layer10/` —— 第十层 **1024 项微指令级操作**全量规范（16 类别 × 64 条），每条含验证不变量
- `index.html` —— 单文件零依赖架构控制台，浏览器直接打开即可浏览/搜索全部 1024 条
- `scripts/build.py` —— 从单一数据源（JSON）生成 markdown 与 HTML，保证三端一致
- `scripts/selftest.py` —— 闭环自检：校验微指令总数 = 1024、ID 唯一、每条含不变量

## 十层架构 × 零重写映射（速览）

| 层 | 职责 | 世界最优解（直接复用） | 本项目动作 |
|---|---|---|---|
| L1 | 算力与硬件调度 | CUDA · NCCL · Triton | 组合调度策略 |
| L2 | 数值与张量核心 | PyTorch · JAX/XLA · GGML | 选型+基准 |
| L3 | 模型与算法 | transformers · FlashAttention · MoE | 组合超越 |
| L4 | 推理服务 | vLLM · SGLang · Ollama | 部署方案 |
| L5 | 训练与微调 | DeepSpeed · FSDP · LoRA/QLoRA | 流水线 |
| L6 | 智能体编排 | LangGraph · AutoGen · MCP | 编排规范 |
| L7 | 检索与记忆 | FAISS · Qdrant · GraphRAG | 混合检索 |
| L8 | 数据与质量 | HF Datasets · Great Expectations | 质量门禁 |
| L9 | 可观测与安全 | OpenTelemetry · Llama Guard | 全链路监控 |
| L10 | **微指令运行时** | ——（本层为本项目原创贡献） | **1024 项规范** |

完整映射（含许可证、选型理由、超越点）见 `docs/ARCHITECTURE.md`。

## 快速开始

```bash
git clone https://github.com/CJX0712/chenxing-ai.git
cd chenxing-ai
python scripts/selftest.py   # 闭环自检：1024 项全绿
python scripts/build.py      # 从数据源重建 layer10/ 与 index.html
```

浏览器打开 `index.html` 即为完整架构控制台。

## 验证不变量（闭环交付承诺）

- 微指令总数恒等于 **1024**，ID 唯一且格式 `L10-C{cc}-{nn}`
- 每条微指令必含：输入 / 动作 / 输出 / **验证不变量**（可机检）
- `selftest.py` 全绿 = 文档、数据、HTML 三端一致

## License

MIT © 2026 晨星 (ChenXing)
