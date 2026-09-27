# -*- coding: utf-8 -*-

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPolygonF, QPixmap
from qfluentwidgets import Theme, setTheme, setThemeColor

PRIMARY_RED = "#E01010"


def setup_theme() -> None:
    setTheme(Theme.LIGHT)
    setThemeColor(QColor(PRIMARY_RED))


def make_app_icon(size: int = 64) -> QIcon:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    painter.setBrush(QColor(PRIMARY_RED))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(QRectF(2, 2, size - 4, size - 4), 14, 14)

    cx, cy = size / 2, size / 2
    painter.setBrush(QColor("#FFFFFF"))
    painter.drawPolygon(QPolygonF([
        QPointF(cx, cy - 15),
        QPointF(cx - 13, cy + 7),
        QPointF(cx - 5, cy + 7),
        QPointF(cx - 5, cy + 15),
        QPointF(cx + 5, cy + 15),
        QPointF(cx + 5, cy + 7),
        QPointF(cx + 13, cy + 7),
    ]))
    painter.end()
    return QIcon(pixmap)


__all__ = ["setup_theme", "make_app_icon", "PRIMARY_RED"]