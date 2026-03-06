---
marp: true
theme: default
paginate: true
size: 16:9
backgroundColor: "#f5f5f7"
color: "#1f2937"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');
  

  section {
    font-family: 'PingFang SC', 'Hiragino Sans GB', 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
    background: #f5f5f7;
    color: #1f2937;
    padding: 46px 62px;
    line-height: 1.45;
  }

  h1, h2, h3 { margin: 0 0 0.45em 0; }
  h1 { color: #0f172a; font-size: 1.7em; }
  h2 { color: #334155; font-size: 1.25em; }
  h3 { color: #475569; font-size: 1.0em; }

  ul, ol { margin-top: 0.3em; }
  li { margin: 0.18em 0; }

  pre {
    background: #1e293b;
    color: #e2e8f0;
    background: #1e293b;
    color: #e2e8f0;
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 0.58em;
    line-height: 1.4;
  }
  pre code {
    background: transparent;
    color: #e2e8f0;
    padding: 0;
  }
  code {
    background: #dbeafe;
    color: #1e3a8a;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 0.9em;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.70em;
  }

  th {
    background: #cbd5e1;
    color: #0f172a;
    border: 1px solid #94a3b8;
    padding: 6px 8px;
  }

  td {
    background: #ffffff;
    border: none;
    padding: 6px 8px;
  }

  a { color: #2563eb; text-decoration: underline; }

  .muted { color: #64748b; font-size: 0.85em; }
  .small { font-size: 0.82em; }
  .tiny { font-size: 0.70em; }
  .tag {
    display: inline-block;
    background: #dbeafe;
    color: #1e40af;
    border-radius: 999px;
    padding: 2px 10px;
    margin-right: 8px;
    font-size: 0.72em;
  }
  .card {
    background: #ffffff;
    border: none;
    border-radius: 12px;
    padding: 12px 14px;
  }
---

<!-- _paginate: false -->

# 第13-14课时｜大模型智能体：走向 LLM OS
## OpenClaw 深度案例与企业实战

<span class="tag">90分钟</span><span class="tag">讲授 + 演示 + 动手</span><span class="tag">60+页完整版</span>

- 主线：从"聊天机器人"到"AI操作系统"
- 平台：OpenClaw（多Agent、多Skill、多Channel）

---

# 课时目标（完成后你将能）

- 解释 Karpathy 提出的 **LLM OS** 愿景
- 用"操作系统类比"理解 Agent 平台核心能力
- 画出 OpenClaw 的 6 层架构并解释数据流
- 完成本地安装、模型接入、Channel 接入
- 配置 Skills 与 Memory，并运行 CEO 多Agent协作
- 用企业视角评估落地价值、成本和治理风险

---

# 课程地图

1. LLM OS 概念与趋势
2. 操作系统类比：从 CPU 到 Agent 调度
3. OpenClaw 架构全景
4. 安装配置与运行
5. Skills 系统与生态
6. Memory 系统与长期价值
7. 多Agent CEO 模式
8. 企业选型与落地路线

---

# 热身问题

- 为什么"更强模型"并不自动等于"更高生产力"？
- 为什么企业会从"单Agent"转向"Agent组织"？
- 如果把 Agent 平台看作 OS，最核心能力是什么？

> 提示：不是"会聊天"，而是"会持续完成任务"。

---

# Part 1｜LLM OS 概念（Karpathy愿景）

- 关键词：**持续性、可组合、可治理、可扩展**
- 核心判断：AI 能力从"工具"升级为"基础设施"
- 类比：就像当年从"单机程序"走向"互联网平台"

---

# 从应用到系统：三阶段演进

| 阶段 | 典型形态 | 核心能力 | 主要限制 |
|---|---|---|---|
| 2022-2023 | Chatbot | 对话问答 | 无长期状态 |
| 2024-2025 | Agent App | 工具调用 | 场景孤岛 |
| 2025+ | LLM OS | 多Agent + 持久化 + 编排 | 需要工程化治理 |

---

# Karpathy 的信号

> "I think we'll increasingly have something that looks like an LLM OS."
> - Andrej Karpathy

- 不是一句口号，而是路线图
- 重点从"模型能力"转向"系统能力"
- 产业机会在 **系统层（OS层）** 而非单点功能层

---

# 为什么现在是 LLM OS 时间窗？

- 模型能力跨过"可用阈值"
- Tool Calling / MCP 标准逐步成型
- 企业开始要求：审计、权限、SLA、成本可控
- 人机协作场景从"回答"变为"执行"

---

# 企业采纳率与预算迁移（2026课堂观察）

| 指标 | 2025 | 2026E | 管理含义 |
|---|---:|---:|---|
| 企业已上线至少1个Agent流程占比 | 31% | 47% | 采纳从试点走向部门级常态 |
| AI预算中"应用/编排层"占比 | 22% | 36% | 预算从底模试验迁移到流程落地 |
| 已建立ROI看板的企业占比 | 18% | 41% | 管理层从"概念验证"转向"经营复盘" |

<div class="tiny muted">数据口径：课堂整理自公开行业调查与厂商年度报告（Gartner/IDC/云厂商企业AI白皮书）交叉估算；时间戳：2026-02；"2026E"为课堂估算值，非单一机构官方预测。</div>

---

# LLM OS 的定义（课堂版）

**LLM OS = 让智能体在真实世界中"长期、安全、可协作"运行的系统软件层。**

包含四个最小要素：
- 运行时：会话、上下文、状态管理
- 能力层：工具、数据、外设、网络
- 组织层：多Agent分工与调度
- 治理层：权限、安全、审计、成本控制

---

# 误区澄清：LLM OS ≠ 更大的 Prompt

- 不是"把系统提示写得更长"
- 不是"把工具都塞给一个 Agent"
- 不是"跑一个 cron + API 就叫 OS"

LLM OS 关注的是：
- 生命周期管理（启动、运行、恢复、退出）
- 资源管理（tokens、工具预算、并发）
- 可观测与可治理（日志、审计、回放）

---

# 操作系统类比总览

| 传统 OS | LLM OS 对应 |
|---|---|
| CPU | LLM 推理引擎 |
| RAM | Context + Working Memory |
| File System | Knowledge & Documents |
| Process/Thread | Agent/Subagent |
| Syscall | Tool Calling / MCP |
| Scheduler | Planner/Orchestrator |
| Permission | Tool & Data Access Policy |
| Shell/GUI | 自然语言 + 多Channel界面 |

---

# 类比1：CPU → LLM（算力与推理）

- CPU 执行指令；LLM 执行"语义指令"
- CPU 有时钟频率；LLM 有 tokens/s 与 latency
- CPU 有 ISA；LLM 有 prompt + tool schema 接口

工程启示：
- 任务拆解比"盲目上大模型"更重要
- 模型混用（小模型路由）是成本关键

---

# 类比2：RAM → 上下文窗口 + 工作记忆

- RAM 快速但有限；上下文窗口同样昂贵且有限
- 页替换对应：摘要、压缩、检索重建
- 内存泄漏对应：prompt 膨胀与无效上下文堆积

```text
策略：短期上下文（会话） + 中期摘要（任务） + 长期记忆（文件/向量）
```

---

# 类比3：文件系统 → 知识与事实存储

- 文件系统承载持久化状态
- Agent 时代的"文件系统"包含：
  - markdown 规则文件（SOUL/USER/MEMORY）
  - 项目目录（代码、文档、数据）
  - 外部知识库（向量库/企业文档）

---

# 类比4：进程模型 → 多Agent协作

- 进程隔离：不同 agent 拥有不同职责与权限
- 线程并行：多个子任务可并发推进
- 父子关系：CEO spawn 子Agent，结果回传

```text
Main Agent = 调度者
Subagent = 专业执行者
Verifier = 质量守门员
```

---

# 类比5：系统调用 → Tool Calling / MCP

- 应用程序通过 syscall 访问系统能力
- Agent 通过工具协议访问外部能力
- MCP 价值：统一接口、降低耦合、提升可移植性

推荐阅读：
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

# 类比6：权限系统 → 安全边界

- OS 有用户/组/ACL；Agent 平台有 tool scopes
- 最小权限原则同样适用
- 高风险动作需"人工确认"

```yaml
policy:
  file_write: allow
  shell_exec: ask
  network_external: allowlist
  delete_recursive: deny
```

---

# 类比7：调度器 → Planner 与 Orchestrator

- OS 调度 CPU 时间片
- LLM OS 调度：模型、工具、Agent、时间预算
- 目标：在成本、时延、质量之间求 Pareto 最优

---

# 类比8：Shell/GUI → 自然语言入口

- 传统 CLI：命令 + 参数
- LLM CLI：意图 + 约束 + 上下文
- 多Channel = 多前端，共享同一"后端大脑"

---

# 小结：为什么"OS类比"有价值？

- 帮我们避免"玩具级 Agent"思维
- 强迫我们关注可运营能力（SRE + Sec + FinOps）
- 让企业讨论从"模型谁更强"转向"系统谁更稳"

---

# Part 2｜OpenClaw：AI-Native Personal OS

- 定位：**开源、可自托管、可扩展** 的智能体操作系统
- 核心卖点：多Agent + 多Channel + Skills + Memory + Node网络
- 场景：个人效率、团队协作、企业私有化

---

# OpenClaw 一句话架构

```text
Channels → Gateway → Session Runtime → Agent Orchestration → Tools/Skills → Node Network
```

- 上层负责交互
- 中层负责会话与决策
- 下层负责执行与连接真实世界

---

# 六层架构总览

1. Node Network（节点网络）
2. Capability Layer（能力层）
3. Agent Layer（智能体层）
4. Session Layer（会话层）
5. Gateway（网关层）
6. Channel Layer（接入层）

---

# Layer 1｜Node Network（节点网络）

- 统一连接 Mac / iPhone / Server / Raspberry Pi
- 让"能力就近执行"：摄像头、麦克风、文件、局域网服务
- 支持跨设备任务协同与故障切换

```text
Laptop(编排) + HomeServer(后台任务) + Phone(移动入口)
```

---

# Layer 2｜Capability Layer（能力层）

- 工具总线：`read/write/edit/exec/process/subagents`
- 外部能力：Browser、Camera、Email、Calendar、Drive
- 规则：工具是"可控系统调用"，不是无限权力

---

# Layer 3｜Agent Layer（智能体层）

- Main Agent（CEO）：理解需求、分解任务、汇总交付
- Subagents：Researcher / Coder / Verifier / Ops...
- 关键设计：角色清晰、上下文隔离、输出契约明确

---

# Layer 4｜Session Layer（会话层）

- 每个请求拥有会话上下文
- 管理短期记忆、权限边界、工具绑定
- 支持中断恢复、持续任务、日志追踪

---

# Layer 5｜Gateway（网关层）

- 消息路由与身份识别
- 连接各类 Channel 协议
- 负责限流、重试、异常隔离

---

# Layer 6｜Channel Layer（接入层）

- 飞书、Telegram、Discord、WhatsApp、CLI...
- 价值：用户在哪，AI 就在哪
- 企业价值：兼容存量沟通平台，降低变革阻力

---

# 端到端请求流（一次任务如何跑）

```text
用户(飞书) -> Gateway -> Main Agent
Main Agent -> 判断复杂度 -> spawn Coder
Coder -> 调用 tools/skills -> 产出结果
Main Agent -> 审核汇总 -> 回复用户
日志/记忆 -> Session + Workspace 持久化
```

---

# OpenClaw 的"可解释性"优势

- Agent 规则是可读文件（Markdown）
- 执行动作可审计（工具调用日志）
- 结果可追溯（子任务链路）

> 对 MBA 管理者最重要：**可管理，而不是魔法黑箱**。

---

# 部署模式

| 模式 | 适用对象 | 优点 | 代价 |
|---|---|---|---|
| 本地单机 | 个人/课堂 | 快速上手 | 可靠性有限 |
| 局域网多节点 | 小团队 | 资源整合 | 维护复杂度上升 |
| 企业私有化 | 中大型企业 | 合规与可控 | 运维与治理成本 |

---

# 课堂案例：CEO模式任务分派

任务：输出《行业AI竞品周报》

- CEO：拆分为"信息收集 / 结构化分析 / 可视化生成"
- Researcher：抓取与摘要
- Analyst：结构化比较与结论
- Designer：转成可汇报文档
- Verifier：事实核验与来源检查

---

# Part 3｜安装与配置（从0到可运行）

- 目标：15分钟内跑通一个最小可用实例
- 路径：安装 CLI → 初始化 workspace → 配置模型 → 启动 gateway

---

# 安装前检查清单

- macOS / Linux 环境（推荐最新稳定版）
- Node.js 20+（课堂环境可用更高版本）
- 可访问的模型提供商 API Key
- 至少一个目标 Channel（CLI 也可）

---

# 快速安装（示例流程）

```bash
# 1) 安装（根据官方文档为准）
npm install -g @openclaw/cli

# 2) 验证
openclaw --version
openclaw help
```

官方入口：
- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)

---

# 初始化工作空间

```bash
openclaw init
```

创建后的关键目录：
- `SOUL.md`：人格与行为边界
- `USER.md`：用户画像与偏好
- `MEMORY.md`：长期记忆摘要
- `projects/`：任务工程内容

---

# Workspace 为什么是核心资产？

- Agent 不再是"远端不可控服务"，而是"可迁移数字员工"
- 文件即策略：可版本管理、可审计、可回滚
- 可复用：一个成熟 workspace 可复制到团队

---

# config.yaml 关键字段

```yaml
models:
  primary: openai/gpt-5.2
  fallback: kimi/k2.5

channels:
  feishu:
    enabled: true
  telegram:
    enabled: false

gateway:
  rate_limit_per_min: 60
  log_level: info
```

---

# 环境变量与密钥管理

- 不把密钥写进仓库
- 使用 `.env` + 密钥管理器
- 对生产环境启用分环境隔离

```bash
OPENAI_API_KEY=...
FEISHU_APP_ID=...
FEISHU_APP_SECRET=...
```

---

# 接入模型提供商

- 主模型：高质量复杂任务
- 备用模型：降级兜底
- 路由策略：按任务类型和预算选择

推荐思路：
- 研究/规划：大模型
- 批处理/提取：中小模型

---

# 接入 Channel（以飞书/Telegram 为例）

- 飞书：企业内部协作场景
- Telegram：外部实时沟通场景
- CLI：开发测试和自动化场景

直达：
- [飞书开放平台](https://open.feishu.cn/)
- [Telegram BotFather](https://t.me/BotFather)

---

# 启动与运维命令（必须记住）

```bash
openclaw gateway status
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
```

> 运维第一原则：先看 status，再谈问题。

---

# 常见故障排查矩阵

| 症状 | 可能原因 | 排查动作 |
|---|---|---|
| 无法回复消息 | Gateway 未启动 | `openclaw gateway status` |
| 调用模型失败 | API Key 配置错误 | 检查 `.env` |
| Channel 无消息 | webhook/token 错误 | 平台控制台重置并重试 |
| 执行超时 | 任务拆分不足 | 减小单任务粒度 |

---

# 生产环境加固清单

- 网关鉴权与IP限制
- 最小工具权限原则
- 高风险动作 `ask` 确认
- 日志脱敏与保留周期策略
- 关键任务告警（失败/延迟/成本异常）

---

# 动手试试①：5分钟跑通本地 OpenClaw

目标：完成安装并获取版本号

1. 按文档安装 CLI
2. 执行 `openclaw --version`
3. 截图保存到课堂群

平台直达：
- [OpenClaw 安装文档](https://docs.openclaw.ai)
- [OpenClaw GitHub 仓库](https://github.com/openclaw/openclaw)

---

# 动手试试②：配置一个可用 Channel

目标：让 Agent 能从至少一个入口接收消息

建议路径：
- 企业协作：飞书
- 个人测试：Telegram

平台直达：
- [飞书开放平台控制台](https://open.feishu.cn/)
- [Telegram BotFather（创建机器人）](https://t.me/BotFather)
- [OpenClaw Channels 文档](https://docs.openclaw.ai)

---

# Part 4｜Skills 系统：能力插件化

- Skill = 可热加载能力模块
- 组成：`SKILL.md` + 脚本 + 配置
- 价值：从"单体 Agent"到"能力市场"

---

# Skill 的生命周期

1. 发现（Discover）
2. 安装（Install）
3. 调用（Invoke）
4. 更新（Update）
5. 下线（Deprecate）

工程要点：每一步都要可追踪、可回滚。

---

# 内置 Skill 能力图谱

- 办公自动化：notes/reminders/calendar/mail
- 开发协作：github/coding-agent
- 信息获取：web_search/web_fetch/summarize
- 生活服务：weather/imh/chat channels

> 业务价值：把"零散API接入成本"一次性产品化。

---

# 自定义 Skill 目录结构

```text
skills/
  my-skill/
    SKILL.md
    scripts/
      run.sh
    config.yaml
```

- `SKILL.md` 负责"让 Agent 会用"
- `scripts/` 负责"真正执行动作"
- `config.yaml` 负责"环境参数与策略"

---

# Skill 路由机制（Agent 如何知道要用谁）

- 首先看用户意图
- 然后匹配 skill 描述
- 若冲突，选择"最具体"技能
- 若无匹配，回退基础工具或请求澄清

---

# Skill 的边界与安全

- Skill ≠ 任意脚本执行
- 必须在工具权限模型内运行
- 对 destructive 操作设置确认门槛

```yaml
skill_policy:
  allow_network: true
  allow_write: scoped
  require_confirmation:
    - delete
    - publish
```

---

# ClawHub：技能生态网络效应

- 类似"App Store for Agent Skills"
- 社区贡献 + 版本分发 + 更新机制
- 企业可维护私有技能市场

平台直达：
- [ClawHub](https://clawhub.com)

---

# 动手试试③：安装并调用一个 Skill

目标：安装 `github` 或 `weather`，完成一次调用

建议步骤：
1. 搜索技能
2. 安装技能
3. 用自然语言触发

平台直达：
- [ClawHub 技能市场](https://clawhub.com)
- [GitHub CLI 文档](https://cli.github.com/)
- [OpenClaw Skills 文档](https://docs.openclaw.ai)

---

# 动手试试④：创建你的第一个 Mini Skill

任务：做一个"日报模板生成器"skill

最低要求：
- 一个 `SKILL.md`
- 一个脚本文件
- 一条示例调用语句

平台直达：
- [Markdown 语法指南](https://www.markdownguide.org/)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [Shell 脚本入门](https://www.gnu.org/software/bash/manual/)

---

# Part 5｜Memory 系统在 LLM OS 中的角色

> 📌 **回顾**：记忆原理已在L7-8详细讲解。本节聚焦**LLM OS视角的记忆架构**。

**LLM OS 记忆 vs 传统应用记忆**：

| 维度 | 传统应用 | LLM OS |
|------|----------|--------|
| 存储 | 数据库/缓存 | 文件系统 + 向量库 |
| 格式 | 结构化Schema | 自然语言 + Markdown |
| 检索 | SQL查询 | 语义搜索 + 规则 |
| 更新 | 显式写入 | Agent自主判断 |

---

# OpenClaw 的文件化记忆设计

```text
workspace/
├── USER.md          # 用户画像（静态）
├── MEMORY.md        # 长期摘要（高密度）
├── SOUL.md          # Agent人格定义
└── memory/
    └── 2026-02-27.md  # 每日工作日志
```

**核心理念**：记忆 = 可版本控制的Markdown文件

优势：可审计、可回滚、可协作、零锁定

---

# 动手试试⑤：给你的 Agent 建一份"用户画像"

目标：让 Agent 在新会话中仍保持一致风格

操作建议：
1. 编辑 `USER.md`
2. 添加 5 条稳定偏好（沟通风格、专业领域、时区等）
3. 新开会话验证效果

平台直达：
- [OpenClaw 文档](https://docs.openclaw.ai)

---

# Part 6｜多Agent CEO模式实战

> 📌 **回顾**：多Agent协作模式已在L9-10详细讲解。本节聚焦**OpenClaw CEO模式的具体实现**。

**L9-10 vs L13-14 侧重点**：

| L9-10 | L13-14 |
|-------|--------|
| 四种协作模式理论 | OpenClaw具体实现 |
| 框架对比 | CEO模式配置与运行 |
| 通用设计原则 | 角色定义与任务模板 |

---

# OpenClaw CEO 模式架构

```text
用户 → Main(CEO) → 任务分解
                    ├→ Researcher: 调研
                    ├→ Coder: 实现  
                    ├→ Verifier: 审核
                    └→ 结果整合 → 用户
```

**核心配置文件**：
- `AGENTS.md` — 角色定义与调度规则
- `TEAM.md` — 团队成员与专长

---

# 任务分解模板（CEO常用）

```markdown
## 任务目标
## 成功标准
## 子任务列表
## 角色分配
## 时间预算
## 交付格式
```

> 没有成功标准，就没有可管理交付。

---

# 子Agent 输出契约（示例）

```json
{
  "task_id": "R-2026-0227-01",
  "summary": "三点结论...",
  "sources": ["https://..."],
  "confidence": 0.82,
  "next_actions": ["..."]
}
```

结构化输出 = 可组合、可审计、可追溯

---

# 实战链路示例：生成董事会简报

```text
CEO: 拆分任务
  -> Researcher: 行业事实
  -> Analyst: 经营指标分析
  -> Coder: 自动生成图表
  -> Verifier: 事实/格式审查
CEO: 最终整合并给出行动建议
```

---

# 动手试试⑥：运行一个 CEO 多Agent流程

目标：完成"调研 + 产出 + 审核"三段式任务

建议任务：
- "调研某AI公司近90天动态，输出一页简报"

平台直达：
- [OpenClaw 文档](https://docs.openclaw.ai)
- [Google Scholar](https://scholar.google.com/)
- [GitHub Trending](https://github.com/trending)

---

# Part 7｜企业应用：从 Demo 到经营指标

- 关键问题：能不能稳定创造业务价值？
- 判断标准：效率、质量、风险、成本、可扩展

---

# 企业场景1：投研与行业分析

- 自动抓取新闻、公告、研报
- 生成结构化对比与风险提示
- 人类分析师聚焦高价值判断

产出：
- 日报 / 周报 / 事件预警 / 深度专题

---

# 企业场景2：研发组织效能

- PR审查、文档生成、Issue分诊
- 多Agent覆盖"编码-验证-发布"链路
- 缩短需求到交付周期

---

# 企业场景3：运营与客服

- 多渠道统一接待
- 客诉分类与工单流转
- 记忆系统保证客户体验连续性

---

# OpenClaw 与替代方案对比（课堂版）

| 维度 | OpenClaw | 通用Chat工具 | 单功能Agent平台 |
|---|---|---|---|
| 多Agent编排 | 强 | 弱 | 中 |
| 可自托管 | 强 | 弱 | 中 |
| 技能扩展 | 强 | 中 | 中 |
| 治理可控 | 强 | 中 | 弱 |
| 开箱即用 | 中 | 强 | 中 |

<div class="tiny muted">评价维度权重（课堂版）：治理可控30% + 多智能体编排25% + 可自托管20% + 技能扩展15% + 开箱即用10%。如以"快速试点"为目标，可上调开箱即用权重。</div>

---

# ROI 计算框架（管理层可用）

```text
ROI = (效率收益 + 质量收益 + 风险降低收益 - 实施总成本) / 实施总成本
```

三情景测算（用于预算评审）：

| 情景 | 效率收益系数 | 质量/风险收益系数 | 成本上浮系数 | 适用场景 |
|---|---:|---:|---:|---|
| 乐观 | 1.3x | 1.2x | 0.9x | 流程标准化高、组织协同成熟 |
| 基准 | 1.0x | 1.0x | 1.0x | 大多数企业首年落地 |
| 保守 | 0.7x | 0.8x | 1.2x | 数据质量一般、变革阻力较大 |

成本项：
- 模型费用
- 开发与运维
- 治理与培训

收益项：
- 人时节省
- 周期缩短
- 错误率下降

---

# 30-60-90 天落地路线

- 30天：选一个高频低风险场景 PoC
- 60天：接入真实流程，建立监控与审计
- 90天：扩展多Agent与多渠道，形成可复制模板

---

# 风险清单与治理动作

| 风险 | 典型表现 | 治理动作 |
|---|---|---|
| 幻觉 | 事实错误 | Verifier + 来源校验 |
| 权限滥用 | 越权执行 | 最小权限 + 人工确认 |
| 成本失控 | token 暴涨 | 模型路由 + 预算阈值 |
| 组织阻力 | 不愿采纳 | 小步快跑 + 可见收益 |

---

# MBA岗位映射：你在LLM OS时代的角色

| 岗位方向 | 可放大的核心价值 | 典型交付物 |
|---|---|---|
| 咨询（战略/数字化） | 把AI能力转化为可执行转型路线 | 路线图、治理蓝图、ROI测算 |
| 投研（一级/二级） | 用多智能体提升信息处理速度与证据密度 | 行业跟踪报告、风险雷达 |
| 运营（增长/客服/供应链） | 用流程自动化提升人效与SLA | 自动化流程看板、异常处置机制 |
| 产品（B端/SaaS） | 设计可复用Agent能力并嵌入业务系统 | PRD、能力矩阵、实验复盘 |

---

# 课堂复盘：我们今天建立了什么能力？

- 概念：LLM OS 不是口号，而是系统工程
- 架构：理解 OpenClaw 6 层设计与请求流
- 工程：掌握安装、配置、排障关键路径
- 组织：会设计 CEO 多Agent协同流程
- 商业：能评估企业落地与 ROI

---

# 课堂小测（3题）

1. 为什么说 Memory 是"持续价值"的核心？
2. CEO 模式里 Verifier 的职责是什么？
3. 企业选型时，为什么"治理能力"比"模型分数"更重要？

---

# 课后作业（下周提交）

请设计一个你所在行业的 LLM OS 方案（3页）：

1. 业务场景与痛点
2. Agent 组织结构图 + Skill 清单
3. ROI 与风险治理计划

加分项：
- 给出可运行最小原型链接或截图

---

# 延伸学习资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [ClawHub 技能市场](https://clawhub.com)
- [Marp 官方文档](https://marp.app/)

---

# 一页清单：你可以立即做的 5 件事

1. 安装 OpenClaw 并初始化 workspace
2. 接入一个模型 + 一个 Channel
3. 安装 1 个 Skill 并触发调用
4. 定义 USER.md 与 MEMORY.md 模板
5. 设计一个 CEO 多Agent最小流程

---

# 致谢 & Q&A

**从"会聊天"到"会工作"，差的是系统，不是幻觉。**

欢迎课后交流：
- 你的行业场景
- 你的组织约束
- 你的落地路径

<!-- _paginate: false -->
