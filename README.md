# 🤖 大模型智能体：从原理到实践

> **上海交通大学安泰经济与管理学院 MBA 课程**  
> 与 [OpenClaw](https://openclaw.ai) 合作开发

---

## 👨‍🏫 讲师

**温颖** 副教授  
上海交通大学 人工智能学院  
🔗 [yingwen.io](https://yingwen.io)

**温睦宁** 助理研究员  
上海交通大学 人工智能学院  

## 👨‍🏫 助教

**王雅娟**
上海交通大学 安泰经济与管理学院  

---

## 📚 课程简介

本课程面向 MBA 学员，系统介绍大语言模型（LLM）与 AI Agent 的核心原理、技术架构与商业应用。通过理论讲解与动手实践相结合，帮助学员理解 AI Agent 如何重塑企业工作流程，并具备评估、选型和落地 AI Agent 解决方案的能力。

### 课程特色

- 🎯 **商业导向**：聚焦 AI Agent 在企业场景的实际应用
- 🌐 **前沿视野**：涵盖 MCP 协议、LLM OS 等最新技术趋势
- 🇨🇳 **本土视角**：深入分析中国 AI 产业格局与机遇

---

## 📅 课程大纲

### Day 1：基础与架构

| 课时 | 主题 | 幻灯片 | 讲义 |
|------|------|--------|------|
| L1-2 | 大语言模型基础 | [MD](slides/day1-lesson1-2-llm-basics.md) · [PDF](output/pdf/slides/day1-lesson1-2-llm-basics.pdf) | [讲义](lecture-notes/L1-2-LLM-Basics-大语言模型基础.md) · [PDF](output/pdf/lecture-notes/L1-2-LLM-Basics-大语言模型基础.pdf) |
| L3-4 | 工作流与 RAG | [MD](slides/day1-lesson3-4-workflow.md) · [PDF](output/pdf/slides/day1-lesson3-4-workflow.pdf) | [讲义](lecture-notes/L3-4-Workflow-RAG-流程与检索增强.md) · [PDF](output/pdf/lecture-notes/L3-4-Workflow-RAG-流程与检索增强.pdf) |
| L5-6 | Agent 架构 | [MD](slides/day1-lesson5-6-agent.md) · [PDF](output/pdf/slides/day1-lesson5-6-agent.pdf) | [讲义](lecture-notes/L5-6-Agent-智能体设计与实现.md) · [PDF](output/pdf/lecture-notes/L5-6-Agent-智能体设计与实现.pdf) |
| L7-8 | 记忆与工具 | [MD](slides/day1-lesson7-8-memory-tools.md) · [PDF](output/pdf/slides/day1-lesson7-8-memory-tools.pdf) | [讲义](lecture-notes/L7-8-Memory-Tools-记忆系统与工具编排.md) · [PDF](output/pdf/lecture-notes/L7-8-Memory-Tools-记忆系统与工具编排.pdf) |

### Day 2：进阶与落地

| 课时 | 主题 | 幻灯片 | 讲义 |
|------|------|--------|------|
| L9-10 | 多智能体系统 | [MD](slides/day2-lesson9-10-multi-agent.md) · [PDF](output/pdf/slides/day2-lesson9-10-multi-agent.pdf) | [讲义](lecture-notes/L9-10-MultiAgent-多智能体系统设计.md) · [PDF](output/pdf/lecture-notes/L9-10-MultiAgent-多智能体系统设计.pdf) |
| L11-12 | MCP 与工具生态 | [MD](slides/day2-lesson11-12-mcp.md) · [PDF](output/pdf/slides/day2-lesson11-12-mcp.pdf) | [讲义](lecture-notes/L11-12-MCP-工具集成标准.md) · [PDF](output/pdf/lecture-notes/L11-12-MCP-工具集成标准.pdf) |
| L13-14 | LLM OS | [MD](slides/day2-lesson13-14-llm-os.md) · [PDF](output/pdf/slides/day2-lesson13-14-llm-os.pdf) | [讲义](lecture-notes/L13-14-LLM-OS-智能体操作系统.md) · [PDF](output/pdf/lecture-notes/L13-14-LLM-OS-智能体操作系统.pdf) |
| L15-16 | 商业落地 | [MD](slides/day2-lesson15-16-business.md) · [PDF](output/pdf/slides/day2-lesson15-16-business.pdf) | [讲义](lecture-notes/L15-16-Business-商业落地与未来展望.md) · [PDF](output/pdf/lecture-notes/L15-16-Business-商业落地与未来展望.pdf) |

### 补充材料

- [课程概览](slides/course-overview.md) · [PDF](output/pdf/slides/course-overview.pdf)
- [课程大纲](SYLLABUS.md) · [PDF](output/pdf/SYLLABUS.pdf)
- [延伸阅读清单](READING-LIST.md) · [PDF](output/pdf/READING-LIST.pdf)

---

## 📂 目录结构

```
├── slides/              # 📽️ 课程幻灯片 (Marp格式)
├── lecture-notes/       # 📖 详细讲义
├── output/pdf/          # 📄 PDF 输出文件
├── SYLLABUS.md          # 课程大纲
└── READING-LIST.md      # 延伸阅读清单
```

---

## 🚀 快速开始

幻灯片使用 [Marp](https://marp.app/) 格式编写，可直接用 VS Code + Marp 插件预览：

```bash
# 安装 Marp CLI
npm install -g @marp-team/marp-cli

# 生成 PDF
marp slides/day1-lesson1-2-llm-basics.md --pdf -o output.pdf
```

---

## 🤝 合作方

### OpenClaw

[OpenClaw](https://openclaw.ai) 是一个开源的 Personal AI 基础设施项目，让每个人都能拥有自己的 AI Agent。

**核心特性：**

- 🦞 **多智能体系统** — CEO Agent 统领多个专业 Agent（研究、编码、投资、运维等），实现复杂任务的自动分解与协作
- 🧩 **Skills 生态** — 模块化的能力扩展系统，通过 Skill 包快速赋予 Agent 新技能（日历管理、邮件处理、智能家居控制等）
- 🔌 **MCP 协议支持** — 兼容 Model Context Protocol，无缝集成 MCP 工具生态
- 💾 **本地记忆系统** — 基于向量搜索的长期记忆，支持 Hybrid Search、MMR 去重、时间衰减等高级特性
- 📱 **全平台接入** — 统一接入 Telegram、飞书、Discord、WhatsApp、iMessage 等消息平台
- 🏠 **隐私优先** — 数据本地存储，支持本地 Embedding 模型，无需上传云端
- ⚡ **Coding Agent 集成** — 原生支持 Codex CLI、Claude Code 等编码工具，实现代码生成与自动化开发

本课程的多智能体系统设计、MCP 集成、LLM OS 等内容深度结合 OpenClaw 的架构设计与实践经验。

---

## 📖 延伸资源

- [OpenClaw 文档](https://docs.openclaw.ai) — 技术文档与教程
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) — 开源代码
- [ClawHub](https://clawhub.com) — Skills 社区与分享平台

---

## 📜 许可证

本课程材料采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可证。

---

<div align="center">

**上海交通大学安泰经济与管理学院 · 上海交通大学人工智能学院 × OpenClaw**

*让每个人都能拥有自己的 AI Agent*

</div>
