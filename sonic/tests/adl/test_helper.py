from adl.types import AgentDescription, TypeDescription, OutputType


def test_agent_description():
    agent_description = AgentDescription(
        name="test",
        example_generator="test",
        system_message="test",
        llm="test",
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
    assert agent_description.to_dict() == {
        "name": "test",
        "example_generator": "test",
        "system_message": "test",
        "llm": "test",
        "inputs": {"test": {"type": "INT", "description": "test", "default": "1"}},
        "outputs": {"test": {"type": "INT", "description": "test", "default": "1"}},
        "guardrails": [],
        "user_message": "",
    }
    assert (
        AgentDescription.from_dict(
            {
                "name": "test",
                "example_generator": "test",
                "system_message": "test",
                "llm": "test",
                "inputs": {
                    "test": {"type": "INT", "description": "test", "default": "1"}
                },
                "outputs": {
                    "test": {"type": "INT", "description": "test", "default": "1"}
                },
                "guardrails": [],
                "user_message": "",
            }
        )
        == agent_description
    )
    assert agent_description.inputs["test"].dict() == {
        "type": "INT",
        "description": "test",
        "default": "1",
    }
    assert agent_description.outputs["test"].dict() == {
        "type": "INT",
        "description": "test",
        "default": "1",
    }
    assert (
        TypeDescription.check_default_matches_type("1", {"type": OutputType.INT}) == "1"
    )
    assert (
        TypeDescription.check_default_matches_type("1.0", {"type": OutputType.FLOAT})
        == "1.0"
    )
    try:
        TypeDescription.check_default_matches_type("1.0", {"type": OutputType.INT})
    except ValueError as e:
        assert str(e) == "Default value 1.0 is not valid for type INT"
    try:
        TypeDescription.check_default_matches_type("1", {"type": OutputType.FLOAT})
    except ValueError as e:
        assert str(e) == "Default value 1 is not valid for type FLOAT"
    try:
        TypeDescription.check_default_matches_type("a", {"type": OutputType.INT})
    except ValueError as e:
        assert str
