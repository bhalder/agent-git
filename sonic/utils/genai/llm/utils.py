import json
import re

from litellm.types.utils import ModelResponse
from pydantic import BaseModel
from sonic.utils.logger import LOG


def get_content(response: ModelResponse) -> str:
    if response.choices:
        return response["choices"][0]["message"]["content"]
    return ""


def extract_json(response_text: str) -> dict:
    try:
        # Extract the JSON part using regex
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            json_object = json.loads(match.group(0))
            return json_object
    except json.JSONDecodeError:
        pass
    raise ValueError("No valid JSON object found in the response.")


def get_content_json(response: ModelResponse) -> dict:
    response_text = get_content(response)
    LOG.debug(f"Response text: {response_text}")
    return extract_json(response_text)


def get_pydantic_object(
    response: ModelResponse, pydantic_class: type[BaseModel]
) -> BaseModel:
    json_object = get_content_json(response)
    return pydantic_class(**json_object)
