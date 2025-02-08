from typing import Optional

from decouple import config  # type: ignore

# NOTE : here we have add the type: ignore to each line
# top-level # type : ignore causes mypy not being able to find Config class


class Config:
    # Logging configuration
    LOG_LEVEL: str = config("LOG_LEVEL", "INFO")  # type: ignore
