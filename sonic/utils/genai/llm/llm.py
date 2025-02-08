from typing import List, Optional, cast

from sonic.utils.logger import LOG
from litellm import Message, completion
from litellm.cost_calculator import completion_cost
from litellm.types.utils import ModelResponse, Usage
from pydantic import BaseModel


class LLM(BaseModel):
    model: str = "gpt-4o"
    api_key: str = ""
    temperature: float = 0.2
    max_tokens: int = 1000
    top_p: float = 0.8

    base_url: str = ""

    def generate(self, messages: List[Message]) -> ModelResponse:
        LOG.debug(f"Generating response using model {self.model}")
        completion_response = completion(  # type: ignore
            model=self.model,
            messages=messages,
            api_key=self.api_key,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
        )
        response: ModelResponse = cast(ModelResponse, completion_response)
        cost: Optional[float] = None
        response_ms: Optional[int] = None

        # Track the event in PostHog
        if response.usage:  # type: ignore
            usage: Usage = response.usage  # type: ignore
            cost = completion_cost(response)

            LOG.debug(f"Usage: {usage}")
            LOG.debug(f"Cost: {cost}")

        if response._response_ms:  # type: ignore
            response_ms = response._response_ms  # type: ignore
            LOG.debug(f"Response time: {response_ms}ms")

        LOG.debug(f"Generated response using model {self.model}")
        return response
