import logging

from rag_project.observability.config import configure_logging


_configured = False


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.

    Logging is configured only once for the entire application.
    """

    global _configured

    if not _configured:
        configure_logging()
        _configured = True

    return logging.getLogger(name)