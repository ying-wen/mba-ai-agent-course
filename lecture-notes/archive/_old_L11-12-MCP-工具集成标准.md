# L11-12 讲义：MCP协议与工具集成

> **课程**: MBA大模型智能体课程  
> **课时**: 第11-12讲（90分钟）  
> **适用**: 讲师备课 / 学生预习与复习  
> **对应Slides**: `slides-marp/day2-lesson11-12-mcp.md`

---

## 本讲核心问题

1. **为什么需要MCP？** 工具集成的痛点是什么？
2. **MCP如何工作？** Host/Client/Server三层架构
3. **Skill是什么？** 与MCP的区别是什么？
4. **如何设计好的工具？** 有哪些原则和反模式？

---

## Part 1：工具集成的痛点

### M×N连接器爆炸

想象你是一家企业的IT负责人：

```
你有 M 个AI应用：
- ChatGPT
- Claude
- 内部Agent
- ...

你有 N 个工具/数据源：
- Slack
- GitHub
- 数据库
- 内部系统
- ...

传统方案：每对都要单独集成
连接器数量 = M × N
```

当M=10，N=20时，你需要维护200个连接器。这是不可持续的。

### 四大痛点

| 痛点 | 表现 | 后果 |
|------|------|------|
| **重复造轮子** | 每个AI应用都重新集成 | 开发成本高 |
| **稳定性差** | 各团队实现质量不一 | 维护成本高 |
| **安全难治理** | 权限分散、审计困难 | 合规风险 |
| **协作成本高** | 接口不统一、文档缺失 | 沟通成本 |

### MCP的解决思路

```
传统: M × N 连接
─────────────────
AI应用1 ──┬── 工具A
          ├── 工具B
          └── 工具C
AI应用2 ──┬── 工具A
          ├── 工具B
          └── 工具C

MCP: M + N 连接
─────────────────
AI应用1 ──┐
AI应用2 ──┼── MCP协议 ──┬── 工具A
AI应用3 ──┘              ├── 工具B
                         └── 工具C
```

**类比**：MCP就像USB协议——在USB出现之前，每种设备都有专属接口；有了USB之后，任何设备都能即插即用。

---

## Part 2：MCP协议原理

### 什么是MCP？

MCP (Model Context Protocol) 是Anthropic于2024年11月发布的开放标准，用于连接AI应用与外部工具/数据。

> **一句话定义**：MCP是AI应用与工具之间的"USB协议"——标准化接口，即插即用。

### 三层架构

```
┌─────────────────────────────────────────────────────┐
│                    MCP 架构                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Host（宿主）                                       │
│  └── Claude Desktop、IDE、你的应用                 │
│      职责：管理生命周期、安全策略                  │
│                                                     │
│  Client（客户端）                                   │
│  └── MCP Client库                                  │
│      职责：与Server通信、协议解析                  │
│                                                     │
│  Server（服务端）                                   │
│  └── GitHub MCP、Slack MCP、自定义MCP             │
│      职责：暴露工具能力、处理请求                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 四大能力

| 能力 | 说明 | 示例 |
|------|------|------|
| **Tools** | 可执行的函数 | 发送消息、创建文件 |
| **Resources** | 可读取的数据 | 文件内容、数据库记录 |
| **Prompts** | 预定义的提示词模板 | 代码审查模板 |
| **Sampling** | Server请求LLM生成 | 高级场景 |

### 工作流程

```
用户: "帮我创建一个GitHub issue"
        │
        ▼
    ┌─────────┐
    │  Host   │  ← Claude Desktop
    └────┬────┘
         │ 1. 识别需要调用GitHub工具
         ▼
    ┌─────────┐
    │ Client  │
    └────┬────┘
         │ 2. 发送JSON-RPC请求
         ▼
    ┌─────────┐
    │ Server  │  ← GitHub MCP Server
    └────┬────┘
         │ 3. 调用GitHub API
         │ 4. 返回结果
         ▼
    用户看到: "已创建Issue #123"
