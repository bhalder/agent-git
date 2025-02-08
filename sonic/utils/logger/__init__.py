import logging

from sonic.utils.config import Config

log_format = (
    "%(asctime)s - %(name)s - %(levelname)s - (%(filename)s:%(lineno)d) - %(message)s"
)

_LOG = None


def init_logging(level: str = Config.LOG_LEVEL) -> logging.Logger:
    global _LOG  # Mark logger as initialized

    if _LOG:
        return _LOG

    # Create a global logger instance
    _LOG = logging.getLogger(__name__)

    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    _LOG.addHandler(console_handler)

    logging.getLogger("sqlalchemy.engine.Engine").disabled = True

    # Set logger level and formatter for the global logger
    _LOG.setLevel(level)

    global LOG
    LOG = _LOG  # Assign to global LOG

    return _LOG


LOG = init_logging()
