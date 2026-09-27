#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Dodotry
Date: 2026-09-27 14:58:24
LastEditors: Dodotry
LastEditTime: 2026-09-27 15:14:00
'''

from typing import Any

from PySide6.QtCore import QThread, Signal
from loguru import logger

from .api_client import ApiClient
from .config import ApiConfig


class SendWorker(QThread):
    progress = Signal(str)
    result_one = Signal(str, bool, str)
    finished_all = Signal(int, int, int)

    def __init__(
        self,
        target_ids: list[str],
        content: str,
        config: ApiConfig | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.target_ids = target_ids
        self.content = content
        self.config = config or ApiConfig()
        self._client = ApiClient(self.config)

    def run(self) -> None:
        total = len(self.target_ids)
        success = 0
        fail = 0
        logger.info("开始批量发送: 目标数={} 内容长度={}", total, len(self.content))
        for index, target_id in enumerate(self.target_ids, start=1):
            self.progress.emit(f"正在发送 ({index}/{total}): {target_id}")
            result: dict[str, Any] = self._client.send_message(target_id, self.content)
            ok = bool(result.get("success"))
            self.result_one.emit(target_id, ok, str(result.get("body", "")))
            if ok:
                success += 1
            else:
                fail += 1
        logger.info("批量发送完成: 总计={} 成功={} 失败={}", total, success, fail)
        self.finished_all.emit(total, success, fail)


__all__ = ["SendWorker"]