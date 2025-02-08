from typing import List, Type, cast

from sonic.utils.genai.agents import Base
from pydantic import BaseModel


class TextClassificationResult(BaseModel):
    label: str
    explanation: str


class TextClassification(Base):
    class_labels: List[str]
    output_format: Type[BaseModel] = TextClassificationResult
    user_message: str = "Classify Text into one of the\nLabels:{labels}\n Text:{text}"

    @property
    def labels(self):
        return ", ".join(self.class_labels)

    def classify(self, text: str) -> str:
        response_object = cast(
            self.output_format,  # type: ignore
            self.run(labels=self.labels, text=text),
        )

        if response_object.label not in self.class_labels:
            raise ValueError(f"Invalid label: {response_object.label}")
        return response_object.label
