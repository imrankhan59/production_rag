import logging


class StandardFormatter(logging.Formatter):
    """
    Standard formatter for application logs.

    This formatter is responsible only for defining
    the output format of log records.
    """

    DEFAULT_FORMAT = (
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "%(message)s"
    )

    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self) -> None:
        super().__init__(
            fmt=self.DEFAULT_FORMAT,
            datefmt=self.DEFAULT_DATE_FORMAT,
        )