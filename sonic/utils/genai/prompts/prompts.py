from enum import Enum

from litellm import Message
from pydantic import BaseModel


class Role(Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class PromptTemplate(BaseModel):
    role: Role = Role.system
    prompt: str

    def fill(self, values: dict = {}) -> str:
        return self.prompt.format(**values)

    def message(self, **kwargs) -> Message:
        return Message(
            **{"role": self.role.value, "content": self.fill(kwargs)}  # type: ignore
        )


class UserPrompt(PromptTemplate):
    role: Role = Role.user


class SystemPrompt(PromptTemplate):
    role: Role = Role.system
