# 第一天课后实践任务手册

> 适用课程：MBA《大模型智能体》
> 
> 完成时间：**第二周上课前完成**（建议总投入 3~5 小时）

---

## 第一天课后任务 (第二周上课前完成)

## 任务1: 环境搭建 (必做)

### 1.1 OpenClaw 安装指南（macOS / Windows / Linux）

> 目标：完成 OpenClaw 本地安装，并能成功启动 Gateway。

#### A) 通用前置检查

OpenClaw CLI 依赖 Node.js 环境，建议先确认：

- Node.js LTS（建议 v20+）
- npm（随 Node.js 安装）
- Git
- 稳定网络环境

---

#### B) macOS 安装步骤

```bash
# 1) 安装 Homebrew（若已安装可跳过）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2) 安装 Node.js 与 Git
brew update
brew install node git

# 3) 验证版本
node -v
npm -v
git --version

# 4) 安装 OpenClaw CLI
npm install -g openclaw

# 5) 验证安装
openclaw --version
openclaw help
```

---

#### C) Windows 安装步骤（PowerShell）

```powershell
# 1) 安装 Node.js LTS 与 Git（需管理员权限）
winget install OpenJS.NodeJS.LTS
winget install Git.Git

# 2) 重新打开 PowerShell 后验证
node -v
npm -v
git --version

# 3) 安装 OpenClaw CLI
npm install -g openclaw

# 4) 验证安装
openclaw --version
openclaw help
```

---

#### D) Linux 安装步骤（Ubuntu/Debian 示例）

```bash
# 1) 安装基础依赖
sudo apt update
sudo apt install -y curl ca-certificates gnupg git

# 2) 安装 Node.js LTS（NodeSource）
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# 3) 验证版本
node -v
npm -v
git --version

# 4) 安装 OpenClaw CLI
npm install -g openclaw

# 5) 验证安装
openclaw --version
openclaw help
```

---

### 1.2 基础配置（API Key 设置）

> 建议优先使用向导，避免手工配置错误。

#### 方案一：向导配置（推荐）

```bash
# 初始化本地配置与工作区
openclaw setup --wizard

# 按需补充模型/网关配置
openclaw configure --section model --section gateway
```

#### 方案二：环境变量配置（示例）

> 仅示例，你可根据所用模型平台选择对应 Key。

**macOS / Linux（zsh/bash）**

```bash
# 编辑 shell 配置文件（zsh 用 ~/.zshrc；bash 用 ~/.bashrc）
export OPENAI_API_KEY="sk-xxx"
export ANTHROPIC_API_KEY="sk-ant-xxx"
export OPENROUTER_API_KEY="sk-or-xxx"

# 使配置生效
source ~/.zshrc
```

**Windows（PowerShell）**

```powershell
setx OPENAI_API_KEY "sk-xxx"
setx ANTHROPIC_API_KEY "sk-ant-xxx"
setx OPENROUTER_API_KEY "sk-or-xxx"

# 关闭并重新打开 PowerShell 后生效
```

#### 安全提醒

- 不要把真实 API Key 提交到 Git 仓库
- 不要在截图中暴露完整 Key（只显示前 4 位）
- 建议使用 `.env` + `.gitignore` 或系统环境变量

---

### 1.3 验证安装成功的检查清单

按顺序执行并打勾：

```bash
openclaw --version
openclaw gateway start
openclaw gateway status
openclaw health
openclaw gateway stop
```

- [ ] `openclaw --version` 有正常版本输出
- [ ] `openclaw gateway start` 启动成功
- [ ] `openclaw gateway status` 显示运行状态
- [ ] `openclaw health` 返回健康检查结果
- [ ] 能正常停止 Gateway（`openclaw gateway stop`）

---

### 1.4 常见问题 FAQ

**Q1: 提示 `openclaw: command not found`？**  
A: 先确认 `npm install -g openclaw` 是否成功；若成功，检查 npm 全局 bin 目录是否在 PATH 中。

**Q2: npm 安装报 EACCES 权限错误？**  
A: 不建议 `sudo npm install -g`。可改为配置用户级 npm 前缀目录后重试。

**Q3: Gateway 启动失败，提示端口占用？**  
A: 先执行 `openclaw gateway status` 查看状态；必要时关闭冲突进程后重启。

**Q4: 已配置 API Key 但模型调用失败？**  
A: 重新打开终端确认环境变量生效；或使用 `openclaw configure --section model` 重新绑定模型配置。

**Q5: 公司网络下连接不稳定？**  
A: 检查代理、防火墙与 DNS；必要时切换网络并重试。

---

## 任务2: 基础体验 (必做)

### 2.1 与 Agent 进行 10 轮以上对话

要求：

- 至少 10 轮连续交互（同一主题更佳）
- 主题建议：市场分析、运营优化、商业模式评估、行业研究
- 每轮记录：你的输入 + Agent 输出 + 你对结果质量的简评

**建议记录模板**

| 轮次 | 你的问题 | Agent回答摘要 | 你的评价（1~5分） |
|---|---|---|---|
| 1 |  |  |  |
| ... |  |  |  |
| 10 |  |  |  |

