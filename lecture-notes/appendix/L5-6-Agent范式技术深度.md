# L5-6 讲义补充章节：智能体经典范式深度实现

> **本文档包含三个补充章节，可直接插入原讲义**
> - Part 2.5：Plan-and-Solve 范式详解
> - Part 2.6：ReAct 完整实现（从零构建）
> - Part 3.5：Reflection 实现细节

---

## Part 2.5（补充）：Plan-and-Solve 范式详解

### 2.5.1 核心思想："三思而后行"

Plan-and-Solve 是一种与 ReAct 风格迥异但同样强大的智能体范式。如果说 ReAct 像一个经验丰富的侦探，根据现场蛛丝马迹一步步推理；那么 **Plan-and-Solve 则像一位建筑师，在动工之前必须先绘制完整蓝图，然后严格按蓝图施工**。

其核心动机是为了解决思维链在处理多步骤、复杂问题时容易"偏离轨道"的问题。

**两阶段工作流程：**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Plan-and-Solve 工作流程                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   用户问题                                                        │
│      │                                                           │
│      ▼                                                           │
│   ┌──────────────────────────────────────┐                       │
│   │         阶段1：规划 (Planning)         │                       │
│   │  • 分析问题                            │                       │
│   │  • 分解为子任务                         │                       │
│   │  • 生成完整行动计划                      │                       │
│   └──────────────────────────────────────┘                       │
│      │                                                           │
│      ▼ [完整计划：Step1, Step2, Step3, ...]                       │
│   ┌──────────────────────────────────────┐                       │
│   │         阶段2：执行 (Solving)          │                       │
│   │  • 严格按计划逐步执行                    │                       │
│   │  • 每步结果作为下一步输入                 │                       │
│   │  • 直到所有步骤完成                      │                       │
│   └──────────────────────────────────────┘                       │
│      │                                                           │
│      ▼                                                           │
│   最终答案                                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.5.2 与 ReAct 的对比

| 维度 | ReAct | Plan-and-Solve |
|------|-------|----------------|
| **决策模式** | 步进式、动态 | 先规划、后执行 |
| **思考时机** | 每步都思考 | 开始时一次性思考 |
| **计划调整** | 随时可调整 | 执行中一般不修改 |
| **信息依赖** | 需要外部观察 | 可纯内部推理 |
| **适用场景** | 探索性任务、需要工具 | 结构性任务、逻辑推理 |
| **执行路径** | 动态生成 | 预先确定 |
| **错误处理** | 边做边纠错 | 失败则重新规划 |
| **形式化表达** | $(th_t, a_t) = \pi(q, history)$ | $P = \pi_{plan}(q)$, $s_i = \pi_{solve}(P, s_{<i})$ |

**形象比喻：**

- **ReAct** = 导航软件（根据实时路况不断重新规划路线）
- **Plan-and-Solve** = 施工图纸（先画好图，再按图施工）

### 2.5.3 执行流程详解

**数学形式化：**

1. **规划阶段**：规划模型 $\pi_{\text{plan}}$ 根据原始问题 $q$ 生成 $n$ 步计划：
   $$P = (p_1, p_2, \dots, p_n) = \pi_{\text{plan}}(q)$$

2. **执行阶段**：执行模型逐步完成计划，每步依赖之前所有结果：
   $$s_i = \pi_{\text{solve}}(q, P, (s_1, \dots, s_{i-1}))$$

3. **最终答案**：$s_n$

**示例：多步数学问题**

```
问题：一个水果店周一卖出15个苹果。周二是周一的两倍。周三比周二少5个。
      三天总共卖出多少苹果？

=== 规划阶段 ===
计划：
  Step 1: 计算周一销量（已知：15个）
  Step 2: 计算周二销量（周一 × 2）
  Step 3: 计算周三销量（周二 - 5）
  Step 4: 计算总销量（周一 + 周二 + 周三）

=== 执行阶段 ===
Step 1 执行: 周一 = 15
Step 2 执行: 周二 = 15 × 2 = 30
Step 3 执行: 周三 = 30 - 5 = 25
Step 4 执行: 总计 = 15 + 30 + 25 = 70

最终答案: 70个
```

### 2.5.4 适用场景

| 场景 | 说明 | 举例 |
|------|------|------|
| **多步数学题** | 需要先列步骤再计算 | 应用题、方程求解 |
| **报告撰写** | 需要先规划结构再填充内容 | 竞品分析报告、技术方案 |
| **代码生成** | 需要先设计架构再实现细节 | 模块划分、类设计 |
| **项目规划** | 需要先分解任务再执行 | 产品上线 checklist |
| **复杂流程** | 有明确逻辑顺序的任务 | 审批流程、数据处理 pipeline |

### 2.5.5 代码框架

```python
# ==================== 提示词模板 ====================

PLANNER_PROMPT_TEMPLATE = """
你是一个顶级的AI规划专家。你的任务是将用户的复杂问题分解成多个简单步骤。
确保每个步骤都是独立的、可执行的子任务，并按逻辑顺序排列。

问题: {question}

请输出一个Python列表格式的计划:
```python
["步骤1: ...", "步骤2: ...", "步骤3: ...", ...]
```
"""

EXECUTOR_PROMPT_TEMPLATE = """
你是一位执行专家。请严格按照给定计划，解决当前步骤。

原始问题: {question}
完整计划: {plan}
历史步骤与结果: {history}
当前步骤: {current_step}

请仅输出当前步骤的答案:
"""


# ==================== 核心类实现 ====================

class Planner:
    """规划器：负责将问题分解为步骤"""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def plan(self, question: str) -> list[str]:
        prompt = PLANNER_PROMPT_TEMPLATE.format(question=question)
        response = self.llm_client.think([{"role": "user", "content": prompt}])
        
        # 解析返回的计划列表
        import ast
        plan_str = response.split("```python")[1].split("```")[0].strip()
        return ast.literal_eval(plan_str)


class Executor:
    """执行器：负责逐步执行计划"""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def execute(self, question: str, plan: list[str]) -> str:
        history = ""
        
        for i, step in enumerate(plan):
            prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                question=question,
                plan=plan,
                history=history or "无",
                current_step=step
            )
            
            result = self.llm_client.think([{"role": "user", "content": prompt}])
            history += f"步骤{i+1}: {step}\n结果: {result}\n\n"
        
        return result  # 最后一步结果即为最终答案


class PlanAndSolveAgent:
    """Plan-and-Solve 智能体"""
    
    def __init__(self, llm_client):
        self.planner = Planner(llm_client)
        self.executor = Executor(llm_client)
    
    def run(self, question: str) -> str:
        # 1. 规划阶段
        plan = self.planner.plan(question)
        print(f"📋 生成计划: {plan}")
        
        # 2. 执行阶段
        answer = self.executor.execute(question, plan)
        print(f"✅ 最终答案: {answer}")
        
        return answer
```

