import pytest
from pydantic import ValidationError
from adl.types import OutputType, TypeDescription, AgentDescription


# Tests for TypeDescription
def test_valid_type_description():
    try:
        td = TypeDescription(
            type=OutputType.INT, description="An integer output", default="10"
        )
        assert td.default == "10"
    except ValidationError:
        pytest.fail("Valid type description raised ValidationError unexpectedly!")


def test_invalid_default_value():
    with pytest.raises(ValidationError) as excinfo:
        TypeDescription(
            type=OutputType.INT, description="An integer output", default="ten"
        )
    assert "not valid for type INT" in str(excinfo.value)


def test_float_default_value_validation():
    # This should not raise an error
    td = TypeDescription(
        type=OutputType.FLOAT, description="A float output", default="10.5"
    )
    assert td.default == "10.5"
    # This should raise an error
    with pytest.raises(ValidationError):
        TypeDescription(
            type=OutputType.FLOAT,
            description="A float output",
            default="ten.point.five",
        )


# Tests for AgentDescription
def test_agent_description_to_dict():
    td = TypeDescription(
        type=OutputType.STRING, description="A string output", default="example"
    )
    agent = AgentDescription(
        name="Test Agent",
        example_generator="Example Generator",
        system_message="System Message",
        llm="LLM Identifier",
        inputs={"input1": td},
        outputs={"output1": td},
    )
    agent_dict = agent.to_dict()
    assert agent_dict["name"] == "Test Agent"
    assert agent_dict["inputs"]["input1"]["default"] == "example"


def test_agent_description_with_invalid_inputs():
    with pytest.raises(ValidationError):
        AgentDescription(
            name="Test Agent",
            example_generator="Example Generator",
            system_message="System Message",
            llm="LLM Identifier",
            inputs={  # type: ignore
                "input1": {
                    "type": "invalid_type",
                    "description": "Invalid",
                    "default": "example",
                }
            },
        )
