#!/usr/bin/env python3
"""Lab 3 - ReAct Agent Demo.

特性：
1) ReAct循环（Thought -> Action -> Observation）
2) 工具集成（计算器 / 知识库 / 当前时间）
3) Self-Refine（对最终答案做结构化补全）
"""

from __future__ import annotations

import argparse
import ast
import operator
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable


# ====== 工具层 ======


def safe_calculator(expression: str) -> str:
    """安全计算四则表达式（不允许任意代码执行）。"""

    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](_eval(node.operand))
        raise ValueError("仅支持数字与 + - * / ** 运算")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval(tree.body)
        if result.is_integer():
            return str(int(result))
        return f"{result:.6g}"
    except Exception as exc:
        return f"计算失败: {exc}"


def kb_search(query: str) -> str:
    """极简本地知识库检索（用于课堂演示）。"""

    knowledge = {
        "rag": "RAG（检索增强生成）= 先检索可信知识，再生成回答，重点是降低幻觉与可追溯。",
        "react": "ReAct = Reason + Act，通过多步推理和工具调用逐步完成复杂任务。",
        "agent": "Agent通常包含：规划器、工具调用器、记忆与反馈机制。",
        "self-refine": "Self-Refine是先生成草稿，再根据检查规则迭代优化输出质量。",
        "crewai": "CrewAI强调多角色协作（研究员、分析师、写作者）来分工完成任务。",
    }

    tokens = re.findall(r"[a-zA-Z\-\u4e00-\u9fff]+", query.lower())
    hits = []
    for key, value in knowledge.items():
        if any(key in tok or tok in key for tok in tokens):
            hits.append(f"[{key}] {value}")

    if hits:
        return "\n".join(hits)
    return "未命中知识库关键词。可尝试：RAG / ReAct / Agent / Self-Refine / CrewAI"


def current_time(_: str = "") -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[[str], str]


# ====== Agent层 ======


@dataclass
class StepRecord:
    step: int
    thought: str
    action: str
    action_input: str
    observation: str


