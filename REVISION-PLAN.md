# 课程内容优化计划

## 优化原则

1. **课程结构不变**：L1-2 到 L15-16 顺序保持
2. **上下文工程保留在 L1-2**：作为 Prompt → Agent 的桥梁
3. **每节课内部整合**：把 Part A-F 等补充内容融入主体
4. **逻辑衔接**：确保每个 Part 之间有过渡

---

## L1-2 大语言模型基础

### 当前结构 ✓
```
Part 0: 环境配置
Part 1: 什么是LLM
Part 2: Token经济学
Part 2.5: Post-Training
Part 3: 上下文窗口与注意力预算
Part 4: Prompt工程基础
Part 5: 从单次调用到Agent [过渡]
Part 6: 上下文工程 [重要！连接Prompt和Agent]
Part 7: Temperature与推理模型
Part 8: 安全与风险
```

### 逻辑流
```
环境准备 → 理解LLM → 成本(Token) → 训练原理 → 
上下文限制 → Prompt技巧 → 
[关键过渡] 为什么需要Agent → 上下文工程(Agent核心) → 
参数调优 → 风险防范
```

### 优化点
- Part 5 加强过渡语言，解释为什么单次调用不够
- Part 6 上下文工程强调是"Agent时代的核心能力"

---

## L3-4 工作流与RAG

### 当前问题
- Part A-F 补充内容与 Part 1-8 重复

### 整合方案
```
Part 1: 从对话到工作流 [不变]
Part 2: LangChain简介 [不变]
Part 3: RAG核心概念 ← 整合 Part A (架构图)
Part 4: 分块策略 ← 整合 Part B (策略详解)
Part 5: 向量数据库 ← 整合 Part E (选型对比)
Part 6: 检索策略 ← 新增：整合 Part C (Dense/Sparse/Hybrid)
Part 7: 重排序与评估 ← 新增：整合 Part D + Part F
Part 8: Coze平台实战 [原Part 7]
Part 9: 企业RAG最佳实践 [原Part 8]
```

### 删除
- Part A-F 作为独立附录，从主讲义中移除

---

## L5-6 智能体架构

### 当前问题
- Part 2.5/2.6/3.5 补充内容与 Part 1-8 重复

### 整合方案
```
Part 1: 什么是AI Agent [不变]
Part 2: ReAct框架 ← 整合 Part 2.6 (完整实现思路，不要代码)
Part 3: Plan-and-Solve ← 整合 Part 2.5 (从补充提升为主体)
Part 4: 反思机制 ← 整合 Part 3.5
Part 5: 规划算法 [不变]
Part 6: Agent设计模式 [不变]
Part 7: 前沿Agent框架 [不变]
Part 8: 企业应用案例 [不变]
```

### 优化点
- 三种范式 (ReAct/Plan-and-Solve/Reflection) 各一个 Part
- 每种范式讲清楚：思想 → 流程 → 对比 → 适用场景

---

## L7-8 记忆与工具

### 当前问题
- 补充内容过于技术化（大量代码）
- 与 L1-2 上下文工程有重叠

### 整合方案
```
Part 1: 为什么需要记忆系统 [不变]
Part 2: 记忆类型（四种）[不变]
Part 3: MemGPT架构 [不变]
Part 4: Function Calling [不变]
Part 5: 长时间Agent Harness [不变]
Part 6: 企业工具集成 [不变]
```

### 优化点
- 删除代码实现细节
- 强调与 L1-2 上下文工程的关系：
  - L1-2 讲"什么是上下文工程"
  - L7-8 讲"如何用记忆系统实现上下文管理"
- 加强商业案例

---

## 执行计划

1. [x] 确认优化原则
2. [ ] L3-4：整合 Part A-F 到 Part 1-9
3. [ ] L5-6：整合 Part 2.5/2.6/3.5 到主体
4. [ ] L7-8：精简代码，加强商业案例
5. [ ] 检查 Slides 与讲义对应
6. [ ] 重新编译