### 2.5.6 Plan-and-Solve 的优势与局限

**优势：**
- ✅ 结构清晰，便于追溯和调试
- ✅ 适合逻辑密集型任务
- ✅ 减少中途"跑偏"的风险
- ✅ 可预估任务复杂度和成本

**局限：**
- ❌ 计划一旦出错，后续全部受影响
- ❌ 不适合需要实时信息反馈的任务
- ❌ 缺乏动态调整能力
- ❌ 初始规划需要较强的问题理解能力

---

## Part 2.6（补充）：ReAct 完整实现（从零构建）

本节将展示如何从零构建一个完整的 ReAct 智能体，包括 LLM 客户端封装、工具执行器、提示词模板、输出解析器等核心组件。

### 2.6.1 HelloAgentsLLM：LLM 客户端封装

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class HelloAgentsLLM:
    """
    统一的 LLM 客户端封装。
    支持任何 OpenAI 兼容接口，使用流式响应。
    """
    
    def __init__(self, 
                 model: str = None, 
                 api_key: str = None, 
                 base_url: str = None,
                 timeout: int = 60):
        """
        初始化客户端，优先使用传入参数，否则从环境变量加载。
        
        环境变量配置 (.env 文件):
        - LLM_MODEL_ID: 模型名称
        - LLM_API_KEY: API密钥
        - LLM_BASE_URL: 服务地址
        """
        self.model = model or os.getenv("LLM_MODEL_ID")
        api_key = api_key or os.getenv("LLM_API_KEY")
        base_url = base_url or os.getenv("LLM_BASE_URL")
        
        if not all([self.model, api_key, base_url]):
            raise ValueError("模型ID、API密钥和服务地址必须配置")
        
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
    
    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用 LLM 进行思考，返回完整响应。
        使用流式输出，实时显示生成内容。
        """
        print(f"🧠 正在调用 {self.model}...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True
            )
            
            # 处理流式响应
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()  # 换行
            
            return "".join(collected_content)
            
        except Exception as e:
            print(f"❌ LLM调用失败: {e}")
            return None
```

### 2.6.2 ToolExecutor：工具执行器类

```python
from typing import Dict, Any, Callable

class ToolExecutor:
    """
    工具执行器：负责管理和执行智能体可用的工具。
    
    工具三要素:
    1. Name: 唯一标识符，供智能体调用
    2. Description: 自然语言描述，帮助 LLM 判断何时使用
    3. Function: 实际执行的函数
    """
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
    
    def register_tool(self, name: str, description: str, func: Callable):
        """注册一个新工具到工具箱"""
        if name in self.tools:
            print(f"⚠️ 工具 '{name}' 已存在，将被覆盖")
        
        self.tools[name] = {
            "description": description,
            "func": func
        }
        print(f"🔧 工具 '{name}' 已注册")
    
    def get_tool(self, name: str) -> Callable:
        """根据名称获取工具函数"""
        return self.tools.get(name, {}).get("func")
    
    def get_available_tools(self) -> str:
        """获取所有可用工具的格式化描述"""
        return "\n".join([
            f"- {name}: {info['description']}"
            for name, info in self.tools.items()
        ])
    
    def execute(self, tool_name: str, tool_input: str) -> str:
        """执行指定工具并返回结果"""
        func = self.get_tool(tool_name)
        if not func:
            return f"错误: 未找到工具 '{tool_name}'"
        
        try:
            return func(tool_input)
        except Exception as e:
            return f"工具执行出错: {e}"


# ==================== 示例工具实现 ====================

def search(query: str) -> str:
    """
    网页搜索工具（示例实现）
    实际使用时可接入 SerpApi、Google Search API 等
    """
    # 这里是模拟实现，实际应调用搜索 API
    from serpapi import GoogleSearch
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "gl": "cn",
        "hl": "zh-cn"
    }
    
    results = GoogleSearch(params).get_dict()
    
    # 智能解析：优先返回直接答案
    if "answer_box" in results:
        return results["answer_box"].get("answer", "")
    if "knowledge_graph" in results:
        return results["knowledge_graph"].get("description", "")
    if "organic_results" in results:
        snippets = [r.get("snippet", "") for r in results["organic_results"][:3]]
        return "\n".join(snippets)
    
    return f"未找到关于 '{query}' 的信息"


def calculator(expression: str) -> str:
    """计算器工具：执行数学运算"""
    try:
        # 安全评估数学表达式
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"
```

### 2.6.3 ReAct 提示词模板设计

```python
REACT_PROMPT_TEMPLATE = """
你是一个有能力调用外部工具的智能助手。

【可用工具】
{tools}

【输出格式要求】
请严格按照以下格式响应：

Thought: [你的思考过程，分析问题、拆解任务、规划下一步]
Action: [你决定采取的行动]

