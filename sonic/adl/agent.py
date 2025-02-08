from sonic.utils.genai.agents import Base, TextClassification
from sonic.adl.types import AgentDescription
from sonic.utils.logger import LOG


class Agent:
    def __init__(self, agent_description: AgentDescription):
        self.description = agent_description
        user_message = self.description.user_message
        if len(user_message) == 0:
            for input_name, _ in self.description.inputs.items():
                user_message += f"{{{input_name}}} "

        self.agent = Base(
            name=self.description.name,
            system_message=self.description.system_message,
            output_format=self.description.output_model,
            user_message=user_message,
        )

        self.guardrails = {}

        for guardrail in self.description.guardrails:
            if guardrail.name in self.guardrails:
                raise ValueError(f"Guardrail {guardrail.name} already exists")

            self.guardrails[guardrail.name] = {
                "guardrail": TextClassification(
                    name=guardrail.name,
                    system_message=guardrail.system_message,
                    class_labels=guardrail.labels,
                ),
                "rejection_labels": guardrail.rejection_labels,
            }

    def run(self, **kwargs):
        result = self.agent.run(**kwargs)
        LOG.debug(f"Result: {result}")
        for guardrail_name, guardrail_config in self.guardrails.items():
            LOG.debug(f'Applying guardrail: "{guardrail_name}"')

            LOG.debug(f"Guardrail: {guardrail_config}")

            guardrail = guardrail_config["guardrail"]
            output = guardrail.classify(text=str(result))

            if output not in guardrail.labels:
                raise ValueError(
                    f"Invalid label: {output}, expected: {guardrail.labels}"
                )

            if output in guardrail_config["rejection_labels"]:
                raise ValueError(
                    f"Rejected label: {output} for guardrail: {guardrail.name}, output: {output}"
                )

        LOG.info(f"All guardrails passed!")
        return result

    def update_system_message(self, system_message: str):
        self.agent.system_message = system_message  # type: ignore
        self.description.system_message = system_message