```

### 传输方式

| 方式 | 适用场景 | 特点 |
|------|----------|------|
| **stdio** | 本地进程 | 简单、安全、无需网络 |
| **HTTP** | 远程服务 | 可扩展、需要认证 |

---

## Part 3：Skill系统

### 什么是Skill？

Skill是OpenClaw的能力扩展机制，核心是一个**SKILL.md**文件——让Agent学习如何使用工具的说明文档。

### 与传统Plugin的区别

```
传统Plugin:
代码 ──► 代码接口 ──► 执行

Skill:
SKILL.md ──► LLM阅读理解 ──► LLM决定如何调用 ──► 执行

关键区别: LLM自己读文档学习使用方法！
```

### 为什么这样设计？

1. **灵活性**：不需要预定义所有调用方式
2. **容错性**：LLM可以处理模糊指令
3. **可扩展**：增加能力只需写文档
4. **可维护**：非程序员也能创建Skill

### Skill结构示例

```
~/.openclaw/workspace/skills/weather/
├── SKILL.md          # 核心说明文档
├── scripts/
│   └── get_weather.sh
└── examples/
    └── usage.md
```

**SKILL.md内容**：

```markdown
# Weather Skill

## 功能
获取指定城市的天气预报。

## 使用方法
运行 `./scripts/get_weather.sh <城市名>`

## 示例
用户: "北京今天天气怎么样？"
动作: 运行 ./scripts/get_weather.sh 北京
输出: 解析结果并回复用户
```

### MCP vs Skill

| 维度 | MCP Server | Skill |
|------|------------|-------|
| 标准化 | JSON-RPC协议 | 无标准 |
| 跨平台 | 任何支持MCP的Host | 仅OpenClaw |
| 实现复杂度 | 中等 | 低 |
| 适用场景 | 通用服务集成 | 特定场景快速实现 |

**选择建议**：
- 需要跨平台 → MCP
- 仅OpenClaw使用 → Skill更简单
- 复杂企业集成 → MCP（标准化）
- 快速原型 → Skill（1小时上线）

---

## Part 4：工具设计原则

### Anthropic的洞察

在[Writing Tools for AI Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)中，Anthropic分享了工具设计的核心原则：

> "One of the most common failure modes we see is **bloated tool sets** that cover too much functionality or lead to ambiguous decision points."

### 原则1：最小化工具集

```
❌ 坏设计：20个功能相近的工具
─────────────────────────────
search_products()
find_products()
query_products()
get_product_list()
lookup_products()
...

问题：Agent困惑"我该用哪个？"


✅ 好设计：最小可行工具集
─────────────────────────────
search_products(query, filters)

清晰、无歧义、一个工具解决一类问题
```

**判断标准**：如果人类工程师都不能确定该用哪个工具，AI也做不到。

### 原则2：清晰的接口描述

```json
{
  "name": "create_issue",
  "description": "在GitHub仓库中创建新的Issue",
  "parameters": {
    "repo": {
      "type": "string",
      "description": "仓库名，格式为 owner/repo"
    },
    "title": {
      "type": "string",
      "description": "Issue标题，简明扼要"
    },
    "body": {
      "type": "string",
      "description": "Issue详细描述，支持Markdown"
    }
  }
}
```

关键：**描述要让LLM能准确判断何时使用、如何使用**。

### 原则3：优雅的错误处理

```python
# 好的错误返回
{
  "success": false,
  "error": {
    "code": "REPO_NOT_FOUND",
    "message": "仓库 'owner/repo' 不存在或无权限访问",
    "suggestion": "请检查仓库名是否正确，或确认有访问权限"
  }
}
```

让Agent能理解错误并采取补救措施。

### 原则4：幂等性

```
同一请求执行多次，结果应该一致

