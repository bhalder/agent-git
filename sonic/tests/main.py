from adl.types import (
    AgentDescription,
    TypeDescription,
    OutputType,
    ClassificationGuardrail,
)
from adl.agent import Agent

ad = AgentDescription(
    name="email classifier",
    example_generator="generate a sales email",
    inputs={
        "email": TypeDescription(
            type=OutputType.STRING, description="email to be classified", default=""
        )
    },
    outputs={
        "is_email": TypeDescription(
            type=OutputType.BOOL, description="True or False", default="False"
        )
    },
    llm="gpt-4o",
    system_message="you help classify emails as sales email or not",
    guardrails=[
        ClassificationGuardrail(
            name="Output checker - key",
            system_message="Does the text string have a key 'is_email'?",
        ),
        ClassificationGuardrail(
            name="Output checker - value",
            system_message="Does text string have a value of True or False?",
        ),
        ClassificationGuardrail(
            name="No invalid strings",
            system_message="Is there anything apart from 'is_email', '=', and 'True' or 'False'?",
        ),
    ],
)
agent = Agent(ad)
agent.run(email="Can you send me the details of the product? and the price?")
