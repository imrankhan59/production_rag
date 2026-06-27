import logging

from rag_project.observability.formatter import StandardFormatter


def configure_logging() -> None:
    """
    Configure application logging.

    This function should be called only once during
    application startup.
    """

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StandardFormatter())

    root_logger = logging.getLogger()

    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)