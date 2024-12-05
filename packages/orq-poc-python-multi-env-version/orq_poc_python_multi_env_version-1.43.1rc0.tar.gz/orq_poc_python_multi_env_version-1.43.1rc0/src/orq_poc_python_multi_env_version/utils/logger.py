"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

import httpx
import logging
import os
from typing import Any, Protocol


class Logger(Protocol):
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        pass


class NoOpLogger:
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        pass


def get_body_content(req: httpx.Request) -> str:
    return "<streaming body>" if not hasattr(req, "_content") else str(req.content)


def get_default_logger() -> Logger:
    if os.getenv("ORQ_DEBUG"):
        logging.basicConfig(level=logging.DEBUG)
        return logging.getLogger("orq_poc_python_multi_env_version")
    return NoOpLogger()
