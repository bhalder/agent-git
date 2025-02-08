from typing import Optional

from decouple import config  # type: ignore

# NOTE : here we have add the type: ignore to each line
# top-level # type : ignore causes mypy not being able to find Config class


class Config:
    # Load values from environment variables or the .env file

    BASE_URL: str = config(
        "BASE_URL", default="http://localhost:8000", cast=str
    )  # type: ignore

    # Postgres specific config
    POSTGRES_USER: str = config("POSTGRES_USER", default="", cast=str)  # type: ignore
    POSTGRES_PASSWORD: Optional[str] = config(
        "POSTGRES_PASSWORD", default=None
    )  # type: ignore
    POSTGRES_HOST: Optional[str] = config("POSTGRES_HOST", default=None)  # type: ignore
    POSTGRES_PORT: Optional[int] = config(
        "POSTGRES_PORT", default=5432, cast=int
    )  # type: ignore

    # The  DB database name in postgres
    POSTGRES_DB: Optional[str] = config("POSTGRES_DB", default=None)  # type: ignore

    # common config
    ENVIRONMENT: Optional[str] = config(
        "ENVIRONMENT", default="development"
    )  # type: ignore

    APP_VERSION: Optional[str] = config(
        "APP_VERSION", default="<unknown>"
    )  # type: ignore

    # redis specific config
    CACHE_NAMESPACE: str = config("CACHE_NAMESPACE", "default")  # type: ignore

    CACHE_TTL: int = config("CACHE_TTL", 60, cast=int)  # type: ignore

    REDIS_HOST: str = config("REDIS_HOST", default=None, cast=str)  # type: ignore

    REDIS_DB: int = config("REDIS_DB", 0, cast=int)
    REDIS_PORT: int = config("REDIS_PORT", default=6379, cast=int)  # type: ignore

    # Logging configuration
    LOG_LEVEL: str = config("LOG_LEVEL", "INFO")  # type: ignore
