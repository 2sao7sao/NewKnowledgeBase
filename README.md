<img src="assets/banner.png" alt="banner" width="100%" />

# EvolveKB — Skills‑Driven Knowledge Base (Execution‑First)

[![Status](https://img.shields.io/badge/status-WIP-yellow)](./README.md)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

> 把“知识”变成 **可执行的技能**。  
> 不止做 recall/rerank，而是沉淀为 **可复用的流程（playbook）与过程（procedure）**，在门控下持续演进。

---

## TL;DR

- 传统 RAG 更擅长“找资料”，但不擅长“把资料变成可复用流程”。
- **EvolveKB** 选择 execution‑first：先让知识可执行，再谈召回增强。
- 你可以选择 **引用 / 消化 / 转化 / 演进** 四种用法，让知识按你的方式参与推理。

---

## Why (问题是什么)

传统 RAG 的主路径是：query → recall → rerank → LLM 参考候选内容生成。工程成熟，但常见问题：

- **理解浅**：更像“片段附近拼接”，而非结构化理解与沉淀。
- **multi‑hop 易断链**：chunk 切分导致跨段逻辑断裂。
- **可用性不足**：GraphRAG / RAPTER 等提升联结，但核心仍是“更好的召回”。

如果你想要的是“可复用的流程、可执行的步骤”，传统 RAG 还不够。

---

## What (我们提供什么)

**EvolveKB = 把知识升级为技能**：

- **Playbook**：面向一个 intent 的完整流程
- **Procedure**：可复用的原子能力
- **Gate**：质量控制与演进门控
- **Settings**：让同一套知识在不同策略下表现不同

---

## How (系统怎么跑)

1. 用户提问 / 上传资料
2. 读取 settings：选择知识使用模式（reference / digest / transform / evolve）
3. 路由到对应 playbook
4. playbook 调用 procedures 分步执行
5. 每一步在 gate 下生成可验证中间产物
6. 若开启 evolve：提出变更 → gate 审核 → 合并为知识库新版本

---

## Knowledge usage modes（四种用法）

| Mode | 作用 | 典型场景 |
| --- | --- | --- |
| Reference | 仅引用资料，不改写知识库 | 快速问答 / 保守模式 |
| Digest | 结构化摘要后再回答 | 需要吸收与总结 |
| Transform | 转为 procedures/playbooks | 构建可复用技能 |
| Evolve | 允许提出变更并门控合并 | 持续演进知识库 |

---

## Repository structure

```text
skills/
  <skill-name>/
    SKILL.md        # YAML frontmatter + markdown body
scripts/
  validate.py       # repo-level checks (symlinks, size limits, etc.)
  skill_validate.py # validates skills: schema, naming, playbook/procedure refs
  run.py            # minimal runner: route by intent -> execute playbook/procedures
AGENT.md            # gate rules / slimming constraints / authoring rules
USER.md             # user-facing usage guidance
```

---

## Quick start

```bash
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/run.py --intent compare_frameworks --question "对比 GraphRAG 和 md-knowledge 的差异"
```

---

## Settings

你可以用 settings 文件控制“知识如何参与推理与产出”：

```bash
python scripts/run.py \
  --intent compare_frameworks \
  --question "..." \
  --settings settings/default.yaml
```

建议配置字段（planned）：

- `knowledge_mode`: reference | digest | transform | evolve
- `gate_level`: 0..3（越高越严格）
- `auto_evolve`: true/false
- `max_skill_md_bytes`: 50000
- `allowed_tools`: [ ... ]
- `memory_policy`: conservative | balanced | aggressive

---

## Skill format (SKILL.md)

每个 skill 由两部分构成：

1. YAML frontmatter（强校验：结构化元信息）
2. Markdown body（人类可读：保持精简，长资料下沉）

### Playbook example

```yaml
---
name: compare-frameworks
description: Compare two frameworks and output a structured decision memo.
allowed-tools: []
metadata:
  kind: playbook
  intent: compare_frameworks
  steps:
    - id: normalize
      uses: normalize-question
    - id: compare
      uses: compare-frameworks
---
```

### Procedure example

```yaml
---
name: normalize-question
description: Normalize user question into structured requirements.
allowed-tools: []
metadata:
  kind: procedure
  inputs:
    question: string
  outputs:
    normalized_question: string
---
```

---

## Gates should evolve

- 初期：人类定义 Gate（可控、快速落地）
- 中期：模型在 Gate 下演进知识，产出失败样例/边界案例
- 后期：系统用这些案例升级 Gate 与 Schema（新增字段、增强校验、优化 slimming 策略、加入回归测试）

目标：让 gate 从“人工规则”变成“反馈驱动的规则”。

---

## Roadmap

1. ✅ README / docs 可读性
2. ⏭️ 引入 settings 文件，用户可选知识使用模式
3. ⏭️ 上 CI：每次提交自动跑 `python scripts/validate.py`
4. ⏭️ 扩展 skill schema（version/owner/tags/examples）+ 更严格校验
5. ⏭️ 引入可插拔执行层（tool/llm executor）
6. ⏭️ 加入“gate evolution loop”

---

## Contributing (self workflow)

每次只做一个小改动，保证可回滚：

```bash
git checkout main
git pull
git checkout -b chore/readme-improve

# edit README.md

git add README.md
git commit -m "Improve README"
git push -u origin chore/readme-improve
```

在 GitHub 点 **Compare & pull request** 创建 PR，无误后 Merge。

---

## License

See `LICENSE`.
