from re import A
from adl.types import (
    AgentDescription,
    TypeDescription,
    OutputType,
    ClassificationGuardrail,
)
from adl.helper import get_agent_from_description
from adl.agent import Agent


def test_create_run_agent():
    agent_description = AgentDescription(
        name="test",
        example_generator="test",
        system_message="What is the sum of 1 and 1?",
        llm="gpt-4o",
        inputs={
            "test": TypeDescription(
                type=OutputType.INT, description="test", default="1"
            )
        },
        outputs={
            "test": TypeDescription(
                type=OutputType.INT, description="test", default="1"
            )
        },
    )

    agent = get_agent_from_description(agent_description)

    assert agent.name == "test"
    assert agent.system_message == "What is the sum of 1 and 1?"
    assert agent.output_format().dict()["test"] == 1
    assert agent.model == "gpt-4o"

    agent = Agent(agent_description)

    assert agent.agent.name == "test"
    assert agent.agent.system_message == "What is the sum of 1 and 1?"
    assert agent.agent.output_format().dict()["test"] == 1
    assert agent.agent.model == "gpt-4o"


def test_agent_with_guardrails():
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
                system_message="Does the output have a field called is_email?",
            ),
            ClassificationGuardrail(
                name="Output checker - value",
                system_message="Is the value of is_email True or False?",
            ),
        ],
    )

    agent = Agent(ad)

    assert agent.agent.name == "email classifier"
    assert (
        agent.agent.system_message == "you help classify emails as sales email or not"
    )
    assert agent.agent.output_format().dict()["is_email"] == "False"
    assert agent.agent.model == "gpt-4o"
    assert len(agent.guardrails) == 2
    assert (
        agent.guardrails["Output checker - key"]["guardrail"].name
        == "Output checker - key"
    )
    assert (
        agent.guardrails["Output checker - value"]["guardrail"].name
        == "Output checker - value"
    )
