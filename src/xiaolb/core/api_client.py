# -*- coding: utf-8 -*-

import json
import urllib.error
import urllib.request
from typing import Any

from loguru import logger

from .config import ApiConfig


class ApiClient:
    def __init__(self, config: ApiConfig | None = None) -> None:
        self.config = config or ApiConfig()

    def send_message(self, target_id: str, content: str) -> dict[str, Any]:
        url = f"{self.config.base_url.rstrip('/')}{self.config.send_endpoint}"
        payload = {"target_id": target_id, "content": content}
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json; charset=utf-8")
        for key, value in self.config.extra_headers.items():
            req.add_header(key, value)
        logger.debug("POST {} target_id={}", url, target_id)
        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                logger.info("发送成功 target_id={} status={}", target_id, resp.status)
                return {"success": True, "status": resp.status, "body": body}
        except urllib.error.HTTPError as exc:
            logger.error("发送失败 target_id={} HTTP {}: {}", target_id, exc.code, exc.reason)
            return {"success": False, "status": exc.code, "body": str(exc.reason)}
        except urllib.error.URLError as exc:
            logger.error("发送失败 target_id={} URL错误: {}", target_id, exc.reason)
            return {"success": False, "status": 0, "body": str(exc.reason)}
        except Exception as exc:  # noqa: BLE001
            logger.exception("发送异常 target_id={}", target_id)
            return {"success": False, "status": 0, "body": f"{type(exc).__name__}: {exc}"}


__all__ = ["ApiClient"]