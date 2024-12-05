import json
import os
from typing import Literal, Optional, cast
from langevals_core.base_evaluator import (
    BaseEvaluator,
    EvaluatorEntry,
    EvaluationResult,
    LLMEvaluatorSettings,
    SingleEvaluationResult,
    EvaluationResultSkipped,
    Money,
    EvaluatorSettings
)
from pydantic import Field
import litellm
from litellm import Choices, Message
from litellm.files.main import ModelResponse
from litellm.cost_calculator import completion_cost



class CustomLLMScoreEntry(EvaluatorEntry):
    input: Optional[str] = None
    output: Optional[str] = None
    contexts: Optional[list[str]] = None


class CustomLLMScoreSettings(LLMEvaluatorSettings):
    prompt: str = Field(
        default="You are an LLM evaluator. Please score from 0.0 to 1.0 how likely the user is to be satisfied with this answer, from 0.0 being not satisfied at all to 1.0 being completely satisfied",
        description="The system prompt to use for the LLM to run the evaluation",
    )
    max_tokens: int = 8192


class CustomLLMScoreResult(EvaluationResult):
    score: float = Field(
        description="The score given by the LLM, according to the prompt"
    )


class CustomLLMScoreEvaluator(
    BaseEvaluator[CustomLLMScoreEntry, CustomLLMScoreSettings, CustomLLMScoreResult]
):
    """
    Use an LLM as a judge with custom prompt to do a numeric score evaluation of the message.
    """

    name = "LLM-as-a-Judge Score Evaluator"
    category = "custom"
    env_vars = []
    default_settings = CustomLLMScoreSettings()
    is_guardrail = False

    def evaluate(self, entry: CustomLLMScoreEntry) -> SingleEvaluationResult:
        vendor, model = self.settings.model.split("/")

        if self.env:
            for key, env in self.env.items():
                os.environ[key] = env

        content = ""
        if entry.input:
            content += f"# Input\n{entry.input}\n\n"
        if entry.output:
            content += f"# Output\n{entry.output}\n\n"
        if entry.contexts:
            content += f"# Contexts\n{'1. '.join(entry.contexts)}\n\n"

        if not content:
            return EvaluationResultSkipped(details="No content to evaluate")

        content += f"# Task\n{self.settings.prompt}"

        litellm_model = model if vendor == "openai" and model != "gpt-4o" else f"{vendor}/{model}"

        total_tokens = len(
            litellm.encode(
                model=litellm_model, text=f"{self.settings.prompt} {content}"
            )
        )
        max_tokens = min(self.settings.max_tokens, 32768)
        if total_tokens > max_tokens:
            return EvaluationResultSkipped(
                details=f"Total tokens exceed the maximum of {max_tokens}: {total_tokens}"
            )

        response = litellm.completion(
            model=litellm_model,
            messages=[
                {
                    "role": "system",
                    "content": self.settings.prompt + ". Always output a valid json for the function call",
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "evaluation",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "scratchpad": {
                                    "type": "string",
                                    "description": "use this field to break down the task and explain your reasoning in multiple sub-scores, using it to combine into a final score",
                                },
                                "final_score": {
                                    "type": "number",
                                    "description": "your final score for the task",
                                },
                            },
                            "required": ["scratchpad", "final_score"],
                        },
                        "description": "use this function to write your thoughts on the scratchpad, then decide on the final score with this json structure",
                    },
                },
            ],
            tool_choice={"type": "function", "function": {"name": "evaluation"}},  # type: ignore
        )

        response = cast(ModelResponse, response)
        choice = cast(Choices, response.choices[0])
        arguments = json.loads(
            cast(Message, choice.message).tool_calls[0].function.arguments
        )
        cost = completion_cost(completion_response=response)

        return CustomLLMScoreResult(
            score=arguments["final_score"],
            details=arguments["scratchpad"],
            cost=Money(amount=cost, currency="USD") if cost else None,
        )
