#!/usr/bin/env python3
"""Lab 1 - Prompt Engineering Playground.

对比 Zero-shot / Few-shot / CoT / Role Prompt 的输出差异。
如果检测到 OPENAI_API_KEY，则调用真实模型；否则使用本地 mock。
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import Optional


DEFAULT_QUESTION = "请为 MBA 学生解释为什么 RAG 能降低大模型幻觉，并给出一个零售行业场景。"


@dataclass
class PromptVariant:
    name: str
    system_prompt: Optional[str]
    user_prompt: str


class LLMGateway:
    """统一封装真实模型与本地 mock。"""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.2) -> None:
        self.model = model
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._client = None

        if self.api_key:
            try:
                from openai import OpenAI

                self._client = OpenAI(api_key=self.api_key)
            except Exception:
                # 即使 openai 包不可用，也不影响课堂演示
                self._client = None

    @property
    def is_real_model(self) -> bool:
        return self._client is not None

    def generate(self, variant_name: str, user_prompt: str, system_prompt: Optional[str] = None) -> str:
        if self._client:
            return self._call_openai(user_prompt=user_prompt, system_prompt=system_prompt)
        return self._mock_response(variant_name=variant_name, user_prompt=user_prompt)

    def _call_openai(self, user_prompt: str, system_prompt: Optional[str]) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        return (response.choices[0].message.content or "").strip()

    def _mock_response(self, variant_name: str, user_prompt: str) -> str:
        topic = user_prompt.strip().replace("\n", " ")[:100]

        if variant_name == "Zero-shot":
            return (
                "RAG（检索增强生成）通过在回答前先查找外部资料，减少模型仅靠参数记忆胡乱补全的概率。"
                "在零售场景中，可先检索商品知识库（库存、价格、活动规则），再生成客服答复，"
                "从而降低‘编造优惠规则’这类幻觉。"
            )

        if variant_name == "Few-shot":
            return (
                "【定义】RAG = 检索 + 生成。\n"
                "【机制】回答前引用企业知识库，减少无依据输出。\n"
                "【零售案例】客服问‘这款咖啡豆是否有机认证？’系统先检索商品主数据，再作答。\n"
                "【价值】准确率提升、投诉率下降、可审计。"
            )

        if variant_name == "CoT":
            return (
                "步骤1：识别问题根因——幻觉来自‘无证据生成’。\n"
                "步骤2：引入RAG——先检索可信文档，再约束生成。\n"
                "步骤3：映射零售——客服回复基于实时库存与活动政策。\n"
                "步骤4：结论——RAG用‘证据链’替代‘猜测链’，显著降低幻觉。"
            )

        if variant_name == "Role Prompt":
            return (
                "作为管理咨询顾问，我建议从四层落地：\n"
                "1) 业务目标：降低客服错误答复率；\n"
                "2) 数据资产：打通商品、促销、物流知识库；\n"
                "3) 流程改造：回答前必须检索证据；\n"
                "4) ROI度量：首解率、人工转接率、投诉率。"
                f"\n（问题上下文：{topic}）"
            )

        return "[mock] 未识别的Prompt策略。"


def build_variants(question: str) -> list[PromptVariant]:
    zero_shot = PromptVariant(
        name="Zero-shot",
        system_prompt=None,
        user_prompt=question,
    )

    few_shot_examples = """
示例1：
问题：什么是RAG？
回答：RAG是先检索外部知识，再用LLM组织答案的方法，可减少事实性错误。

示例2：
问题：RAG在医疗行业的价值？
回答：可先检索临床指南和医院内部流程，再生成解释，从而降低错误建议风险。
""".strip()

    few_shot = PromptVariant(
        name="Few-shot",
        system_prompt="你是一个教学助理，回答要结构化、可教学。",
        user_prompt=(
            f"{few_shot_examples}\n\n"
            f"现在请按【定义-机制-案例-价值】结构回答：\n问题：{question}"
        ),
    )

    cot = PromptVariant(
        name="CoT",
        system_prompt="你是一个严谨的分析师，请按步骤推理后给出结论。",
        user_prompt=(
            "请先分步骤思考，再给出最终回答。\n"
            "输出格式：\n"
            "步骤1...\n步骤2...\n步骤3...\n结论...\n\n"
            f"问题：{question}"
        ),
    )

    role_prompt = PromptVariant(
        name="Role Prompt",
        system_prompt=(
            "你是麦肯锡风格的管理咨询顾问，"
            "擅长将AI技术翻译为业务落地方案，回答要有框架、有指标。"
        ),
        user_prompt=question,
    )

    return [zero_shot, few_shot, cot, role_prompt]


def run_experiment(question: str, model: str, temperature: float) -> None:
    llm = LLMGateway(model=model, temperature=temperature)
    variants = build_variants(question)

    engine = "真实模型(OpenAI)" if llm.is_real_model else "本地Mock引擎"
    print(f"\n=== Prompt Playground 启动 | 引擎: {engine} ===")
    print(f"问题: {question}\n")

    for variant in variants:
        print("=" * 20, variant.name, "=" * 20)
        answer = llm.generate(
            variant_name=variant.name,
            user_prompt=variant.user_prompt,
            system_prompt=variant.system_prompt,
        )
        print(answer)
        print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prompt Engineering Playground")
    parser.add_argument("--question", default=DEFAULT_QUESTION, help="要测试的问题")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI模型名")
    parser.add_argument("--temperature", type=float, default=0.2, help="采样温度")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_experiment(question=args.question, model=args.model, temperature=args.temperature)


if __name__ == "__main__":
    main()