✅ 幂等: get_user(id=123) 总是返回同一用户
✅ 幂等: set_status(id=123, status="done") 重复执行无副作用
❌ 非幂等: create_order() 每次都创建新订单
```

非幂等操作需要额外的确认机制。

### 反模式清单

| 反模式 | 问题 | 改进 |
|--------|------|------|
| 功能重叠 | Agent不知选哪个 | 合并或明确区分 |
| 描述模糊 | 误用率高 | 写清楚使用场景 |
| 错误不明 | Agent无法恢复 | 提供可操作的错误信息 |
| 参数过多 | 调用复杂 | 提供合理默认值 |
| 无权限控制 | 安全风险 | 实现最小权限原则 |

---

## Part 5：企业工具治理

### 安全分层

```
┌─────────────────────────────────────────────────────┐
│                   安全分层模型                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  L0 只读工具                                        │
│  └── 搜索、查询、读取                              │
│      风险：低，可自由使用                          │
│                                                     │
│  L1 低影响写入                                      │
│  └── 创建草稿、添加备注                            │
│      风险：中低，需要日志                          │
│                                                     │
│  L2 业务影响                                        │
│  └── 发送消息、修改数据                            │
│      风险：中，需要审批或确认                      │
│                                                     │
│  L3 高风险操作                                      │
│  └── 删除、资金操作、权限变更                      │
│      风险：高，必须人工确认                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 审计要求

每次工具调用应记录：

```json
{
  "timestamp": "2026-03-01T00:15:00Z",
  "user": "user_123",
  "agent": "assistant",
  "tool": "create_issue",
  "parameters": {"repo": "...", "title": "..."},
  "result": "success",
  "token_cost": 150
}
```

### 成本控制

| 维度 | 控制手段 |
|------|----------|
| 调用频率 | Rate limiting |
| 单次成本 | Token限制 |
| 累计成本 | 预算告警 |
| 异常检测 | 模式识别 |

---

## Part 6：实战演示

### 体验MCP

**Claude Desktop配置示例**：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_token"
      }
    }
  }
}
```

配置后，可以直接对Claude说"帮我创建一个GitHub issue"。

### 创建自定义Skill

**步骤**：

1. 创建目录：`~/.openclaw/workspace/skills/my-skill/`
2. 编写SKILL.md
3. 添加脚本或工具
4. 测试使用

**示例SKILL.md**：

```markdown
# 股票查询 Skill

## 功能
查询A股股票的实时行情。

## 使用方法
运行 `curl "https://api.example.com/stock?code=$CODE"`

## 示例
用户: "茅台现在多少钱？"
动作: 查询股票代码600519的实时价格
```

---

## 课堂实操

### 设计一个MCP Server（15分钟）

选择以下场景之一，设计MCP Server的接口：

1. **企业知识库**：搜索内部文档
2. **CRM系统**：查询客户信息
3. **日程管理**：创建和查询日程

需要定义：
- 提供哪些Tools？
- 每个Tool的参数和返回值？
- 如何处理错误？
- 安全等级是什么？

---

## 本讲总结

### 核心概念

- **MCP = AI应用与工具之间的USB协议**
- **三层架构**：Host / Client / Server
- **四大能力**：Tools / Resources / Prompts / Sampling
- **Skill**：OpenClaw的轻量级能力扩展机制

### 工具设计原则

1. **最小化工具集**：避免功能重叠
2. **清晰的描述**：让LLM能准确判断
3. **优雅的错误处理**：让Agent能恢复
4. **幂等性**：重复执行无副作用

### MBA关键洞察

1. **MCP解决的是协作问题**，不只是调用问题
2. **好的工具设计减少Token消耗**，直接降低成本
3. **安全分层是必须的**，不是可选的
4. **Skill让非技术人员也能扩展AI能力**

---

## 延伸阅读

### 官方资源
- [MCP官网](https://modelcontextprotocol.io/)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [Anthropic: Writing Tools for AI Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

### OpenClaw
- [OpenClaw Skills文档](https://docs.openclaw.ai/skills)
- [ClawHub技能市场](https://clawhub.com)

---

*本讲义最后更新：2026-03-01*
