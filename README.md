# 🤖 大模型智能体 2026春

> **上海交通大学 安泰经济管理学院**  
> MBA 课程 · 与 [OpenClaw](https://openclaw.ai) 合作开发  
> 最后更新：2026-03-14

---

## 👨‍🏫 讲师

**温颖** 副教授 · 上海交通大学 人工智能学院 · [yingwen.io](https://yingwen.io)  
**温睦宁** 助理研究员 · 上海交通大学 人工智能学院

**助教**：王雅娟 · 上海交通大学 安泰经济与管理学院

---

## 📚 课程简介

两天密集课程（16课时），面向 MBA 学员，系统讲解大语言模型与 AI Agent 的**原理、架构与商业落地**。

### 你将学到

- LLM 核心原理（Transformer → 推理模型 → GPT-5.4/Claude Opus 4.6 Agent模型）
- 工作流设计（Pipeline/Routing/Parallelization + RAG）
- Agent 架构（ReAct/反思/规划 + 记忆 + 工具）
- 多 Agent 协作（共识机制、OMAO 实战挑战）
- 工具生态（CLI → MCP → Agent Skills，安全治理）
- Harness Engineering（Agent = Model + Harness）
- 商业落地（Services as Software、AI-native 组织、$1→$4800 经济学）

### 课程特色

- 🎯 **商业导向**：每个技术点都配 MBA 视角的商业洞察
- 🔥 **前沿内容**：整合 2026 年 3 月最新的硅谷趋势（Harness Engineering、MCP vs CLI 争论、红杉万亿美元论）
- 📊 **数据驱动**：引用 Anthropic 2026 报告、$OneMillion-Bench、Lakera 安全审计等一手数据
- 🏗️ **案例丰富**：OpenAI 0 代码实验、Cursor $50B、Zapier 800 Agent 等真实案例

---

## 📅 课程大纲

### Day 1：基础与架构（4 × 90min）

| 课时 | 主题 | 页数 | 核心内容 |
|------|------|------|----------|
| **L0** | 安装OpenClaw🦞 & Token订阅 | N/A | [OpenClaw官网](https://openclaw.ai/) |
| **L1-2** | [大语言模型基础](slides/day1-lesson1-2-llm-basics.md) | 87页 | Transformer → GPT-5/Claude 4.6/Gemini 3.1，推理模型，MoE，Token Pricing, Prompt/Context Engineering |
| **L3-4** | [工作流与 RAG](slides/day1-lesson3-4-workflow.md) | 77页 | Anthropic 5种工作流模式（含官方架构图），RAG/GraphRAG/Agentic RAG |
| **L5-6** | [智能体架构与设计](slides/day1-lesson5-6-agent.md) | 82页 | ReAct/反思/规划，OpenAI+Anthropic 官方 Agent 定义，自主时长 14.5h |
| **L7-8** | [记忆系统与工具编排](slides/day1-lesson7-8-memory-tools.md) | 65页 | 三层记忆架构，Context Rot，AGENTS.md，MCP/CLI/Skill 预览 |

### Day 2：进阶与落地（4 × 90min）

| 课时 | 主题 | 页数 | 核心内容 |
|------|------|------|----------|
| **L9-10** | [多智能体协作与共识机制](slides/day2-lesson9-10-multi-agent.md) | 51页 | 4种协作模式，共识机制（Voting/Debate/Consensus），OMAO 七缺口，实战瓶颈 |
| **L11-12** | [CLI · MCP · Skills 工具生态](slides/day2-lesson11-12-mcp.md) | 63页 | CLI→MCP→Skills 四代演进，MCP vs CLI（10-32x 成本差），Lakera 安全审计 |
| **L13-14** | [LLM OS 与 Harness Engineering](slides/day2-lesson13-14-llm-os.md) | 59页 | Harness Engineering（OpenAI/LangChain/Anthropic），OpenClaw 架构，Big Model vs Big Harness |
| **L15-16** | [AI Agent 商业革命与未来](slides/day2-lesson15-16-business.md) | 58页 | $1→$4800 Agent 经济学，红杉 Services as Software，AI-native 组织，技术趋势 |

> 共 **542 页**，含 **15 张**来自 Anthropic 和 OpenAI 的官方架构图

---

## 📂 仓库结构

```
├── slides/                     # 📽️ 课程幻灯片 (Marp Markdown)
│   ├── course-overview.md      # 课程总览
│   ├── day1-lesson*.md         # Day 1 四讲
│   ├── day2-lesson*.md         # Day 2 四讲
│   ├── images/                 # Anthropic + OpenAI 官方图
│   └── assets/images/          # Lilian Weng 论文图
├── .marprc.yml                 # Marp 配置
├── package.json                # 依赖
└── README.md
```

---

## 🔧 本地编译

### 安装依赖

```bash
npm install -g @marp-team/marp-cli
```

### 编译为 PDF

```bash
marp slides/day1-lesson1-2-llm-basics.md --pdf --allow-local-files -o output.pdf
```

### 编译为 HTML

```bash
marp slides/day1-lesson1-2-llm-basics.md --html --allow-local-files -o output.html
```

### 编译为 PPTX

```bash
marp slides/day1-lesson1-2-llm-basics.md --pptx --allow-local-files -o output.pptx
```

### 批量编译

```bash
for md in slides/day*.md; do
  name=$(basename "$md" .md)
  marp "$md" --pdf --allow-local-files -o "output/${name}.pdf"
done
```

---

## 📖 参考资料

### 官方技术博客（课程核心引用）

| 来源 | 文章 | 用于 |
|------|------|------|
| Anthropic | [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | L3-4, L5-6, L9-10 |
| Anthropic | [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | L13-14 |
| Anthropic | [2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf) | L13-14, L15-16 |
| OpenAI | [A Practical Guide to Building AI Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | L5-6, L9-10 |
| OpenAI | [Harness Engineering](https://openai.com/index/harness-engineering/) | L13-14 |
| LangChain | [The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) | L13-14 |
| Sequoia | [Services: The New Software](https://sequoiacap.com/article/services-the-new-software/) | L15-16 |
| CircleCI | [MCP vs CLI for AI-native Development](https://circleci.com/blog/mcp-vs-cli/) | L11-12 |
| Lakera | [Agent Skill Ecosystem Security](https://www.lakera.ai/blog/the-agent-skill-ecosystem-when-ai-extensions-become-a-malware-delivery-channel) | L11-12 |
| Latent Space | [Is Harness Engineering Real?](https://www.latent.space/p/ainews-is-harness-engineering-real) | L13-14 |

### 学术论文

- [Voting or Consensus? Decision-Making in Multi-Agent Debate](https://arxiv.org/abs/2502.19130) — ACL 2025
- [$OneMillion-Bench](https://arxiv.org/abs/2603.07980) — Agent 经济价值评估
- [Auditing Multi-Agent LLM Reasoning Trees](https://arxiv.org/abs/2602.09341)

### 产品与生态

- [OpenClaw](https://openclaw.ai) · [ClawHub Skills](https://clawhub.com) · [MCP Protocol](https://modelcontextprotocol.io) · [AgentSkills.io](https://agentskills.io)

---

## 📜 License

本课程材料仅供教学使用。

---

*上海交通大学 · 人工智能学院 · 2026 春*
