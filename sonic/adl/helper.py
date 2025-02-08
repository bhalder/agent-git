from adl.types import AgentDescription
from sonic.utils.genai.agents import Base


def get_agent_from_description(description: AgentDescription) -> Base:
    user_message = description.user_message
    if len(user_message) == 0:
        for input_name, _ in description.inputs.items():
            user_message += f"{{{input_name}}} "

    return Base(
        name=description.name,
        system_message=description.system_message,
        output_model=description.output_model,
        user_message=user_message,
    )
