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
    line-height: 1.42;
  }

  h1, h2, h3 { margin: 0 0 0.45em 0; }
  h1 { color: #0f172a; font-size: 1.72em; }
  h2 { color: #334155; font-size: 1.24em; }
  h3 { color: #475569; font-size: 1.02em; }

  ul, ol { margin-top: 0.25em; }
  li { margin: 0.16em 0; }

  pre {
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
    font-size: 0.72em;
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

  .tag {
    display: inline-block;
    background: #dbeafe;
    color: #1e40af;
    border-radius: 999px;
    padding: 2px 10px;
    margin-right: 8px;
    font-size: 0.7em;
  }

  .small { font-size: 0.82em; }
  .tiny { font-size: 0.7em; }
  .muted { color: #64748b; }
---

<!-- _paginate: false -->

# 第11-12课时｜工具集成演进：CLI → MCP → Skills
## MBA课程《大模型智能体》

<span class="tag">90分钟</span><span class="tag">讲授 + 案例 + 讨论</span>

- 主题：Agent如何获得"动手能力"——从命令行到协议到技能生态
- 目标：理解三代工具集成范式，掌握选型框架与安全治理

---

# 你将掌握什么

1. 理解工具集成的四代演进逻辑
2. 掌握CLI作为Agent工具接口的原理与优势
3. 读懂MCP协议的架构、能力与工作流
4. 用**Inner Loop / Outer Loop**框架做工具选型
5. 理解Agent Skills的设计哲学与生态现状
6. 识别Skill生态的安全风险与治理方案

---

# 课程地图

| Part | 主题 | 时间 |
|------|------|------|
| 1 | 工具集成的四代演进 | 10 min |
| 2 | CLI/Bash——Agent最自然的工具接口 | 12 min |
| 3 | MCP协议——从"能调用"到"可治理" | 15 min |
| 4 | MCP vs CLI——2026年最热的工具争论 | 12 min |
| 5 | Agent Skills——第四代工具集成 | 15 min |
| 6-9 | 三方对比 + 安全治理 + 展望 + 总结 | 26 min |

---

# 先问一个问题

> Agent能思考、能规划、能对话，但光靠"说"不够——它需要**动手**。

- 查数据库、发消息、跑测试、部署代码、读文件……
- 问题不是"能不能调工具"，而是**怎么调才能规模化、安全化、可治理**

<div class="small muted">这就是本讲要回答的核心问题。</div>

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 1｜工具集成的四代演进

从硬编码到知识驱动

---

# Agent需要工具——这是基本事实

没有工具的Agent = 只能聊天的ChatBot

![augmented-llm](images/augmented-llm.png)

```text
Agent能力 = 推理能力 × 可用工具 × 集成质量
```

- **推理能力**：模型决定
- **可用工具**：生态决定
- **集成质量**：架构决定 ← 本讲重点

---

# 四代演进：一张图看全

```text
第一代: 硬编码API        每个工具单独写集成代码
  │                      M个Agent × N个工具 = M×N连接器
  ▼
第二代: CLI/Bash         Unix哲学：小工具 + 管道组合
  │                      LLM天然擅长，零schema开销
  ▼
第三代: MCP协议          标准化JSON-RPC，即插即用
  │                      认证集中、结构化输出、可发现
  ▼
第四代: Agent Skills     写文档而非写代码
                         LLM阅读SKILL.md自主学习
```

---

# 第一代：硬编码API——M×N问题

3个Agent × 20个系统 = **60条集成链路**

每条链路都要处理：认证、限流、错误、重试、版本兼容

| 方案 | 接入复杂度 | 维护复杂度 |
|---|---:|---:|
| 各做各的 | M×N | 极高 |
| 统一协议 | M+N | 可控 |

**类比**：USB出现之前，每种设备都有专属接口

---

# 第二代→第四代的核心跃迁

| 代际 | 核心思想 | 接口形式 | Agent学习方式 |
|------|----------|----------|---------------|
| 硬编码API | 写代码集成 | 函数调用 | 预定义 |
| CLI/Bash | Unix哲学 | stdin/stdout | 训练数据 |
| MCP协议 | 标准化协议 | JSON-RPC | Schema发现 |
| Agent Skills | 知识驱动 | Markdown文档 | 阅读理解 |

每一代都在降低集成门槛、提升可扩展性

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 2｜CLI/Bash——Agent最自然的工具接口

为什么LLM天生就会用命令行

---

# CLI的核心思想：Unix哲学

> "Write programs that do one thing and do it well. Write programs to work together."
> — Doug McIlroy, 1978

- **小工具**：每个命令只做一件事（`grep`, `sort`, `wc`）
- **管道组合**：`|` 把输出喂给下一个命令
- **文本流**：一切皆文本，人和机器都能读

这套哲学诞生于1970年代——但在2026年的AI时代，它比以往更重要。

---

# 为什么LLM天然擅长CLI

> "AI has made the CLI more important and powerful."

LLM的训练数据包含**海量Shell用法**：

- Stack Overflow上的命令行问答
- GitHub上的脚本和CI配置
- 技术文档和教程

**结果**：LLM已经"见过"几乎所有常用CLI工具的用法，无需额外学习。

<div class="tiny muted">来源: <a href="https://www.theregister.com/2026/03/11/ai_needs_command_line_interface/">The Register, 2026.03.11</a></div>

---

# CLI在Agent中的工作方式

```text
Agent
  │
  ├─ 1. 决定需要什么信息/操作
  │
  ├─ 2. 构造Shell命令
  │
  ├─ 3. spawn subprocess → 传参数
  │
  ├─ 4. 读取 stdout / stderr
  │
  └─ 5. 解析文本结果 → 继续推理
```

**零握手、零schema、零持久连接**——跑完就走。

---

# 真实案例：一行命令搞定测试

```bash
pytest --tb=short 2>&1 | head -50
```

输出：
```text
FAILED tests/test_auth.py::test_login
  AssertionError: expected 200, got 401
1 failed, 14 passed in 0.43s
```

Agent直接读文本，理解失败原因，修改代码，重新运行。

整个过程**没有加载任何schema，没有消耗额外token**。

---

# CLI的优势

| 优势 | 说明 |
|------|------|
| **零schema开销** | 不需要加载工具定义，省token |
| **训练熟悉度** | LLM见过大量CLI用法，准确率高 |
| **Unix管道** | `cmd1 | cmd2 | cmd3` 天然可组合 |
| **生态广泛** | 几乎所有开发工具都有CLI |
| **调试直观** | 人可以直接在终端复现 |

---

# CLI的局限

| 局限 | 说明 |
|------|------|
| **无认证管理** | 每个工具单独配置凭证 |
| **无审计日志** | 谁调了什么？不知道 |
| **无Schema** | 输出格式因版本/环境而异 |
| **非结构化输出** | 纯文本，解析可能出错 |
| **安全边界弱** | 命令行可以做任何事 |

<div class="small muted">CLI适合"快速迭代"场景，但企业治理需要更多。</div>

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 3｜MCP协议——从"能调用"到"可治理"

AI应用与工具之间的"USB协议"

---

# MCP是什么

MCP（Model Context Protocol）= AI应用与工具之间的**标准化协议**

- Anthropic于2024年11月发布
- 开放标准，不绑定特定LLM
- 目标：让工具连接像USB一样**即插即用**

```text
传统: 每对单独集成 → M×N
MCP:  统一协议层   → M+N
```

---

# MCP三层架构

| 角色 | 典型实例 | 职责 |
|---|---|---|
| **Host** | Claude Desktop, IDE | 管理会话与安全策略 |
| **Client** | Host中的MCP客户端 | 发送JSON-RPC请求 |
| **Server** | GitHub/DB/Filesystem | 暴露标准化能力 |

```text
User → Host (Claude Desktop)
         ├─ Client A ── JSON-RPC ── Server: github
         ├─ Client B ── JSON-RPC ── Server: postgres
         └─ Client C ── JSON-RPC ── Server: filesystem
```

---

# MCP四大能力

| 能力 | 作用 | 示例 |
|---|---|---|
| **Tools** | 可执行的函数 | 创建Issue、发消息 |
| **Resources** | 可读取的数据 | 文件内容、数据库记录 |
| **Prompts** | 预定义提示模板 | 代码审查模板 |
| **Sampling** | Server请求LLM推理 | 复杂链式决策 |

Agent连接Server后，先通过`tools/list`发现可用能力，再通过`tools/call`执行。

---

# MCP工作流（精简）

```text
1. Host ──► Server:  initialize（协商版本+能力）
2. Host ──► Server:  tools/list（发现可用工具）
3. Host ──► Server:  tools/call（执行具体动作）
4. Server ──► Host:  返回结构化JSON结果
5. Host ──► 模型:    推理下一步
```

所有通信基于**JSON-RPC 2.0**——标准、可追踪、便于审计。

---

# MCP Tool调用示例

```json
// Request
{
  "jsonrpc": "2.0", "id": "req-42",
  "method": "tools/call",
  "params": {
    "name": "create_issue",
    "arguments": {"repo": "org/project", "title": "Bug: login 401"}
  }
}

// Response
{
  "jsonrpc": "2.0", "id": "req-42",
  "result": {
    "content": [{"type": "text", "text": "Issue #128 created"}]
  }
}
```

---

# MCP的核心优势

| 优势 | 说明 |
|------|------|
| **认证集中** | Server统一管理OAuth/API Key |
| **结构化输出** | JSON格式，解析无歧义 |
| **工具可发现** | `tools/list` 自动枚举能力 |
| **Session状态** | 支持有状态交互 |
| **安全可审计** | 每次调用可记录、可追溯 |

---

# 传输方式：本地 vs 远程

| 方式 | 适用场景 | 特点 |
|---|---|---|
| **stdio** | 本地进程 | Host拉起子进程，stdin/stdout通信 |
| **HTTP** | 远程服务 | 网络通信，需认证与网关 |

```text
本地: Claude Desktop → spawn mcp-server-github → stdin/stdout
远程: Host → HTTPS → API Gateway → MCP Server Cluster
```

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 4｜MCP vs CLI——2026年最热的工具争论

两者都讲清楚了，现在来比较

---

# 争论的起源

2025年末以来，开发者社区激烈讨论：

> **给AI助手连接工具，该用MCP还是CLI？**

这不是技术信仰问题——而是**场景匹配问题**。

CircleCI给出了最精辟的框架：

> "The CLI vs. MCP question is really a question about **where you are in the development loop**."

<div class="tiny muted">来源: <a href="https://circleci.com/blog/mcp-vs-cli/">CircleCI Blog</a></div>

---

# Inner Loop vs Outer Loop

| | Inner Loop（内循环） | Outer Loop（外循环） |
|---|---|---|
| **做什么** | 写代码→跑测试→改代码 | CI/CD→部署→安全检查 |
| **时间尺度** | 秒～分钟 | 分钟～小时 |
| **关键指标** | **速度** | **可靠性+安全性** |
| **谁控制** | 开发者本人 | 团队/系统 |
| **最佳选择** | **CLI** ✅ | **MCP** ✅ |

**大多数团队最终两者都用。**

---

# Benchmark数据：残酷的事实

### ScaleKit 2026 Benchmark

> **MCP比CLI贵 10–32x**
> （在token消耗和API调用成本上）

<div class="tiny muted">来源: <a href="https://www.scalekit.com/blog/mcp-vs-cli-use">ScaleKit, 2026.03</a></div>

### 浏览器自动化Benchmark

| 维度 | CLI | MCP | 差距 |
|------|-----|-----|------|
| Token效率 | 基准 | **+33%** 消耗 | CLI胜 |
| 任务完成分 | **77**/100 | 60/100 | CLI胜22% |
| 多步调试 | 完成 | context耗尽 | CLI显著胜 |

---

# Context Budget杀手

**真实案例**：GitHub MCP Server一次dump **93个tool** = **55,000 tokens**

你的128K context window，光加载工具schema就用了**43%**。

```text
128K context budget 分配：

███████████████████░░░░░░░░░░░░░░░░░░░░░░  43% MCP Schema
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  
                                            剩余57%给推理+代码+对话

vs CLI: 100%可用于实际工作
```

<div class="tiny muted">来源: Reddit r/ClaudeAI 热帖</div>

---

# 五问决策框架

| 问题 | → CLI | → MCP |
|------|-------|-------|
| 谁控制反馈循环？ | 开发者本人 | 团队/系统 |
| 循环有多紧？ | 高频迭代 | 离散查询 |
| 需要认证外部系统？ | 否 | 是 |
| 输出格式要求？ | 纯文本即可 | 需结构化JSON |
| 个人还是团队？ | 个人工作流 | 团队共享 |

---

# 真相：不是二选一

> "最常见的错误是把传输选择当成架构决策——'We're a CLI shop'或'We're an MCP shop'是错误的抽象层级。"

**混合方案才是正解**：

```text
CLI包装MCP后端：
  ┌─────────┐      ┌─────────────┐      ┌──────────┐
  │  Agent   │─CLI─►│ 轻量CLI封装  │─API─►│ MCP后端  │
  └─────────┘      └─────────────┘      └──────────┘
  
  对Agent：零schema开销，CLI体验
  对后端：统一认证、审计、结构化
```

正如CircleCI总结："Stop treating this as either/or and start matching the tool to the loop."

---

# 行业标准化动向

**NIST 2026.02**：启动 AI Agent Standards Initiative

- 正在制定Agent工具交互的安全与互操作标准
- MCP和CLI都在讨论范围内
- 目标：建立工具调用的安全基线与审计要求

**信号**：工具协议不再是"社区玩具"，已进入国家标准视野。

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 5｜Agent Skills——第四代工具集成

不是给Agent写代码接口，而是写文档

---

# 从MCP vs CLI到Skill

CLI和MCP解决的是**"怎么调工具"**

Skill解决的是**"怎么教Agent做事"**

```text
传统Plugin:  代码 → 代码接口 → 固定执行路径

Agent Skill: SKILL.md → LLM阅读理解 → LLM自己决定如何调用
```

**革命性**：非程序员也能创建Skill——写Markdown即可。

---

# SKILL.md结构详解

```yaml
---
name: deploy
description: Deploy the application to production.
  Use when the user says "deploy" or "ship it".
disable-model-invocation: true    # 只能手动触发
allowed-tools: Bash, Read         # 限制可用工具
context: fork                     # 子Agent隔离执行
---

## Deploy Procedure

1. **Pre-flight**: Run `npm test`, ensure all pass
2. **Build**: Run `npm run build`
3. **Deploy**: Run `./scripts/deploy.sh production`
4. **Verify**: Run smoke tests, if fail → rollback
```

---

# Frontmatter配置

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | Skill名称 = `/slash-command` |
| `description` | string | Agent据此判断何时使用 |
| `disable-model-invocation` | bool | `true` = 只能用户手动触发 |
| `allowed-tools` | list | 限制Skill可使用的工具集 |
| `context` | string | `fork` = 在子Agent中执行（隔离） |

Agent遵循 [AgentSkills.io](https://agentskills.io) 开放标准，跨Claude Code、OpenClaw等工具通用。

---

# Skill目录结构

```text
my-skill/
├── SKILL.md           # 核心说明文件（必须）
├── scripts/
│   └── validate.sh    # Agent可执行的脚本
├── references/
│   └── api-docs.md    # 参考文档
└── examples/
    └── sample.md      # 示例输出
```

Agent先读SKILL.md理解"做什么、怎么做"，再调用脚本执行。

---

# 三种存储层级

| 层级 | 路径 | 作用范围 | 典型场景 |
|------|------|----------|----------|
| **Enterprise** | managed settings | 组织全员 | 合规检查、安全策略 |
| **Personal** | `~/.claude/skills/` | 个人所有项目 | 工作流偏好 |
| **Project** | `.claude/skills/` | 仅当前项目 | 构建、测试、部署 |

优先级：**Enterprise > Personal > Project**

同名冲突时，高优先级覆盖低优先级。

---

# 内置强力Skill

| Skill | 功能 | 亮点 |
|-------|------|------|
| **`/simplify`** | 审查代码，并行3个review Agent | 多Agent协作 + 聚合修复 |
| **`/batch`** | 编排**5-30个Agent**并行修改 | 每个在独立git worktree |
| **`/loop`** | 定时重复执行prompt | 类似cron |

> `/batch` 是Skill能力的巅峰——一个SKILL.md编排数十个并行Agent，全部通过Markdown描述实现。

<div class="tiny muted">来源: <a href="https://code.claude.com/docs/en/skills">Claude Code Skills Docs</a></div>

---

# Skill生态系统

| 生态 | 状态 |
|------|------|
| **ClawHub** | **2,857+ skills**（2026.03），CLI一键安装 |
| **AgentSkills.io** | 跨工具开放标准 |
| **anthropics/skills** | Anthropic官方仓库 |
| **Google gws** | CLI + MCP + Skills三合一（100+ Skills） |

**关键趋势**：Skill不是某一家的私有概念——它正在成为行业通用标准。

---

# Progressive Disclosure 解决 Context Rot

[Context Rot](https://research.trychroma.com/context-rot)：模型性能随context填满而下降

| 方式 | 启动加载 | Token消耗 |
|------|----------|-----------|
| MCP schema-on-connect | 所有Server全量加载 | 10个Server = **数千tokens** |
| Skill按需加载 | 仅名称+简短描述 | 10个Skill = **几百tokens** |

```text
Skill的Progressive Disclosure:
  启动 → 只加载名称和描述（几十tokens）
  需要 → Agent读取完整SKILL.md（按需）
  完成 → 结果压缩，释放context
```

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 6｜CLI vs MCP vs Skill 三方对比

一页看清三种范式

---

# 三方对比表

| 维度 | CLI | MCP Server | Agent Skill |
|------|-----|------------|-------------|
| **本质** | 命令行程序 | 结构化API服务 | 知识文档 + 脚本 |
| **接口** | stdin/stdout | JSON-RPC | Markdown文件 |
| **上下文成本** | ~零 | 高（schema加载） | 低（按需加载） |
| **创建难度** | 需编程 | 中等（实现协议） | 低（写Markdown） |
| **认证** | 手动/每次配 | 集中管理 | 依赖底层工具 |
| **输出格式** | 自由文本 | 结构化JSON | Agent理解后整合 |
| **适合场景** | 快速迭代 | 外部系统集成 | 工作流定义 |

---

# 选型建议

```text
什么时候用什么？

CLI:   Agent已经知道怎么用的工具 + 快速本地操作 + 不需要schema
MCP:   连接外部SaaS（GitHub/Slack/DB）+ 需要认证和审计
Skill: 定义操作流程 + 教Agent处理特定任务 + 扩展"知识"
```

**最佳实践**：三者混合使用

- Skill定义"做什么"（SOP）
- Skill内部调用CLI做"快操作"
- 涉及外部系统时走MCP

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 7｜安全与治理——Skill生态的暗面

![OpenAI Agent安全Guardrails架构](images/openai-guardrails.png)

当"任何人都能发布代码执行能力"时会发生什么

---

# Lakera安全审计：触目惊心

审计了 **4,310个** Agent Skill → 深度分析 **221个**：

| 风险类型 | 占比 | 说明 |
|----------|------|------|
| OAuth过度授权 | **70.1%** | 请求权限远超实际需要 |
| 命令注入模式 | **43.4%** | 用户输入直接拼接到shell |
| 确认恶意软件 | **44个** Skill | 累计 **12,559+** 下载 |
| 无沙箱隔离 | **100%** | 直接访问文件系统和网络 |

<div class="tiny muted">来源: <a href="https://www.lakera.ai/blog/the-agent-skill-ecosystem-when-ai-extensions-become-a-malware-delivery-channel">Lakera Security Research, 2026</a></div>

---

# 攻击模式：ClawHavoc恶意软件

```text
攻击链:
  1. 发布看似正常的Skill到ClawHub
  2. SKILL.md中嵌入Base64编码的payload
  3. Agent执行时: echo "base64..." | base64 -d | bash
  4. 连接C2服务器（命令控制中心）
  5. 部署Atomic Stealer → 窃取浏览器密码、SSH密钥、钱包
```

**44个确认恶意Skill**，被安装了**12,559次以上**。

---

# 与成熟生态对比

| 生态 | 审核机制 | 权限控制 | 沙箱 |
|------|----------|----------|------|
| 浏览器扩展 | Chrome Web Store审核 | 权限声明 | 有 |
| App Store | Apple人工审核 | 权限弹窗 | 强 |
| npm/PyPI | 无审核 | 无 | 无 |
| **Agent Skills** | **无审核** | **无** | **无** |

Agent Skill生态本质上是**分布式代码执行平台**——但治理水平停留在早期npm。

---

# 治理建议：安全分层模型

| 层级 | 建议 |
|---|---|
| **L0 只读** | 搜索、查询 → 自由使用 |
| **L1 低影响写入** | 创建草稿、添加备注 → 需日志 |
| **L2 业务影响** | 发消息、修改数据 → 需审批 |
| **L3 高风险** | 删除、资金、权限变更 → **必须人工确认** |

**三条底线**：

1. 不安装未审计的Skill
2. 生产环境Skill必须代码审查
3. 建立Skill的version pinning + 变更通知

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 8｜展望与趋势

工具协议的终局在哪里

---

# 工具协议的终局：三层架构

```text
┌─────────────────────────────────────────────┐
│  社会层: 信任、声誉、治理                     │
│  (NIST标准、Skill审计、安全评级)              │
├─────────────────────────────────────────────┤
│  协作层: Agent-to-Agent通信                   │
│  (Google A2A协议、任务委托、能力协商)          │
├─────────────────────────────────────────────┤
│  工具层: Agent-to-Tool连接                    │
│  (MCP + CLI + Skills)                        │
└─────────────────────────────────────────────┘
```

我们今天讲的是**工具层**——但协作层和社会层正在快速发展。

---

# 趋势1：Context Engineering成为核心能力

> "The trend is to let LLMs themselves control context engineering."
> — Harrison Chase, LangChain CEO

**从"全量加载"到"按需加载"**：

- MCP的schema-on-connect → **lazy loading**
- Skill的Progressive Disclosure已经走在前面
- 未来：Agent自己决定加载哪些工具

---

# 趋势2：动态工具发现

当前：连接时加载所有schema → context bloat

未来：

```text
Agent: "我需要查GitHub issue"
  → 动态发现GitHub MCP Server
  → 只加载 issue 相关的 3 个 tool schema
  → 用完释放

而不是一次性加载 93 个 tool = 55,000 tokens
```

CircleCI已经观察到部分MCP实现开始支持这种模式。

---

# 趋势3：工具生态的网络效应

```text
更多Skill → 更多Agent使用 → 更多开发者创建Skill
     ↑                                    │
     └────────────────────────────────────┘
```

- ClawHub从0到2,857+ skills只用了不到一年
- Google gws将CLI+MCP+Skills三合一
- **赢家通吃的逻辑**：谁的工具生态最丰富，谁的Agent最强大

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 9｜总结

---

# 核心概念回顾

| 概念 | 一句话 |
|------|--------|
| **M×N问题** | 没有标准协议，集成成本指数增长 |
| **CLI** | LLM天然擅长，零开销，适合快速迭代 |
| **MCP** | 标准化协议，认证集中，适合企业治理 |
| **Inner/Outer Loop** | CLI适合内循环，MCP适合外循环 |
| **Agent Skill** | 写文档教Agent，非程序员也能创建 |
| **Context Rot** | Skill用按需加载解决schema膨胀 |
| **安全治理** | 70%过度授权，44个恶意软件——不能裸奔 |

---

# MBA洞察

> **Skill是AI Agent时代的SOP。**

传统企业用SOP文档管理知识——谁的SOP好，谁的执行力强。

AI企业用Skill管理Agent能力——**谁能更快把业务知识编码成Skill，谁就让AI更有效服务客户。**

三个战略问题：

1. 你的核心业务流程，能写成Skill吗？
2. 你的团队，谁来维护这些Skill？
3. 你的Skill生态，有安全治理吗？

---

# 课后作业（建议2小时）

1. 选一个业务流程（如客服质检、销售周报）
2. 输出一份A4方案：
   - 哪些环节用CLI，哪些用MCP，哪些用Skill
   - 写一个SKILL.md草案
   - 安全治理方案（权限分层 + 审计策略）
3. 可选：实现一个最小Demo并录屏5分钟

---

# 延伸阅读

## 核心资源
- [CircleCI: MCP vs CLI for AI-native development](https://circleci.com/blog/mcp-vs-cli/)
- [ScaleKit: MCP vs CLI Benchmarking](https://www.scalekit.com/blog/mcp-vs-cli-use)
- [Claude Code: Extend Claude with Skills](https://code.claude.com/docs/en/skills)
- [Lakera: Agent Skill Ecosystem Security](https://www.lakera.ai/blog/the-agent-skill-ecosystem-when-ai-extensions-become-a-malware-delivery-channel)

## 协议与标准
- [MCP官方文档](https://modelcontextprotocol.io/introduction)
- [AgentSkills.io — 开放标准](https://agentskills.io)
- [NIST AI Agent Standards Initiative](https://www.nist.gov/)

## 生态
- [ClawHub — Skill市场](https://clawhub.com)
- [Anthropic Skills仓库](https://github.com/anthropics/skills)
- [Context Rot研究](https://research.trychroma.com/context-rot)

---

# Q&A

## 从"会调用工具"到"会建设能力平台"

谢谢大家。

<div class="small">下一步建议：把课堂作业直接作为你团队的PoC启动文档。</div>
