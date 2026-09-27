# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from loguru import logger
from qfluentwidgets import (
    BodyLabel,
    FluentIcon,
    LineEdit,
    PrimaryPushButton,
    StrongBodyLabel,
    TextEdit,
)

from ..core.config import ApiConfig
from ..core.sender import SendWorker
from .theme import make_app_icon


class MainWindow(QWidget):
    def __init__(self, config: ApiConfig | None = None, parent=None) -> None:
        super().__init__(parent)
        self.config = config or ApiConfig()
        self._worker: SendWorker | None = None
        self.setWindowTitle("聊天消息发送工具")
        self.setWindowIcon(make_app_icon())
        self.resize(720, 520)
        self._build_ui()
        self._connect_signals()
        self._refresh_send_state()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        top = QHBoxLayout()
        top.setSpacing(10)
        self.id_label = StrongBodyLabel("目标ID:")
        self.id_input = LineEdit()
        self.id_input.setPlaceholderText("输入群ID或用户ID，多个用逗号分隔")
        self.id_input.setClearButtonEnabled(True)
        self.send_button = PrimaryPushButton(FluentIcon.SEND, "发送")
        self.send_button.setFixedWidth(110)
        top.addWidget(self.id_label)
        top.addWidget(self.id_input, 1)
        top.addWidget(self.send_button)
        root.addLayout(top)

        root.addWidget(StrongBodyLabel("消息内容:"))
        self.content_input = TextEdit()
        self.content_input.setPlaceholderText("输入要发送的富文本消息内容...")
        self.content_input.setMinimumHeight(200)
        root.addWidget(self.content_input, 1)

        self.status_bar = BodyLabel("就绪：填写目标ID与消息内容后即可发送")
        self.status_bar.setObjectName("statusBar")
        self.status_bar.setWordWrap(True)
        font = QFont(self.status_bar.font())
        font.setPointSize(9)
        self.status_bar.setFont(font)
        self._apply_status_style("idle")
        root.addWidget(self.status_bar)

    def _connect_signals(self) -> None:
        self.id_input.textChanged.connect(self._refresh_send_state)
        self.content_input.textChanged.connect(self._refresh_send_state)
        self.send_button.clicked.connect(self._on_send_clicked)

    def _refresh_send_state(self) -> None:
        has_id = bool(self.id_input.text().strip())
        has_content = bool(self.content_input.toPlainText().strip())
        self.send_button.setEnabled(has_id and has_content)

    def _parse_target_ids(self) -> list[str]:
        raw = self.id_input.text().strip()
        normalized = raw.replace("，", ",").replace("\n", ",").replace(";", ",")
        return [item.strip() for item in normalized.split(",") if item.strip()]

    def _on_send_clicked(self) -> None:
        target_ids = self._parse_target_ids()
        content = self.content_input.toPlainText().strip()
        if not target_ids or not content:
            return
        self.send_button.setEnabled(False)
        self.id_input.setEnabled(False)
        self.content_input.setEnabled(False)
        self.status_bar.setText(f"准备发送给 {len(target_ids)} 个目标...")
        self._apply_status_style("running")
        logger.info("点击发送: 目标数={} 内容长度={}", len(target_ids), len(content))
        self._worker = SendWorker(target_ids, content, self.config, parent=self)
        self._worker.progress.connect(self._on_progress)
        self._worker.result_one.connect(self._on_result_one)
        self._worker.finished_all.connect(self._on_finished)
        self._worker.start()

    def _on_progress(self, message: str) -> None:
        self.status_bar.setText(message)

    def _on_result_one(self, target_id: str, ok: bool, body: str) -> None:
        flag = "成功" if ok else "失败"
        logger.debug("单条结果: {} -> {} ({})", target_id, flag, body[:120])

    def _on_finished(self, total: int, success: int, fail: int) -> None:
        self.status_bar.setText(
            f"发送完成：总计 {total} | 成功 {success} | 失败 {fail}"
        )
        self._apply_status_style("success" if fail == 0 else "warn")
        self.send_button.setEnabled(True)
        self.id_input.setEnabled(True)
        self.content_input.setEnabled(True)
        self._worker = None

    def _apply_status_style(self, state: str) -> None:
        colors = {
            "idle": "#888888",
            "running": "#E01010",
            "success": "#2E8B57",
            "warn": "#D2691E",
        }
        color = colors.get(state, "#888888")
        self.status_bar.setStyleSheet(
            f"color: {color}; padding: 6px 4px; border-top: 1px solid #E5E5E5;"
        )

    def closeEvent(self, event) -> None:  # noqa: N802
        if self._worker is not None and self._worker.isRunning():
            logger.warning("窗口关闭：终止正在进行的发送任务")
            self._worker.quit()
            self._worker.wait(3000)
        super().closeEvent(event)


__all__ = ["MainWindow"]