#!/usr/bin/env python3
# encoding=utf-8
'''
Author: Dodotry
Date: 2026-09-27 14:59:26
LastEditors: Dodotry
LastEditTime: 2026-09-27 15:36:01
'''


import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QLocale, QLibraryInfo, QTranslator
from qfluentwidgets import setThemeColor, Theme, FluentTranslator

from .core.config import ApiConfig
from .core.logger import setup_logger
from .ui.main_window import MainWindow
from .ui.theme import setup_theme


def install_translators(app: QApplication) -> list[QTranslator]:
    translators: list[QTranslator] = []

    ft_translator = FluentTranslator(
        QLocale(QLocale.Language.Chinese, QLocale.Country.China)
    )
    app.installTranslator(ft_translator)
    translators.append(ft_translator)

    qt_translator = QTranslator(app)
    translation_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    if qt_translator.load("qt_zh_CN.qm", translation_path):
        app.installTranslator(qt_translator)
        translators.append(qt_translator)

    return translators


def run(config: ApiConfig | None = None) -> int:
    setup_logger()
    app = QApplication.instance() or QApplication(sys.argv)
    setup_theme()
    translators = install_translators(app)
    window = MainWindow(config)
    window.show()
    return app.exec()


def main() -> None:
    raise SystemExit(run())


__all__ = ["run", "main"]