Action 必须是以下格式之一：
- `工具名[输入参数]`: 调用一个工具，例如 Search[苹果公司市值]
- `Finish[最终答案]`: 当你已经得到最终答案时使用

【重要规则】
1. 每次只输出一个 Thought 和一个 Action
2. 必须等待 Observation（工具返回结果）后再继续思考
3. 当信息足够回答问题时，使用 Finish[答案] 结束

【当前任务】
Question: {question}

【历史轨迹】
{history}

请开始你的思考和行动：
"""
```

### 2.6.4 输出解析器实现

```python
import re
from typing import Tuple, Optional

class ReActOutputParser:
    """
    ReAct 输出解析器
    负责从 LLM 响应中提取 Thought 和 Action
    """
    
    @staticmethod
    def parse_output(text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        解析 LLM 输出，提取 Thought 和 Action
        
        Returns:
            (thought, action) 元组
        """
        # 匹配 Thought（到 Action 或文本结束）
        thought_match = re.search(
            r"Thought:\s*(.*?)(?=\nAction:|$)", 
            text, 
            re.DOTALL
        )
        
        # 匹配 Action（到文本结束）
        action_match = re.search(
            r"Action:\s*(.*?)$", 
            text, 
            re.DOTALL
        )
        
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        
        return thought, action
    
    @staticmethod
    def parse_action(action_text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        解析 Action 字符串，提取工具名和输入
        
        Examples:
            "Search[华为最新手机]" -> ("Search", "华为最新手机")
            "Finish[最终答案是42]" -> ("Finish", "最终答案是42")
        """
        match = re.match(r"(\w+)\[(.+)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None
    
    @staticmethod
    def is_finish_action(action_text: str) -> bool:
        """判断是否是结束动作"""
        return action_text.strip().startswith("Finish")
    
    @staticmethod
    def extract_final_answer(action_text: str) -> str:
        """从 Finish[...] 中提取最终答案"""
        match = re.match(r"Finish\[(.+)\]", action_text, re.DOTALL)
        return match.group(1) if match else action_text
```

### 2.6.5 ReActAgent 完整类实现

```python
class ReActAgent:
    """
    ReAct 智能体完整实现
    
    工作流程:
    1. 格式化提示词（注入工具、问题、历史）
    2. 调用 LLM 获取 Thought + Action
    3. 解析 Action，执行工具或结束
    4. 将 Observation 追加到历史
    5. 重复直到完成或达到最大步数
    """
    
    def __init__(self, 
                 llm_client: HelloAgentsLLM,
                 tool_executor: ToolExecutor,
                 max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.parser = ReActOutputParser()
        self.history = []
    
    def run(self, question: str) -> str:
        """
        运行 ReAct 智能体回答问题
        
        Args:
            question: 用户问题
            
        Returns:
            最终答案或 None（如果失败）
        """
        self.history = []  # 重置历史
        
        print(f"\n{'='*50}")
        print(f"🎯 问题: {question}")
        print('='*50)
        
        for step in range(1, self.max_steps + 1):
            print(f"\n--- 第 {step} 步 ---")
            
            # 1. 构建提示词
            prompt = self._build_prompt(question)
            
            # 2. 调用 LLM
            messages = [{"role": "user", "content": prompt}]
            response = self.llm_client.think(messages)
            
            if not response:
                print("❌ LLM 响应失败")
                break
            
            # 3. 解析输出
            thought, action = self.parser.parse_output(response)
            
            if thought:
                print(f"💭 Thought: {thought}")
            
            if not action:
                print("⚠️ 未能解析出 Action")
                continue
            
            # 4. 检查是否结束
            if self.parser.is_finish_action(action):
                final_answer = self.parser.extract_final_answer(action)
                print(f"\n🎉 最终答案: {final_answer}")
                return final_answer
            
            # 5. 执行工具
            tool_name, tool_input = self.parser.parse_action(action)
            
            if not tool_name or not tool_input:
                observation = "错误: Action 格式不正确"
            else:
                print(f"🔧 Action: {tool_name}[{tool_input}]")
                observation = self.tool_executor.execute(tool_name, tool_input)
            
            print(f"👀 Observation: {observation}")
            
            # 6. 更新历史
            self.history.append(f"Thought: {thought}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")
        
        print("\n⚠️ 达到最大步数，任务未完成")
        return None
    
    def _build_prompt(self, question: str) -> str:
        """构建完整的提示词"""
        tools_desc = self.tool_executor.get_available_tools()
        history_str = "\n".join(self.history) if self.history else "无"
        
        return REACT_PROMPT_TEMPLATE.format(
            tools=tools_desc,
            question=question,
            history=history_str
        )
```

### 2.6.6 实际运行示例

```python
# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 1. 初始化 LLM 客户端
    llm = HelloAgentsLLM()
    
    # 2. 初始化工具执行器并注册工具
    tools = ToolExecutor()
    tools.register_tool(
        "Search",
        "网页搜索引擎。当需要查询实时信息、事实数据时使用。",
        search
    )
    tools.register_tool(
        "Calculator",
        "数学计算器。当需要进行数学运算时使用。",
        calculator
    )
    
    # 3. 创建 ReAct 智能体
    agent = ReActAgent(llm, tools, max_steps=5)
    
    # 4. 运行任务
    answer = agent.run("苹果公司的市值是多少？比微软高还是低？")
```

**预期输出：**

```
==================================================
🎯 问题: 苹果公司的市值是多少？比微软高还是低？
==================================================

--- 第 1 步 ---
🧠 正在调用 gpt-4...
💭 Thought: 要回答这个问题，我需要查询苹果和微软的当前市值。
          先搜索苹果公司的市值。
🔧 Action: Search[苹果公司 Apple 市值 2026]
👀 Observation: 苹果公司 (AAPL) 当前市值约 3.2 万亿美元...

--- 第 2 步 ---
🧠 正在调用 gpt-4...
💭 Thought: 已获得苹果市值约 3.2 万亿美元。
          现在需要查询微软的市值进行比较。
🔧 Action: Search[微软公司 Microsoft 市值 2026]
👀 Observation: 微软公司 (MSFT) 当前市值约 3.4 万亿美元...

--- 第 3 步 ---
🧠 正在调用 gpt-4...
💭 Thought: 已获得两家公司的市值数据：
          - 苹果: 约 3.2 万亿美元
          - 微软: 约 3.4 万亿美元
          可以得出结论并回答问题。

🎉 最终答案: 截至2026年，苹果公司市值约3.2万亿美元，
              微软市值约3.4万亿美元。苹果市值比微软低约2000亿美元。
```

---

## Part 3.5（补充）：Reflection 实现细节

### 3.5.1 反思机制的核心循环

Reflection（反思）机制为智能体引入了一种**事后自我校正循环**，使其能够像人类一样审视自己的工作，发现不足并迭代优化。

**核心工作流程：执行 → 反思 → 优化**

```
┌────────────────────────────────────────────────────────┐
│                 Reflection 迭代循环                      │
├────────────────────────────────────────────────────────┤
│                                                         │
│   ┌───────────┐      ┌───────────┐      ┌───────────┐  │
│   │  执行      │ ───▶ │  反思      │ ───▶ │  优化      │  │
│   │ Execution │      │ Reflection│      │ Refinement│  │
│   └───────────┘      └───────────┘      └───────────┘  │
│        │                   │                   │        │
│        │                   ▼                   │        │
│        │         ┌─────────────────┐          │        │
│        │         │   反馈 Feedback  │          │        │
│        │         │  • 事实性错误    │          │        │
│        │         │  • 逻辑漏洞      │          │        │
│        │         │  • 效率问题      │          │        │
│        │         │  • 遗漏信息      │          │        │
│        │         └─────────────────┘          │        │
│        │                                       │        │
│        └───────────────────────────────────────┘        │
│                         │                               │
│                         ▼                               │
│              "无需改进" 或 达到最大迭代次数？              │
│                    │           │                        │
│                  Yes          No                        │
│                    │           │                        │
│                    ▼           └────────────────────┐   │
│              最终输出                     继续迭代 ──┘   │
│                                                         │
└────────────────────────────────────────────────────────┘
```

**数学形式化：**

$$F_i = \pi_{\text{reflect}}(\text{Task}, O_i)$$
$$O_{i+1} = \pi_{\text{refine}}(\text{Task}, O_i, F_i)$$

其中 $O_i$ 是第 $i$ 次迭代的输出，$F_i$ 是反馈。

### 3.5.2 记忆存储设计

Reflection 的核心在于迭代，而迭代需要记住之前的尝试和反馈。我们需要一个"短期记忆"模块。

```python
from typing import List, Dict, Any, Optional

class ReflectionMemory:
    """
    反思记忆模块
    存储智能体的行动与反思轨迹
    """
    
    def __init__(self):
        self.records: List[Dict[str, Any]] = []
        self.iteration_count = 0
    
    def add_execution(self, content: str, metadata: dict = None):
        """记录一次执行结果"""
        self.records.append({
            "type": "execution",
            "iteration": self.iteration_count,
            "content": content,
            "metadata": metadata or {}
        })
        print(f"📝 记忆更新: 第{self.iteration_count}轮执行结果已记录")
    
    def add_reflection(self, feedback: str, issues: list = None):
        """记录一次反思结果"""
        self.records.append({
            "type": "reflection",
            "iteration": self.iteration_count,
            "feedback": feedback,
            "issues": issues or []
        })
        print(f"📝 记忆更新: 第{self.iteration_count}轮反思已记录")
        self.iteration_count += 1
    
    def get_trajectory(self) -> str:
        """
        将所有记忆格式化为文本
        用于构建优化阶段的提示词
        """
        trajectory_parts = []
        
        for record in self.records:
            if record["type"] == "execution":
                trajectory_parts.append(
                    f"=== 第{record['iteration']}轮尝试 ===\n{record['content']}"
                )
            elif record["type"] == "reflection":
                trajectory_parts.append(
                    f"=== 第{record['iteration']}轮反思 ===\n{record['feedback']}"
                )
        
        return "\n\n".join(trajectory_parts)
    
    def get_last_execution(self) -> Optional[str]:
        """获取最近一次执行结果"""
        for record in reversed(self.records):
            if record["type"] == "execution":
                return record["content"]
        return None
    
    def get_last_feedback(self) -> Optional[str]:
        """获取最近一次反思反馈"""
        for record in reversed(self.records):
            if record["type"] == "reflection":
                return record["feedback"]
        return None
    
    def get_all_issues(self) -> List[str]:
        """获取所有被识别的问题"""
        all_issues = []
        for record in self.records:
            if record["type"] == "reflection" and record.get("issues"):
                all_issues.extend(record["issues"])
        return all_issues
```

### 3.5.3 教训提取逻辑

从反思中提取可复用的"教训"，形成经验积累。

```python
class LessonExtractor:
    """
    教训提取器
    从反思记录中提取可复用的经验
    """
    
    EXTRACTION_PROMPT = """
分析以下反思内容，提取可复用的经验教训。

反思内容:
{reflection}

请提取:
1. 问题类型（如：逻辑错误、效率问题、边界情况等）
2. 根本原因
3. 改进建议
4. 可泛化的教训（可应用到其他类似问题的经验）

输出格式:
```json
{
  "problem_type": "...",
  "root_cause": "...",
  "improvement": "...",
  "generalizable_lesson": "..."
}
```
"""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.lessons: List[Dict] = []
    
    def extract(self, reflection: str) -> Dict:
        """从单次反思中提取教训"""
        prompt = self.EXTRACTION_PROMPT.format(reflection=reflection)
        response = self.llm_client.think([{"role": "user", "content": prompt}])
        
        import json
        try:
            lesson = json.loads(
                response.split("```json")[1].split("```")[0].strip()
            )
            self.lessons.append(lesson)
            return lesson
        except:
            return {"error": "提取失败", "raw": response}
    
    def get_relevant_lessons(self, task_description: str) -> List[Dict]:
        """根据任务描述获取相关的历史教训"""
        # 简单实现：返回所有教训
        # 高级实现：可使用向量相似度匹配
        return self.lessons
```

### 3.5.4 完整的 Reflection Agent 实现

```python
class ReflectionAgent:
    """
    反思智能体完整实现
    
    工作流程:
    1. 初始执行：生成第一版输出
    2. 反思循环：
       a. 评估当前输出
       b. 如果"无需改进"则结束
       c. 否则根据反馈优化
    3. 返回最终输出
    """
    
    # ==================== 提示词模板 ====================
    
    INITIAL_PROMPT = """
你是一位资深的{role}。请根据以下要求完成任务。

任务要求: {task}

请直接输出结果，不要包含额外解释。
"""
    
    REFLECT_PROMPT = """
你是一位极其严格的评审专家。请审查以下输出，专注于找出问题。

【原始任务】
{task}

【待审查内容】
```
{content}
```

【评审维度】
1. 正确性：是否有事实错误或逻辑漏洞？
2. 完整性：是否遗漏了重要内容？
3. 效率/质量：是否有更优的方案？
4. 规范性：是否符合最佳实践？

【评审要求】
- 如果存在问题，清晰指出并给出具体改进建议
- 如果已经足够好，回答"无需改进"

请输出你的评审意见：
"""
    
    REFINE_PROMPT = """
你是一位资深的{role}。请根据评审反馈优化你的输出。

【原始任务】
{task}

【上一版输出】
```
{last_output}
```

【评审反馈】
{feedback}

请根据反馈生成优化后的新版本，直接输出结果：
"""
    
    def __init__(self, 
                 llm_client, 
                 role: str = "专家",
                 max_iterations: int = 3):
        self.llm_client = llm_client
        self.role = role
        self.max_iterations = max_iterations
        self.memory = ReflectionMemory()
    
    def run(self, task: str) -> str:
        """运行反思智能体"""
        print(f"\n{'='*50}")
        print(f"🎯 任务: {task}")
        print('='*50)
        
        # 1. 初始执行
        print("\n--- 初始执行 ---")
        initial_output = self._execute(task)
        self.memory.add_execution(initial_output)
        
        # 2. 反思循环
        for i in range(self.max_iterations):
            print(f"\n--- 第 {i+1}/{self.max_iterations} 轮迭代 ---")
            
            # a. 反思
            print("\n🔍 正在反思...")
            last_output = self.memory.get_last_execution()
            feedback = self._reflect(task, last_output)
            self.memory.add_reflection(feedback)
            
            # b. 检查是否需要继续
            if "无需改进" in feedback:
                print("\n✅ 反思认为已无需改进，任务完成！")
                break
            
            # c. 优化
            print("\n🔧 正在优化...")
            refined_output = self._refine(task, last_output, feedback)
            self.memory.add_execution(refined_output)
        
        # 3. 返回最终输出
        final_output = self.memory.get_last_execution()
        print(f"\n{'='*50}")
        print(f"📋 最终输出:\n{final_output}")
        print('='*50)
        
        return final_output
    
    def _execute(self, task: str) -> str:
        """执行任务，生成初始输出"""
        prompt = self.INITIAL_PROMPT.format(role=self.role, task=task)
        return self.llm_client.think([{"role": "user", "content": prompt}])
    
    def _reflect(self, task: str, content: str) -> str:
        """反思当前输出"""
        prompt = self.REFLECT_PROMPT.format(task=task, content=content)
        return self.llm_client.think([{"role": "user", "content": prompt}])
    
    def _refine(self, task: str, last_output: str, feedback: str) -> str:
        """根据反馈优化输出"""
        prompt = self.REFINE_PROMPT.format(
            role=self.role,
            task=task,
            last_output=last_output,
            feedback=feedback
        )
        return self.llm_client.think([{"role": "user", "content": prompt}])


# ==================== 使用示例 ====================

if __name__ == "__main__":
    llm = HelloAgentsLLM()
    
    # 代码生成任务
    agent = ReflectionAgent(
        llm_client=llm,
        role="Python程序员",
        max_iterations=3
    )
    
    result = agent.run(
        "编写一个Python函数，找出1到n之间所有的素数"
    )
```

### 3.5.5 运行示例与分析

```
==================================================
🎯 任务: 编写一个Python函数，找出1到n之间所有的素数
==================================================

--- 初始执行 ---
🧠 正在调用模型...
def find_primes(n):
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes
📝 记忆更新: 第0轮执行结果已记录

--- 第 1/3 轮迭代 ---

🔍 正在反思...
当前代码的时间复杂度为 O(n²)。存在以下问题：
1. 内层循环可以只检查到 sqrt(num)，复杂度降为 O(n*sqrt(n))
2. 更优方案是使用埃拉托斯特尼筛法，复杂度为 O(n*log(log(n)))
建议使用筛法重写。
📝 记忆更新: 第0轮反思已记录

🔧 正在优化...
def find_primes(n):
    if n < 2:
        return []
    
    # 埃拉托斯特尼筛法
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    
    return [i for i in range(n + 1) if is_prime[i]]
📝 记忆更新: 第1轮执行结果已记录

--- 第 2/3 轮迭代 ---

🔍 正在反思...
当前实现使用了埃拉托斯特尼筛法，时间复杂度为 O(n*log(log(n)))，
已经是寻找素数的最优算法之一。代码结构清晰，边界条件处理正确。
无需改进。
📝 记忆更新: 第1轮反思已记录

✅ 反思认为已无需改进，任务完成！

==================================================
📋 最终输出:
def find_primes(n):
    if n < 2:
        return []
    
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    
    return [i for i in range(n + 1) if is_prime[i]]
==================================================
```

### 3.5.6 Reflection 最佳实践

| 实践要点 | 说明 |
|---------|------|
| **精心设计反思提示词** | 反思的质量决定了优化的方向，需要明确评审维度 |
| **设置合理的迭代上限** | 通常 2-3 次迭代即可，过多会增加成本且收益递减 |
| **定义清晰的终止条件** | "无需改进"关键词 + 迭代次数双重保险 |
| **保持角色一致性** | 执行者和评审者可以是不同角色，但需保持任务理解一致 |
| **记录完整轨迹** | 便于调试和分析优化过程 |

---

## 三种范式的综合对比与选型指南

| 维度 | ReAct | Plan-and-Solve | Reflection |
|------|-------|----------------|------------|
| **核心特点** | 思考+行动交织 | 先规划后执行 | 执行+反思迭代 |
| **决策模式** | 动态、步进 | 静态、分阶段 | 迭代优化 |
| **工具使用** | 核心能力 | 可选 | 可选 |
| **适用场景** | 探索性任务 | 结构化任务 | 质量敏感任务 |
| **成本** | 中等 | 较低 | 较高 |
| **可解释性** | 高 | 高 | 最高 |
| **典型应用** | 问答搜索 | 数学推理 | 代码生成 |

**选型决策树：**

```
任务需要外部工具/实时信息？
    │
    ├── Yes → ReAct
    │
    └── No → 任务结构是否清晰可分解？
              │
              ├── Yes → Plan-and-Solve
              │
              └── No → 对输出质量要求是否极高？
                        │
                        ├── Yes → Reflection
                        │
                        └── No → 简单 Prompt 即可
```

---

*本补充章节参考：Datawhale Hello-Agents 第四章*
*生成时间：2026-03-06*
# L5-6 补充章节：Agent范式深度实现

> **课程**: MBA大模型智能体课程  
> **补充来源**: Datawhale Hello-Agents 第四章  
> **适用**: 讲师备课 / 学生深入学习

---

## 背景

原有L5-6讲义主要从概念层面介绍了ReAct框架、反思机制和规划算法，但缺少：
1. **Plan-and-Solve范式**的详细讲解（完全缺失）
2. **完整的代码实现**（从零构建ReAct）
3. **ToolExecutor类设计**（工具管理器）
4. **输出解析器实现**（从LLM输出中提取结构化信息）

本补充章节将填补这些空白，让学员不仅理解概念，更能动手实现。

---

## 补充内容

### Part 1: Plan-and-Solve 范式详解

#### 1.1 范式概述

如果说ReAct像一个经验丰富的侦探，根据现场线索一步步推理；那么**Plan-and-Solve**则更像一位建筑师，在动工之前必须先绘制完整的蓝图。

Plan-and-Solve将整个流程解耦为两个核心阶段：

```
┌─────────────────────────────────────────────────────┐
│                Plan-and-Solve 范式                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Phase 1: Planning（规划阶段）                      │
│  ─────────────────────────────                      │
│  • 接收完整问题                                     │
│  • 分解任务为多个子步骤                             │
│  • 输出结构化的行动计划                             │
│                                                     │
│  Phase 2: Solving（执行阶段）                       │
│  ─────────────────────────                          │
│  • 严格按计划逐步执行                               │
│  • 每步结果作为下一步输入                           │
│  • 直到完成所有步骤                                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

#### 1.2 形式化表达

规划模型 $\pi_{\text{plan}}$ 根据原始问题 $q$ 生成包含 $n$ 个步骤的计划：

$$P = \pi_{\text{plan}}(q) = (p_1, p_2, \dots, p_n)$$

执行阶段，每个步骤的解决方案依赖于问题、计划和之前的执行结果：

$$s_i = \pi_{\text{solve}}(q, P, (s_1, \dots, s_{i-1}))$$

#### 1.3 与ReAct的对比

| 维度 | ReAct | Plan-and-Solve |
|------|-------|----------------|
| 决策方式 | 步进式（走一步看一步） | 预规划式（先规划后执行） |
| 适用场景 | 探索性任务、需要外部反馈 | 结构化任务、逻辑链明确 |
| 纠错能力 | 动态调整 | 计划一旦确定较难修改 |
| 效率 | 可能多次试错 | 路径清晰、效率高 |
| 典型应用 | 搜索任务、信息收集 | 数学推理、报告生成、代码开发 |

#### 1.4 适用场景

Plan-and-Solve特别适合：
- **多步数学应用题**：需要先列出计算步骤，再逐一求解
- **报告撰写**：先规划结构（引言、正文、结论），再逐一填充
- **代码生成**：先构思架构，再逐一实现模块
- **项目管理**：先分解任务，再逐一执行

---

### Part 2: 完整的ReAct代码实现

#### 2.1 基础LLM客户端

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class HelloAgentsLLM:
    """
    统一的LLM客户端，支持任何兼容OpenAI接口的服务
    """
    def __init__(self, model: str = None, api_key: str = None, base_url: str = None):
        self.model = model or os.getenv("LLM_MODEL_ID")
        api_key = api_key or os.getenv("LLM_API_KEY")
        base_url = base_url or os.getenv("LLM_BASE_URL")
        
        if not all([self.model, api_key, base_url]):
            raise ValueError("模型ID、API密钥和服务地址必须提供或在.env文件中定义")

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """调用LLM进行思考"""
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()
            return "".join(collected_content)

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None
```

#### 2.2 ToolExecutor类设计

**设计理念**：工具执行器负责管理和调度所有可用工具，是Agent与外部世界交互的桥梁。

```python
from typing import Dict, Any, Callable

class ToolExecutor:
    """
    工具执行器 - 统一管理和执行工具
    
    设计原则：
    1. 统一注册：所有工具通过统一接口注册
    2. 描述驱动：工具描述用于让LLM理解何时使用
    3. 安全执行：捕获异常，返回友好错误信息
    """
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, description: str, func: Callable):
        """
        注册一个新工具
        
        Args:
            name: 工具名称（供LLM调用时使用）
            description: 工具描述（让LLM理解何时使用）
            func: 实际执行函数
        """
        if name in self.tools:
            print(f"⚠️ 警告: 工具 '{name}' 已存在，将被覆盖")
        
        self.tools[name] = {
            "description": description, 
            "func": func
        }
        print(f"✅ 工具 '{name}' 已注册")

    def get_tool(self, name: str) -> Callable:
        """根据名称获取工具函数"""
        return self.tools.get(name, {}).get("func")

    def get_available_tools(self) -> str:
        """获取所有可用工具的格式化描述"""
        return "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.tools.items()
        ])
    
    def execute(self, tool_name: str, tool_input: str) -> str:
        """
        安全执行工具
        
        Returns:
            执行结果或错误信息
        """
        tool_func = self.get_tool(tool_name)
        if not tool_func:
            return f"❌ 错误: 未找到名为 '{tool_name}' 的工具"
        
        try:
            return tool_func(tool_input)
        except Exception as e:
            return f"❌ 工具执行错误: {str(e)}"
```

#### 2.3 输出解析器实现

**核心挑战**：LLM返回的是自然语言文本，需要从中精确提取结构化信息。

```python
import re
from typing import Tuple, Optional

class ReActOutputParser:
    """
    ReAct输出解析器 - 从LLM输出中提取Thought和Action
    
    期望的LLM输出格式：
    Thought: 我需要搜索最新的信息...
    Action: Search[华为最新手机]
    """
    
    @staticmethod
    def parse_output(text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        解析LLM的完整输出，提取Thought和Action
        
        Returns:
            (thought, action) 元组
        """
        # 提取Thought：匹配到Action或文本末尾
        thought_match = re.search(
            r"Thought:\s*(.*?)(?=\nAction:|$)", 
            text, 
            re.DOTALL
        )
        
        # 提取Action：匹配到文本末尾
        action_match = re.search(
            r"Action:\s*(.*?)$", 
            text, 
            re.DOTALL
        )
        
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        
        return thought, action

    @staticmethod
    def parse_action(action_text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        解析Action字符串，提取工具名称和输入
        
        示例输入: "Search[华为最新手机]"
        返回: ("Search", "华为最新手机")
        """
        # 匹配 ToolName[input] 格式
        match = re.match(r"(\w+)\[(.*)?\]", action_text, re.DOTALL)
        if match:
            tool_name = match.group(1)
            tool_input = match.group(2) if match.group(2) else ""
            return tool_name, tool_input
        return None, None
    
    @staticmethod
    def is_finish_action(action: str) -> bool:
        """检查是否是Finish动作"""
        return action.startswith("Finish")
    
    @staticmethod
    def extract_final_answer(action: str) -> str:
        """从Finish动作中提取最终答案"""
        match = re.match(r"Finish\[(.*)\]", action, re.DOTALL)
        return match.group(1) if match else action
```

#### 2.4 完整的ReAct Agent实现

```python
class ReActAgent:
    """
    ReAct Agent - 完整实现
    
    核心循环: Thought → Action → Observation → Thought → ...
    """
    
    # 提示词模板
    PROMPT_TEMPLATE = """
你是一个有能力调用外部工具的智能助手。

可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`: 调用一个可用工具。
- `Finish[最终答案]`: 当你认为已经获得最终答案时。

重要: 当你收集到足够的信息能够回答用户问题时，必须使用 Finish[最终答案] 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}
"""

    def __init__(
        self, 
        llm_client: HelloAgentsLLM, 
        tool_executor: ToolExecutor, 
        max_steps: int = 5
    ):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.parser = ReActOutputParser()
        self.history = []

    def run(self, question: str) -> str:
        """
        运行ReAct Agent来回答问题
        
        Args:
            question: 用户问题
            
        Returns:
            最终答案或None
        """
        self.history = []  # 重置历史记录
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"\n{'='*50}")
            print(f"--- 第 {current_step} 步 ---")
            print(f"{'='*50}")

            # 1. 构建提示词
            prompt = self._build_prompt(question)
            
            # 2. 调用LLM
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)
            
            if not response_text:
                print("❌ LLM未能返回有效响应")
                break

            # 3. 解析输出
            thought, action = self.parser.parse_output(response_text)
            
            if thought:
                print(f"🤔 思考: {thought}")

            if not action:
                print("⚠️ 未能解析出有效的Action")
                break

            # 4. 检查是否完成
            if self.parser.is_finish_action(action):
                final_answer = self.parser.extract_final_answer(action)
                print(f"\n🎉 最终答案: {final_answer}")
                return final_answer
            
            # 5. 解析并执行工具调用
            tool_name, tool_input = self.parser.parse_action(action)
            
            if not tool_name:
                print(f"⚠️ 无法解析Action: {action}")
                self.history.append(f"Action: {action}")
                self.history.append(f"Observation: 无效的Action格式")
                continue

            print(f"🎬 行动: {tool_name}[{tool_input}]")
            
            # 6. 执行工具
            observation = self.tool_executor.execute(tool_name, tool_input)
            print(f"👀 观察: {observation}")
            
            # 7. 更新历史
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        print("\n⏰ 已达到最大步数，流程终止")
        return None
    
    def _build_prompt(self, question: str) -> str:
        """构建完整的提示词"""
        tools_desc = self.tool_executor.get_available_tools()
        history_str = "\n".join(self.history) if self.history else "无"
        
        return self.PROMPT_TEMPLATE.format(
            tools=tools_desc,
            question=question,
            history=history_str
        )
```

---

### Part 3: Plan-and-Solve 完整实现

#### 3.1 规划器（Planner）

```python
import ast

class Planner:
    """
    规划器 - 将复杂问题分解为可执行的步骤计划
    """
    
    PLANNER_PROMPT = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。

请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。

你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}

请严格按照以下格式输出你的计划（```python与```作为前后缀是必要的）:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""

    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def plan(self, question: str) -> list:
        """
        生成行动计划
        
        Returns:
            步骤列表，如 ["计算周一销量", "计算周二销量", ...]
        """
        prompt = self.PLANNER_PROMPT.format(question=question)
        messages = [{"role": "user", "content": prompt}]
        
        print("📋 正在生成计划...")
        response_text = self.llm_client.think(messages=messages) or ""
        
        # 解析Python列表
        try:
            # 提取```python和```之间的内容
            plan_str = response_text.split("```python")[1].split("```")[0].strip()
            plan = ast.literal_eval(plan_str)
            
            if isinstance(plan, list):
                print(f"✅ 计划已生成，共 {len(plan)} 个步骤")
                return plan
            return []
            
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划失败: {e}")
            return []
```

#### 3.2 执行器（Executor）

```python
class Executor:
    """
    执行器 - 按计划逐步执行，维护状态（历史结果）
    """
    
    EXECUTOR_PROMPT = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。

你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决"当前步骤"，并仅输出该步骤的最终答案，不要输出任何额外的解释。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对"当前步骤"的回答:
"""

    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def execute(self, question: str, plan: list) -> str:
        """
        执行计划中的所有步骤
        
        Returns:
            最终答案（最后一步的结果）
        """
        history = ""
        
        print("\n🚀 开始执行计划...")
        
        for i, step in enumerate(plan):
            print(f"\n--- 执行步骤 {i+1}/{len(plan)}: {step} ---")
            
            prompt = self.EXECUTOR_PROMPT.format(
                question=question,
                plan=plan,
                history=history if history else "无",
                current_step=step
            )
            
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages) or ""
            
            # 更新历史记录
            history += f"步骤 {i+1}: {step}\n结果: {response_text}\n\n"
            
            print(f"✅ 步骤 {i+1} 完成，结果: {response_text}")

        return response_text
```

#### 3.3 Plan-and-Solve Agent

```python
class PlanAndSolveAgent:
    """
    Plan-and-Solve Agent - 先规划后执行
    """
    
    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client
        self.planner = Planner(llm_client)
        self.executor = Executor(llm_client)

    def run(self, question: str) -> str:
        """
        运行完整流程：规划 → 执行
        """
        print(f"\n{'='*60}")
        print(f"📌 问题: {question}")
        print(f"{'='*60}")
        
        # Phase 1: 规划
        plan = self.planner.plan(question)
        
        if not plan:
            print("❌ 无法生成有效计划")
            return None
        
        print(f"\n📋 生成的计划:")
        for i, step in enumerate(plan, 1):
            print(f"  {i}. {step}")
        
        # Phase 2: 执行
        final_answer = self.executor.execute(question, plan)
        
        print(f"\n{'='*60}")
        print(f"🎉 最终答案: {final_answer}")
        print(f"{'='*60}")
        
        return final_answer
```

---

### Part 4: 三种范式对比总结

| 范式 | 核心思想 | 决策方式 | 适用场景 | 典型应用 |
|------|---------|---------|---------|---------|
| **ReAct** | 思考与行动交织 | 步进式 | 需要外部信息的探索性任务 | 搜索、问答、信息收集 |
| **Plan-and-Solve** | 先规划后执行 | 预规划式 | 结构化的多步推理任务 | 数学题、报告生成、代码开发 |
| **Reflection** | 执行-反思-优化 | 迭代式 | 需要高质量输出的任务 | 代码优化、文档撰写、决策支持 |

**选择建议**：
- 需要实时信息 → **ReAct**
- 逻辑链清晰 → **Plan-and-Solve**
- 质量要求高 → **Reflection**
- 复杂场景 → **混合使用**

---

## 代码示例：完整运行Demo

```python
# demo_react.py
from serpapi import SerpApiClient
import os

# 1. 定义搜索工具
def search(query: str) -> str:
    """网页搜索工具"""
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "错误: SERPAPI_API_KEY 未配置"
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "gl": "cn",
        "hl": "zh-cn",
    }
    
    client = SerpApiClient(params)
    results = client.get_dict()
    
    # 智能解析结果
    if "answer_box" in results and "answer" in results["answer_box"]:
        return results["answer_box"]["answer"]
    if "organic_results" in results and results["organic_results"]:
        snippets = [
            f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
            for i, res in enumerate(results["organic_results"][:3])
        ]
        return "\n\n".join(snippets)
    
    return f"未找到关于 '{query}' 的信息"

# 2. 创建Agent
llm_client = HelloAgentsLLM()
tool_executor = ToolExecutor()
tool_executor.register_tool(
    "Search", 
    "网页搜索引擎，用于查询实时信息和事实",
    search
)

agent = ReActAgent(llm_client, tool_executor, max_steps=5)

# 3. 运行
result = agent.run("华为最新的旗舰手机是哪款？主要卖点是什么？")
print(f"\n最终结果: {result}")
```

---

## 与原有内容的衔接

本补充章节应安排在原L5-6讲义的以下位置：

1. **Part 2（ReAct框架）之后**：插入"Part 2.5: ReAct完整代码实现"
2. **Part 3（反思机制）之前**：插入"Part 2.6: Plan-and-Solve范式详解"
3. **Part 4（规划算法）之后**：插入"Part 4.5: ToolExecutor与输出解析器设计"

建议的课堂安排：
- 概念讲解：30分钟（使用原讲义）
- 代码实现演示：30分钟（使用补充内容）
- 动手实践：30分钟（学员自己实现简化版Agent）

---

*本补充章节最后更新：2026-03-06*
