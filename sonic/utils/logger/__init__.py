import logging

from sonic.utils.config import Config

log_format = (
    "%(asctime)s - %(name)s - %(levelname)s - (%(filename)s:%(lineno)d) - %(message)s"
)

_LOG = None  # Placeholder for the global logger


def init_logging(level: str = Config.LOG_LEVEL) -> logging.Logger:
    """
    Initializes the logging setup for the application with Datadog logging integration.

    Args:
        level (str): The logging level (default: INFO).
    """

    global _LOG  # Mark logger as initialized

    # Check if already initialized
    if _LOG:
        return _LOG  # Avoid re-initializing

    # Create a global logger instance
    _LOG = logging.getLogger(__name__)

    # Set up the basic Python logging configuration with format
    formatter = logging.Formatter(log_format)

    # Create and add a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    _LOG.addHandler(console_handler)

    logging.getLogger("sqlalchemy.engine.Engine").disabled = True

    # Set logger level and formatter for the global logger
    _LOG.setLevel(level)

    global LOG
    LOG = _LOG  # Assign to global LOG

    return _LOG


LOG = init_logging()  # Initialize the logger on module load
