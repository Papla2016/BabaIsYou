from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt

from level import Level
from Task5 import GameWindow
import render


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        render.menu_render(self)
    def start_level(self, filename):
        try:
            level = Level.from_file(filename)
            self.start_game(level)
        except FileNotFoundError:
            QMessageBox.critical("Ошибка", "Файл уровня не найден.")
        except (ValueError, KeyError) as e:
            QMessageBox.critical("Ошибка", str(e))

    def start_game(self, level):
        self.game_window = GameWindow(level)
        self.game_window.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.game_window.show()

