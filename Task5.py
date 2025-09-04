from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt

import render


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


class RuleEngine:
    def __init__(self, level):
        self.level = level
        self.words_object = ["baba_word", "flag_word", "rock_word"]
        self.words_features = ["win_word", "you_word", "push_word"]
        self.words = self.words_object + self.words_features + ["is"]
        self.logic = {}
        self.current_positions = []
        self.current_win = []
        self.current_push = []
        self.build()

    def replace(self, at, to):
        at = at.replace("_word", "")
        to = to.replace("_word", "")
        for i in range(self.level.rows):
            for j in range(self.level.columns):
                if self.level.grid[i][j] == at:
                    self.level.grid[i][j] = to

    def build(self):
        self.logic = {}
        for i in range(1, self.level.rows - 1):
            for j in range(1, self.level.columns - 1):
                if self.level.grid[i][j] == 'is':
                    if self.level.grid[i-1][j] in self.words_object and self.level.grid[i+1][j] in self.words_features:
                        self.logic.setdefault(self.level.grid[i-1][j], []).append(self.level.grid[i+1][j])
                    elif self.level.grid[i-1][j] in self.words_object and self.level.grid[i+1][j] in self.words_object:
                        self.replace(self.level.grid[i-1][j], self.level.grid[i+1][j])

                    if self.level.grid[i][j-1] in self.words_object and self.level.grid[i][j+1] in self.words_features:
                        self.logic.setdefault(self.level.grid[i][j-1], []).append(self.level.grid[i][j+1])
                    elif self.level.grid[i][j-1] in self.words_object and self.level.grid[i][j+1] in self.words_object:
                        self.replace(self.level.grid[i][j-1], self.level.grid[i][j+1])

        self.find_you_pos()
        self.find_win_pos()
        self.find_push_pos()

    def _find_objects_with_feature(self, feature):
        return [key.replace("_word", "") for key, value in self.logic.items() if feature in value]

    def _collect_positions(self, names):
        positions = []
        for i in range(self.level.rows):
            for j in range(self.level.columns):
                if self.level.grid[i][j] in names:
                    positions.append([i, j])
        return positions

    def find_push_pos(self):
        self.push = self._find_objects_with_feature('push_word')
        self.current_push = self._collect_positions(self.push)

    def find_win_pos(self):
        self.win = self._find_objects_with_feature('win_word')
        self.current_win = self._collect_positions(self.win)

    def find_you_pos(self):
        self.you = self._find_objects_with_feature('you_word')
        self.current_positions = self._collect_positions(self.you)


class GameWindow(QMainWindow):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.rows = level.rows
        self.columns = level.columns
        self.grid = level.grid
        self.engine = RuleEngine(level)

        render.initUI(self)
        self.setFocusPolicy(Qt.StrongFocus)

    def show_rules(self):
        rules_text = (
            "Цель игры: достичь маркера указывающего на победу \n\n"
            "Управление: Игрок может управлять черным кубиком с помощью стрелок на клавиатуре.\nСтрелка вверх перемещает"
            "кубик вверх\nстрелка вниз - вниз\nстрелка влево - влево\nстрелка вправо - вправо.\n")

        QMessageBox.information(self, "Правила", rules_text)
    def keyPressEvent(self, event):
        key = event.key()
        if key in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down]:
            new_positions = []
            is_word_move = False
            is_push_move = False
            temp_copy_current_positions = self.engine.current_positions.copy()
            if key == Qt.Key_Up:
                temp_copy_current_positions = sorted(temp_copy_current_positions, key=lambda x: x[0])
            elif key == Qt.Key_Down:
                temp_copy_current_positions = sorted(temp_copy_current_positions, key=lambda x: x[0], reverse=True)
            elif key == Qt.Key_Right:
                temp_copy_current_positions = sorted(temp_copy_current_positions, key=lambda x: x[1], reverse=True)
            elif key == Qt.Key_Left:
                temp_copy_current_positions = sorted(temp_copy_current_positions, key=lambda x: x[1])
            for current_position in temp_copy_current_positions:
                next_position = current_position.copy()

                if key == Qt.Key_Left:
                    next_position[1] -= 1
                elif key == Qt.Key_Right:
                    next_position[1] += 1
                elif key == Qt.Key_Up:
                    next_position[0] -= 1
                elif key == Qt.Key_Down:
                    next_position[0] += 1

                next_position[0] = max(1, min(next_position[0], self.rows - 2))
                next_position[1] = max(1, min(next_position[1], self.columns - 2))
                if next_position in self.engine.current_win:
                    QMessageBox.information(self, "Победа!", "Вы выйграли!")
                    self.close()
                if (next_position[0] == 0 or next_position[0] == self.rows - 1 or
                    next_position[1] == 0 or next_position[1] == self.columns - 1):
                    return
                if next_position == current_position:
                    new_positions.append(current_position)
                elif self.grid[next_position[0]][next_position[1]] == 'none':
                    if current_position in new_positions:
                        self.grid[next_position[0]][next_position[1]] = self.grid[current_position[0]][current_position[1]]
                    else:
                        self.grid[next_position[0]][next_position[1]] = self.grid[current_position[0]][current_position[1]]
                        self.grid[current_position[0]][current_position[1]] = 'none'
                    new_positions.append(next_position)
                elif self.grid[next_position[0]][next_position[1]] in self.engine.words:
                    is_word_move = True
                    next_position_cube = [next_position[0] + (next_position[0] - current_position[0]),
                                        next_position[1] + (next_position[1] - current_position[1])]
                    if 1 <= next_position_cube[0] < self.rows - 1 and 1 <= next_position_cube[1] < self.columns - 1:
                        if self.grid[next_position_cube[0]][next_position_cube[1]] == 'none':
                            self.grid[next_position_cube[0]][next_position_cube[1]] = self.grid[next_position[0]][next_position[1]]
                            self.engine.current_positions.append(next_position)
                            self.grid[next_position[0]][next_position[1]] = self.grid[current_position[0]][current_position[1]]
                            self.grid[current_position[0]][current_position[1]] = 'none'
                            new_positions.append(current_position)
                    else:
                        new_positions.append(current_position)
                elif next_position in self.engine.current_push:
                    next_position_cube = [next_position[0] + (next_position[0] - current_position[0]),
                                          next_position[1] + (next_position[1] - current_position[1])]
                    if 1 <= next_position_cube[0] < self.rows - 1 and 1 <= next_position_cube[1] < self.columns - 1:
                        if self.grid[next_position_cube[0]][next_position_cube[1]] == 'none':
                            self.grid[next_position_cube[0]][next_position_cube[1]] = self.grid[next_position[0]][
                                next_position[1]]
                            self.engine.current_positions.append(next_position)
                            self.grid[next_position[0]][next_position[1]] = self.grid[current_position[0]][
                                current_position[1]]
                            self.grid[current_position[0]][current_position[1]] = 'none'

                            new_positions.append(next_position)
                            is_push_move = True
                        else:
                            new_positions.append(current_position)
                    else:
                        new_positions.append(current_position)
                else:
                    new_positions.append(current_position)

            self.engine.current_positions = new_positions
            if is_word_move:
                self.engine.build()
            elif is_push_move:
                self.engine.find_push_pos()
            render.update_cubes(self)
            if len(self.engine.current_positions) == 0:
                QMessageBox.information(self, "Поражение!", "Вы проиграли!")
                self.close()
            if len(intersection(self.engine.current_positions, self.engine.current_win)) > 0:
                QMessageBox.information(self, "Победа!", "Вы выйграли!")
                self.close()




