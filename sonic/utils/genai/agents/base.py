from typing import Any, List, Type

from sonic.utils.genai.llm import LLM, get_pydantic_object
from sonic.utils.genai.prompts import SystemPrompt, UserPrompt
from sonic.utils.logger import LOG
from litellm import Message
from pydantic import BaseModel


class Base(LLM):
    name: str = ""
    system_message: str = ""
    user_message: str = ""
    output_format: Type[BaseModel]

    def _enrichment_key(self, key: str) -> str:
        return f"ai_{self.name}_{key}".lower()

    @property
    def system_prompt(self) -> SystemPrompt:
        """
        Dynamically generates the system prompt using output_format's schema
        to include structured instructions about the expected JSON response.
        """
        format_instructions = ""
        if self.output_format:
            # Extract schema from output_format
            schema = self.output_format.model_json_schema()
            format_instructions = """
            The response should be a valid JSON object with the following structure:\n\n
            """
            for field_name, field_info in schema.get("properties", {}).items():
                field_details = f"- `{field_name}`: {field_info.get('type', 'unknown')}"

                # Add description if available
                if "description" in field_info:
                    field_details += f" - {field_info['description']}"

                # Add default value if available
                if "default" in field_info:
                    field_details += f" (Default: {field_info['default']})"
                else:
                    # Check if the field is required
                    required = field_name in schema.get("required", [])
                    field_details += " (Required)" if required else " (Optional)"

                format_instructions += field_details + "\n"

            format_instructions += (
                "\nEnsure your response strictly adheres to this structure"
                " and is always a valid JSON."
                "There should not be  any formatting directives e.g. ```json."
                "If you cannot comply, respond with an error message explaining why."
            )

        return SystemPrompt(
            prompt=f"{self.system_message.strip()}\n\n{format_instructions.strip()}"
        )

    @property
    def user_prompt(self) -> UserPrompt:
        return UserPrompt(prompt=self.user_message)

    def generate_messages(self, **kwargs) -> List[Message]:
        return [self.system_prompt.message(), self.user_prompt.message(**kwargs)]

    def pre_run(self, **kwargs: Any) -> None:
        """Hook for pre-run tasks. Override this in subclasses if needed."""
        pass

    def post_run(self, result: Any) -> None:
        """Hook for post-run tasks. Override this in subclasses if needed."""
        pass

    def run(self, **kwargs) -> Any:
        self.pre_run(**kwargs)
        try:
            messages = self.generate_messages(**kwargs)
            response = self.generate(messages)
            LOG.debug(response)
            result = get_pydantic_object(response, self.output_format)

        except Exception as e:
            raise e

        self.post_run(result)
        return result
