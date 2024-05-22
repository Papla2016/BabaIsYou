from Task5 import *
class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        render.menu_render(self)
    def start_level(self,filename):
        try:
            with open(filename, 'r') as file:
                rows = 0
                columns = 0
                grid = []
                colors = {
                    0: 'none',
                    1: 'grey',
                    2: 'baba',
                    3: 'rock',
                    4: 'is',
                    5: 'baba_word',
                    6: 'you_word',
                    7: 'flag_word',
                    8: 'win_word',
                    9: 'flag',
                    10: 'rock_word',
                    11: 'push_word'
                }
                for line in file:
                    row = [colors[int(num)] for num in line.split()]
                    if not columns:
                        columns = len(row)
                    else:
                        if len(row) != columns:
                            raise ValueError("Inconsistent number of columns")
                    rows += 1
                    grid.append(row)
                self.start_game(rows, columns, grid, filename)
        except FileNotFoundError:
            QMessageBox.critical( "Ошибка", "Файл уровня не найден.")
        except ValueError as e:
            QMessageBox.critical( "Ошибка", str(e))
        except KeyError as e:
            QMessageBox.critical( "Ошибка", f"Неизвестный цвет: {e}")
    def start_game(self, rows, columns, grid,level_name):
        self.game_window = MainWindow(rows, columns, grid)
        self.game_window.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.game_window.show()