---

### 2.2 修改 SOUL.md，观察行为变化

> 目标：理解“系统人格/行为约束”对 Agent 输出的影响。

操作建议：

1. 备份原文件
2. 修改 2~3 条人格或输出风格规则
3. 用**同一组问题**做 A/B 对比（修改前 vs 修改后）

示例（可参考）：

- 输出风格：从“简洁结论优先”改为“先结构化分析后结论”
- 语气风格：从“严谨专业”改为“顾问式建议 + 可执行清单”
- 约束策略：增加“所有建议必须含风险提示”

**建议命令**

```bash
# macOS/Linux
cd ~/.openclaw/workspace
cp SOUL.md SOUL.md.bak
# 用你熟悉的编辑器打开 SOUL.md 修改
```

---

### 2.3 尝试至少 3 个内置 Skill

要求：

- 至少调用 3 个不同 Skill
- 每个 Skill 至少 1 次成功调用
- 记录：用途、输入、输出、是否符合预期

示例方向（任选）：

1. `weather`：查询某城市未来 3 天天气
2. `summarize`：总结一篇网页/文章核心观点
3. `github`：查看某仓库 issue 或 PR 信息
4. 你熟悉的其他内置 Skill

---

### 2.4 记录使用体验（截图 + 文字）

**截图指引（必含）**

- 截图1：安装成功（`openclaw --version` + `openclaw help`）
- 截图2：Gateway 状态（`openclaw gateway status`）
- 截图3：10轮对话证据（至少展示开始、中间、结尾）
- 截图4：SOUL.md 修改前后差异（可用 diff 或前后片段）
- 截图5：3个 Skill 的调用结果

**文字反思（300~500字）**

建议回答：

1. 哪个环节最顺利？为什么？
2. 哪个环节最卡顿？你如何排查？
3. 修改 SOUL.md 后，Agent 行为发生了哪些可观察变化？
4. 你认为 Agent 在你所在行业最有价值的场景是什么？

---

## 任务3: 调研报告 (选做，加分)

请选择 **A/B/C** 任一方向完成短报告（建议 1000~2000 字）。

### A. 行业应用调研

选一个行业（如金融、零售、医疗、教育、制造等），调研 Agent 应用现状：

- 典型应用场景（至少 3 个）
- 头部公司/产品案例（至少 2 个）
- 价值与限制（ROI、风险、合规）
- 你对未来 2 年趋势判断

### B. 竞品对比分析

选择 2~3 个 Agent 平台进行对比：

- 功能维度：工具调用、记忆、工作流、多 Agent、可观测性
- 商业维度：定价、生态、目标用户
- 体验维度：上手难度、稳定性、响应质量
- 最终结论：给出你的选型建议（含适用场景）

### C. 技术深度探索

深入研究一个技术点（如 MCP / RAG / 多 Agent）：

- 核心机制与架构图
- 关键技术挑战
- 工程落地建议
- 未来迭代方向

---

## 任务4: 创意实践 (选做，加分)

完成以下任意 2~3 项并给出成果证明：

- 配置一个专属 Agent（修改人格/添加 Skill）
- 连接一个 Channel（飞书 / Telegram）
- 实现一个简单自动化工作流

### 示例：自动化工作流参考

**场景**：每日晨间行业资讯摘要

1. 获取信息源（新闻/RSS/网页）
2. Agent 总结成 5 条要点
3. 自动发送到指定频道（飞书/Telegram）

**验收标准**：

- 流程可重复执行
- 输出格式稳定
- 至少运行成功 2 次

---

## 提交要求

- 格式：Markdown 或 PDF
- 截止时间：第二周上课前一天
- 提交方式：[待定]

建议文件命名：

`姓名-班级-day1-homework.md` 或 `姓名-班级-day1-homework.pdf`

---

## 评分标准

- 环境搭建：30%
- 基础体验：30%
- 调研/创意：40%

### 评分细则（助教参考）

| 维度 | 权重 | A档（优秀） | B档（良好） | C档（及格） |
|---|---:|---|---|---|
| 环境搭建 | 30% | 安装+配置+排障完整，证据充分 | 完成安装配置，证据较完整 | 仅部分完成，证据不足 |
| 基础体验 | 30% | 10轮对话高质量，SOUL对比清晰，3个Skill效果好 | 完成要求，分析一般 | 仅完成最低要求 |
| 调研/创意 | 40% | 观点深入，有案例与方法论，落地性强 | 有分析有结论 | 描述性为主，深度不足 |

---

## 最终提交清单（Checklist）

- [ ] 已完成 OpenClaw 安装与基础配置
- [ ] 已通过安装验证检查清单
- [ ] 已完成 10 轮以上对话记录
- [ ] 已完成 SOUL.md 修改与前后对比
- [ ] 已完成至少 3 个 Skill 体验
- [ ] 已附关键截图（不少于 5 张）
- [ ] 已完成文字反思（300~500字）
- [ ] （选做）已完成调研报告或创意实践

---

> 提示：本次作业重点不是“代码量”，而是你对 Agent 系统的理解深度、实验过程严谨性与商业洞察。