#!/usr/bin/env python3
"""Lab 4 - 多智能体协作示例（CrewAI + 本地回退模式）。"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass


DEFAULT_TOPIC = "为一家中型零售企业设计AI客服升级路线图"


@dataclass
class LocalOutputs:
    research: str
    strategy: str
    report: str


def local_researcher(topic: str) -> str:
    return (
        f"围绕主题《{topic}》的研究结论：\n"
        "1) 行业趋势：企业从FAQ机器人升级到可调用系统工具的Agent。\n"
        "2) 关键痛点：知识更新慢、答案不可追溯、人工客服成本高。\n"
        "3) 风险点：数据质量不足、权限治理不清、模型幻觉导致业务错误。"
    )


def local_strategist(topic: str, research: str) -> str:
    _ = research
    return (
        f"针对《{topic}》的策略建议：\n"
        "- 阶段1（0-30天）：梳理高频场景与知识库，建立RAG底座。\n"
        "- 阶段2（30-60天）：引入ReAct Agent，支持工具调用（订单、库存、政策）。\n"
        "- 阶段3（60-90天）：多智能体协作（研究/策略/质检）并接入审计监控。\n"
        "- KPI：首次解决率(FCR)、人工转接率、用户满意度(CSAT)、平均处理时长(AHT)。"
    )


def local_writer(topic: str, research: str, strategy: str) -> str:
    return (
        f"# 多智能体协作报告\n\n"
        f"## 主题\n{topic}\n\n"
        "## 执行摘要\n"
        "通过‘研究员-策略师-写作者’分工，能够提升报告结构化程度与可执行性。\n\n"
        "## 研究发现\n"
        f"{research}\n\n"
        "## 策略路线图\n"
        f"{strategy}\n\n"
        "## 下一步行动\n"
        "1. 明确数据责任人并建立知识库更新SLA。\n"
        "2. 先从单一高价值场景试点（如售后客服）。\n"
        "3. 引入审计日志与质量评估闭环。\n"
    )


def run_local_crew(topic: str) -> LocalOutputs:
    research = local_researcher(topic)
    strategy = local_strategist(topic, research)
    report = local_writer(topic, research, strategy)
    return LocalOutputs(research=research, strategy=strategy, report=report)


def can_run_crewai() -> tuple[bool, str]:
    try:
        import crewai  # noqa: F401
    except Exception as exc:
        return False, f"未安装crewai或导入失败: {exc}"

    if not os.getenv("OPENAI_API_KEY"):
        return False, "未检测到 OPENAI_API_KEY"

    return True, "ok"


def run_crewai(topic: str) -> str:
    """真实 CrewAI 流程（需要安装 crewai 且配置 API Key）。"""
    from crewai import Agent, Crew, Process, Task

    # 兼容较新版本 CrewAI 的 LLM 初始化方式
    try:
        from crewai import LLM

        llm = LLM(model=os.getenv("CREWAI_MODEL", "gpt-4o-mini"), temperature=0.2)
    except Exception:
        llm = os.getenv("CREWAI_MODEL", "gpt-4o-mini")

    researcher = Agent(
        role="行业研究员",
        goal="快速梳理主题相关趋势、挑战和风险",
        backstory="你擅长将复杂技术主题拆解为管理者可理解的洞察。",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    strategist = Agent(
        role="商业策略师",
        goal="把研究结论转化为可执行策略与KPI",
        backstory="你专注于90天落地路径与ROI设计。",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    writer = Agent(
        role="报告写作者",
        goal="产出结构清晰、可汇报的管理报告",
        backstory="你擅长高管摘要与行动建议写作。",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    task_research = Task(
        description=(
            "围绕主题 {topic}，输出：行业趋势、关键挑战、风险清单。"
            "请用要点列表。"
        ),
        expected_output="研究摘要（不少于5条要点）",
        agent=researcher,
    )

    task_strategy = Task(
        description=(
            "基于研究结果，设计90天实施路线图与核心KPI。"
            "强调可执行动作与里程碑。"
        ),
        expected_output="策略方案（阶段计划 + KPI）",
        agent=strategist,
        context=[task_research],
    )

    task_report = Task(
        description=(
            "将研究与策略整合为一份可向管理层汇报的Markdown报告，"
            "包含：执行摘要、关键发现、行动建议。"
        ),
        expected_output="完整Markdown报告",
        agent=writer,
        context=[task_research, task_strategy],
    )

    crew = Crew(
        agents=[researcher, strategist, writer],
        tasks=[task_research, task_strategy, task_report],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"topic": topic})
    return str(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab4: Multi-agent demo with CrewAI")
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help="协作任务主题")
    parser.add_argument(
        "--mode",
        choices=["auto", "local", "crewai"],
        default="auto",
        help="运行模式：auto优先crewai，否则回退local",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.mode == "local":
        outputs = run_local_crew(args.topic)
        print("[Mode] local")
        print("\n[Researcher Output]")
        print(outputs.research)
        print("\n[Strategist Output]")
        print(outputs.strategy)
        print("\n[Writer Output]")
        print(outputs.report)
        return

    if args.mode == "crewai":
        ok, reason = can_run_crewai()
        if not ok:
            raise RuntimeError(f"无法运行CrewAI模式: {reason}")
        print("[Mode] crewai")
        print(run_crewai(args.topic))
        return

    # auto mode
    ok, reason = can_run_crewai()
    if ok:
        print("[Mode] crewai (auto)")
        print(run_crewai(args.topic))
    else:
        print(f"[Mode] local (auto fallback, reason: {reason})")
        outputs = run_local_crew(args.topic)
        print("\n[Researcher Output]")
        print(outputs.research)
        print("\n[Strategist Output]")
        print(outputs.strategy)
        print("\n[Writer Output]")
        print(outputs.report)


if __name__ == "__main__":
    main()
