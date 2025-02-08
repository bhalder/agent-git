from typing import Any, List, Type

from sonic.utils.genai.llm import LLM, pydantic_object
from sonic.utils.genai.prompts import SystemPrompt, UserPrompt
from sonic.utils.logger import LOG
from litellm import Message
from pydantic import BaseModel


class Base(LLM):
    name: str = ""
    system_message: str = ""
    user_message: str = ""
    output_model: Type[BaseModel]

    def _enrichment_key(self, key: str) -> str:
        return f"ai_{self.name}_{key}".lower()

    @property
    def system_prompt(self) -> SystemPrompt:
        _instructions = ""
        if self.output_model:
            schema = self.output_model.model_json_schema()
            _instructions = """
            The response should be a valid JSON object with the following structure:\n\n
            """
            for field_name, field_info in schema.get("properties", {}).items():
                field_details = f"- `{field_name}`: {field_info.get('type', 'unknown')}"

                # Add description if available
                if "description" in field_info:
                    field_details += f" - {field_info['description']}"

                if "default" in field_info:
                    field_details += f" (Default: {field_info['default']})"
                else:
                    required = field_name in schema.get("required", [])
                    field_details += " (Required)" if required else " (Optional)"

                _instructions += field_details + "\n"

            _instructions += (
                "\nEnsure your response strictly adheres to this structure"
                " and is always a valid JSON."
                "There should not be  any formatting directives e.g. ```json."
                "If you cannot comply, respond with an error message explaining why."
            )

        return SystemPrompt(
            prompt=f"{self.system_message.strip()}\n\n{_instructions.strip()}"
        )

    @property
    def user_prompt(self) -> UserPrompt:
        return UserPrompt(prompt=self.user_message)

    def generate_messages(self, **kwargs) -> List[Message]:
        return [self.system_prompt.message(), self.user_prompt.message(**kwargs)]

    def pre(self, **kwargs: Any) -> None:
        """Hook for pre-run tasks"""
        pass

    def post(self, result: Any) -> None:
        """Hook for post-run tasks"""
        pass

    def run(self, **kwargs) -> Any:
        self.pre(**kwargs)
        try:
            messages = self.generate_messages(**kwargs)
            response = self.generate(messages)
            LOG.debug(response)
            result = pydantic_object(response, self.output_model)

        except Exception as e:
            raise e

        self.post(result)
        return result
