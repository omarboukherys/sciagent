import asyncio

import opik
from opik.evaluation import evaluate

from sciagents.config import settings  # noqa: F401  (loads Opik env vars)
from sciagents.application.conversation_service.generate_response import generate_response
import os
os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY


def evaluation_task(item: dict) -> dict:
    """Run the agent on one dataset item and return input/output for scoring."""
    scientist_id = item["scientist_id"]
    question = item["question"]

    # generate_response is async; run it synchronously here
    answer = asyncio.run(
        generate_response(
            scientist_id=scientist_id,
            message=question,
            thread_id=f"eval-{scientist_id}",
        )
    )

    return {
        "input": question,
        "output": answer,
    }


# --- The LLM-as-judge model: point Opik's judges at Groq ---
from opik.evaluation.metrics import AnswerRelevance, Hallucination

JUDGE_MODEL = "groq/llama-3.3-70b-versatile"

metrics = [
    AnswerRelevance(model=JUDGE_MODEL, require_context=False),
    Hallucination(model=JUDGE_MODEL),
]


def main():
    client = opik.Opik()
    dataset = client.get_dataset(name="sciagents-eval")

    evaluate(
        dataset=dataset,
        task=evaluation_task,
        scoring_metrics=metrics,
        experiment_name="sciagents-baseline",
    )


if __name__ == "__main__":
    main()