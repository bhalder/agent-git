from ast import List
from pydantic import BaseModel, Field, validator, create_model
from enum import Enum
from typing import Any, Dict, Tuple, Type


class OutputType(str, Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOL = "BOOL"

    def __str__(self):
        return self.value


class ClassificationGuardrail(BaseModel):
    name: str
    description: str = ""
    system_message: str
    labels: list[str] = ["True", "False"]
    rejection_labels: list[str] = ["False"]


class TypeDescription(BaseModel):
    type: OutputType = Field(..., description="The data type of the output")
    description: str = Field(..., description="Description of the data type")
    default: str = Field(
        ..., description="Default value as a string, which should match the type"
    )

    @validator("default")
    def check_default_matches_type(cls, v, values):
        if "type" in values:
            if values["type"] == OutputType.INT:
                if not v.isdigit():
                    raise ValueError(f"Default value {v} is not valid for type INT")
            elif values["type"] == OutputType.FLOAT:
                try:
                    float(v)
                except ValueError:
                    raise ValueError(f"Default value {v} is not valid for type FLOAT")
        return v

    def dict(self, **kwargs) -> dict:
        """
        Overrides the dict method to convert the OutputType enum to a string.
        """
        r = super().dict(
            **kwargs,
        )
        r["type"] = str(self.type)
        return r


class AgentDescription(BaseModel):
    name: str = Field(..., description="The name of the agent")
    example_generator: str = Field(
        ..., description="Reference to the example generator"
    )
    system_message: str = Field(
        ..., description="System message to be used by the agent"
    )
    user_message: str = Field(
        description="User message to be used by the agent", default=""
    )
    llm: str = Field(description="Large language model identifier", default="gpt-4")
    inputs: dict[str, TypeDescription] = Field(
        ..., description="Dictionary of input types with descriptions"
    )
    outputs: dict[str, TypeDescription] = Field(
        ..., description="Dictionary of output types with descriptions"
    )
    guardrails: list[ClassificationGuardrail] = Field(
        description="List of guardrails which the agent must satisfy",
        default_factory=list,
    )

    def to_dict(self) -> dict:
        """
        Converts the AgentDescription instance to a dictionary, including nested TypeDescription instances.
        """
        return {
            "name": self.name,
            "example_generator": self.example_generator,
            "system_message": self.system_message,
            "user_message": self.user_message,
            "llm": self.llm,
            "inputs": {k: v.dict() for k, v in self.inputs.items()},
            "outputs": {k: v.dict() for k, v in self.outputs.items()},
            "guardrails": [guardrail.dict() for guardrail in self.guardrails],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AgentDescription":
        """
        Converts a dictionary to an AgentDescription instance, including nested TypeDescription instances.
        """
        return AgentDescription(
            name=data["name"],
            example_generator=data["example_generator"],
            system_message=data["system_message"],
            user_message=data.get("user_message", ""),
            llm=data["llm"],
            inputs={k: TypeDescription(**v) for k, v in data["inputs"].items()},
            outputs={k: TypeDescription(**v) for k, v in data["outputs"].items()},
            guardrails=[
                ClassificationGuardrail(**guardrail) for guardrail in data["guardrails"]
            ],
        )

    def _get_model(self, source: dict) -> Type[BaseModel]:
        """
        Helper method to dynamically generate a Pydantic model based on the inputs or outputs dictionary.
        """
        fields: Dict[str, Tuple[Any, ...]] = {}

        for key, type_desc in source.items():
            # Map OutputType to Pydantic field types
            field_type = {
                OutputType.INT: (int, ...),
                OutputType.FLOAT: (float, ...),
                OutputType.STRING: (str, ...),
            }.get(
                type_desc.type, (str, ...)
            )  # Default to string type if undefined

            # Convert default value based on type, safely parsing numbers
            try:
                if type_desc.type == OutputType.INT:
                    default_value = int(type_desc.default)
                elif type_desc.type == OutputType.FLOAT:
                    default_value = float(type_desc.default)
                else:
                    default_value = type_desc.default
            except ValueError as e:
                raise ValueError(f"Error converting default value for {key}: {e}")

            # Add the field to the fields dictionary with additional Pydantic settings
            fields[key] = (
                field_type[0],
                Field(default=default_value, description=type_desc.description),
            )

        # Create the dynamic Pydantic model
        return create_model(  # type: ignore
            "DynamicModel", **fields  # type: ignore
        )

    @property
    def input_model(self) -> Type[BaseModel]:
        """
        Dynamically generates a Pydantic model based on the inputs dictionary.
        This model can be used to validate the inputs received for the agent.
        """
        return self._get_model(self.inputs)

    @property
    def output_model(self) -> Type[BaseModel]:
        """
        Dynamically generates a Pydantic model based on the outputs dictionary.
        This model can be used to validate the outputs received from the agent.
        """
        return self._get_model(self.outputs)

    class Config:
        validate_assignment = True
        anystr_strip_whitespace = True
