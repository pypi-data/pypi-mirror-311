"""Logging setup."""

import logging
from typing import ClassVar


class EmojiLevelFormatter(logging.Formatter):
    """Logging formater with emojis."""

    emojis: ClassVar[dict[int, str]] = {
        logging.DEBUG: "🔬",
        logging.INFO: "ℹ️",  # noqa: RUF001
        logging.WARNING: "⚠️",
        logging.ERROR: "💥",
        logging.CRITICAL: "☢️",
    }

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = self.emojis.get(record.levelno, record.levelname)
        return logging.Formatter.format(self, record)


def setup_logging(log_level: int = logging.INFO) -> None:
    logger = logging.getLogger()
    logger.setLevel(log_level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(EmojiLevelFormatter("%(levelname)s  %(message)s"))
    logger.addHandler(console_handler)
