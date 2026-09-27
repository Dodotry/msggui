# -*- coding: utf-8 -*-

import sys
from pathlib import Path

from loguru import logger

_LOG_DIR = Path(__file__).resolve().parents[3] / "logs"


def setup_logger() -> "logger":  # type: ignore[name-defined]
    logger.remove()
    _LOG_DIR.mkdir(exist_ok=True)
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan> - {message}",
    )
    logger.add(
        _LOG_DIR / "chat_sender_{time:YYYY-MM-DD}.log",
        level="DEBUG",
        rotation="1 day",
        retention="30 days",
        encoding="utf-8",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} - {message}",
    )
    return logger


__all__ = ["setup_logger", "logger"]