@dataclass
class ReActAgent:
    max_steps: int = 5
    trace: bool = True
    tools: dict[str, Tool] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.tools:
            self.tools = {
                "calculator": Tool("calculator", "计算数学表达式", safe_calculator),
                "kb_search": Tool("kb_search", "检索本地知识库", kb_search),
                "current_time": Tool("current_time", "获取当前时间", current_time),
            }

    def run(self, user_query: str) -> str:
        records: list[StepRecord] = []
        used_actions: set[str] = set()
        draft_answer = ""

        for step in range(1, self.max_steps + 1):
            thought, action, action_input = self._plan(user_query, records, used_actions)

            if action == "finish":
                draft_answer = action_input
                if self.trace:
                    print(f"Step {step} | Thought: {thought}")
                    print(f"Step {step} | Action: finish")
                break

            tool = self.tools.get(action)
            if not tool:
                observation = f"未知工具: {action}"
            else:
                observation = tool.func(action_input)
                used_actions.add(action)

            record = StepRecord(
                step=step,
                thought=thought,
                action=action,
                action_input=action_input,
                observation=observation,
            )
            records.append(record)

            if self.trace:
                print(f"Step {step} | Thought: {thought}")
                print(f"Step {step} | Action: {action} -> {action_input}")
                print(f"Step {step} | Observation: {observation}\n")

        if not draft_answer:
            draft_answer = self._synthesize_from_records(user_query, records)

        refined = self._self_refine(user_query, draft_answer, records)

        if self.trace:
            print("Draft Answer:")
            print(draft_answer)
            print("\nRefined Answer:")

        return refined

    def _plan(
        self,
        query: str,
        records: list[StepRecord],
        used_actions: set[str],
    ) -> tuple[str, str, str]:
        # 1) 先看是否有算式
        expr = self._extract_expression(query)
        if expr and "calculator" not in used_actions:
            return (
                "用户问题包含算式，先调用计算器得到准确结果。",
                "calculator",
                expr,
            )

        # 2) 再看是否包含知识点
        if self._need_kb(query) and "kb_search" not in used_actions:
            return (
                "问题涉及概念解释，调用知识库补充事实依据。",
                "kb_search",
                query,
            )

        # 3) 时间相关
        if self._need_time(query) and "current_time" not in used_actions:
            return (
                "问题可能涉及当前时间，调用时间工具。",
                "current_time",
                "",
            )

        # 4) 结束并总结
        return (
            "证据已足够，输出最终回答。",
            "finish",
            self._synthesize_from_records(query, records),
        )

    @staticmethod
    def _extract_expression(query: str) -> str:
        # 提取简单数学表达式
        candidates = re.findall(r"[\d\s\(\)\+\-\*/\.\*\*]+", query)
        for cand in candidates:
            cleaned = cand.strip()
            if len(cleaned) >= 3 and any(op in cleaned for op in ["+", "-", "*", "/"]):
                return cleaned
        return ""

    @staticmethod
    def _need_kb(query: str) -> bool:
        keywords = ["rag", "react", "agent", "智能体", "自我优化", "self-refine", "crewai"]
        q = query.lower()
        return any(k in q for k in keywords)

    @staticmethod
    def _need_time(query: str) -> bool:
        keywords = ["几点", "现在", "时间", "today", "now", "日期"]
        q = query.lower()
        return any(k in q for k in keywords)

    @staticmethod
    def _synthesize_from_records(query: str, records: list[StepRecord]) -> str:
        if not records:
            return "我需要更多信息才能回答该问题。"

        calc_result = None
        kb_result = None
        time_result = None

        for r in records:
            if r.action == "calculator":
                calc_result = r.observation
            elif r.action == "kb_search":
                kb_result = r.observation
            elif r.action == "current_time":
                time_result = r.observation

        parts = [f"针对你的问题：{query}"]
        if kb_result:
            parts.append(f"概念依据：{kb_result}")
        if calc_result:
            parts.append(f"计算结果：{calc_result}")
        if time_result:
            parts.append(f"当前时间：{time_result}")

        if len(parts) == 1:
            parts.append("已完成推理，但未触发有效工具。")

        return "\n".join(parts)

    @staticmethod
    def _self_refine(query: str, draft: str, records: list[StepRecord]) -> str:
        """最小可用 Self-Refine：检查结构完整性并补全。"""

        refined_sections = []

        # 结论
        if "【结论】" in draft:
            refined_sections.append(draft)
        else:
            refined_sections.append(f"【结论】{draft.splitlines()[0] if draft else '已完成任务。'}")

        # 依据
        evidence_lines = [f"- Step {r.step}: {r.action} => {r.observation}" for r in records]
        if evidence_lines:
            refined_sections.append("【依据】\n" + "\n".join(evidence_lines[:4]))
        else:
            refined_sections.append("【依据】未调用到有效工具，建议补充上下文。")

        # 建议
        suggestion = (
            "【建议】若用于企业生产环境，请增加："
            "1) 外部检索工具；2) 错误重试；3) 审计日志；4) 成本与延迟监控。"
        )
        refined_sections.append(suggestion)

        return "\n\n".join(refined_sections)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab3: ReAct Agent demo")
    parser.add_argument("--query", default="", help="要处理的问题；为空时进入交互模式")
    parser.add_argument("--max-steps", type=int, default=5, help="最大ReAct步数")
    parser.add_argument("--no-trace", action="store_true", help="不打印中间Thought/Action/Observation")
    return parser.parse_args()


def interactive_mode(agent: ReActAgent) -> None:
    while True:
        query = input("\n请输入问题（exit退出）: ").strip()
        if query.lower() in {"exit", "quit", "q"}:
            print("已退出。")
            break
        if not query:
            continue
        result = agent.run(query)
        print(result)


def main() -> None:
    args = parse_args()
    agent = ReActAgent(max_steps=args.max_steps, trace=not args.no_trace)

    if args.query:
        result = agent.run(args.query)
        print(result)
    else:
        interactive_mode(agent)


if __name__ == "__main__":
    main()
