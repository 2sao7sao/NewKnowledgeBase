# NewKnowledgeBase — Skills‑Driven Knowledge Base (Execution‑First)

[![Status](https://img.shields.io/badge/status-WIP-yellow)](./README.md)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

> 一个把“知识”组织成 **可执行技能（skills）** 的知识库框架。  
> 不止做 recall/rerank，而是把知识沉淀为 **可复用的流程（playbook）与过程（procedure）**，并用门控机制推动知识持续演进。

---

## Vision

**Execution‑first**：把知识升级为“可执行技能”，让 agent 在系统内完成理解、梳理、更新、演进，最终从根源产出可用信息，而不是依赖候选池参考。

---

## Star history

![Star History](https://api.star-history.com/svg?repos=2sao7sao/NewKnowledgeBase&type=Date)

---

## Architecture (high‑level)

1. 用户提问 / 上传资料
2. 读取 settings：选择知识使用模式（reference / digest / transform / evolve）
3. 路由到对应 playbook
4. playbook 调用 procedures 分步执行
5. 每一步在 gate 下生成可验证中间产物
6. 若开启 evolve：提出变更 → gate 审核 → 合并为知识库新版本

---

## What problem this solves

传统 RAG 的主路径是：query → recall → rerank → LLM 参考候选内容生成。它工程成熟，但常见问题：

- **知识未被真正理解**：更多是“片段附近拼接”，而非结构化理解与沉淀。
- **multi‑hop 易断链**：chunk 切分导致跨段逻辑断裂。
- **可用性不足**：GraphRAG / RAPTER 等提升联结，但核心仍是“更好的召回”。

本项目选择另一条路线：**先让知识可执行，再谈召回增强**。

---

## Core concepts (4 件事就够用)

### 1) Skill = Playbook / Procedure
- **Playbook**：面向一个 intent 的完整工作流（多步骤）
- **Procedure**：可复用的原子能力（被多个 playbook 调用）

### 2) Knowledge usage modes（用户可选）

| Mode | 作用 | 典型场景 |
| --- | --- | --- |
| Reference | 仅引用资料，不改写知识库 | 快速问答 / 保守模式 |
| Digest | 结构化摘要后再回答 | 需要吸收与总结 |
| Transform | 转为 procedures/playbooks | 构建可复用技能 |
| Evolve | 允许提出变更并门控合并 | 持续演进知识库 |

### 3) Settings Layer（配置层）
把“知识用法 / 门控强度 / 演进策略”从代码和 prompt 中抽离出来，让同一套知识在不同 settings 下呈现不同策略。

### 4) Gates（演进质量控制）
- 结构正确、引用完整、内容瘦身、可回滚、可验证
- Gate 本身也可演进（见 Roadmap）

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
