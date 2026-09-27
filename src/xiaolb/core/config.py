# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class ApiConfig:
    base_url: str = "http://localhost:8080"
    send_endpoint: str = "/api/chat/send"
    timeout: float = 10.0
    extra_headers: dict[str, str] = field(default_factory=dict)


DEFAULT_CONFIG = ApiConfig()


__all__ = ["ApiConfig", "DEFAULT_CONFIG"]