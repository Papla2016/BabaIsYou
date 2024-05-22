
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

import main_window
import render


def intersection(lst1, lst2):
    lst3 = []
    for i in lst1:
        if i in lst2:
            lst3.append(i)
    return lst3

class MainWindow(QMainWindow):
    def replace(self,at,to):
        at = at.replace("_word", "")
        to = to.replace("_word", "")
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] == at:
                    self.grid[i][j] = to
    def logic_input(self):
        self.logic = {}
        for i in range(1,self.rows-1):
            for j in range(1,self.columns-1):
                if self.grid[i][j] == 'is':
                    if self.grid[i-1][j] in self.words_object and self.grid[i+1][j] in self.words_features:
                        if self.logic.get(self.grid[i - 1][j]) is None:
                            self.logic[self.grid[i-1][j]] = [self.grid[i+1][j]]
                        else:
                            self.logic[self.grid[i-1][j]].append(self.grid[i+1][j])
                    elif self.grid[i-1][j] in self.words_object and self.grid[i+1][j] in self.words_object:
                        self.replace(self.grid[i-1][j].replace("_word", ""),self.grid[i+1][j].replace("_word", ""))
                    if self.grid[i][j-1] in self.words_object and self.grid[i][j+1] in self.words_features:
                        if self.logic.get(self.grid[i][j - 1]) is None:
                            self.logic[self.grid[i][j-1]] = [self.grid[i][j+1]]
                        else:
                            self.logic[self.grid[i][j-1]] = self.logic[self.grid[i][j-1]].append([self.grid[i][j+1]])
                    elif self.grid[i][j-1] in self.words_object and self.grid[i][j+1] in self.words_object:
                        self.replace(self.grid[i][j-1].replace("_word", ""),self.grid[i][j+1].replace("_word", ""))
        self.find_you_pos()
        self.find_win_pos()
        self.find_push_pos()
    def find_you(self):
        temp = []
        for key, value in self.logic.items():
            if 'you_word' in value:
                temp.append(key.replace("_word",""))
        return temp
    def find_win(self):
        temp = []
        for key, value in self.logic.items():
            if 'win_word' in value:
                temp.append(key.replace("_word",""))
        return temp
    def find_push(self):
        temp = []
        for key, value in self.logic.items():
            if 'push_word' in value:
                temp.append(key.replace("_word", ""))
        return temp
    def find_push_pos(self):
        self.push = self.find_push()
        self.current_push = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] in self.push:
                    self.current_push.append([i,j])
    def find_win_pos(self):
        self.win = self.find_win()
        self.current_win = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] in self.win:
                    self.current_win.append([i,j])
    def find_you_pos(self):
        self.you = self.find_you()
        self.current_positions = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] in self.you:
                    self.current_positions.append([i, j])

    def __init__(self, rows, columns, grid):
        super().__init__()
        self.words_object = ["baba_word","flag_word","rock_word"]
        self.words_features = ["win_word","you_word","push_word"]
        self.words = self.words_object + self.words_features + ["is"]
        self.rows = rows
        self.columns = columns
        self.grid = grid

        render.initUI(self)
        self.logic_input()
        self.setFocusPolicy(5)
    def initLogic(self):
        self.logic_input()



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
            temp_copy_current_positions = self.current_positions.copy()
            if key == Qt.Key_Up:
                temp_copy_current_positions = sorted(temp_copy_current_positions,key=lambda x:x[0])
            elif key == Qt.Key_Down:
                temp_copy_current_positions = sorted(temp_copy_current_positions,key=lambda x:x[0],reverse=True)
            elif key == Qt.Key_Right:
                temp_copy_current_positions = sorted(temp_copy_current_positions, key=lambda x: x[1],reverse=True)
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
                if next_position in self.current_win:
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
                elif self.grid[next_position[0]][next_position[1]] in self.words:
                    is_word_move = True
                    next_position_cube = [next_position[0] + (next_position[0] - current_position[0]),
                                        next_position[1] + (next_position[1] - current_position[1])]
                    if 1 <= next_position_cube[0] < self.rows - 1 and 1 <= next_position_cube[1] < self.columns - 1:
                        if self.grid[next_position_cube[0]][next_position_cube[1]] == 'none':
                            self.grid[next_position_cube[0]][next_position_cube[1]] = self.grid[next_position[0]][next_position[1]]
                            self.current_positions.append(next_position)
                            self.grid[next_position[0]][next_position[1]] = self.grid[current_position[0]][current_position[1]]
                            self.grid[current_position[0]][current_position[1]] = 'none'
                            new_positions.append(current_position)
                    else:
                        new_positions.append(current_position)
                elif next_position in self.current_push:
                    next_position_cube = [next_position[0] + (next_position[0] - current_position[0]),
                                          next_position[1] + (next_position[1] - current_position[1])]
                    if 1 <= next_position_cube[0] < self.rows - 1 and 1 <= next_position_cube[1] < self.columns - 1:
                        if self.grid[next_position_cube[0]][next_position_cube[1]] == 'none':
                            self.grid[next_position_cube[0]][next_position_cube[1]] = self.grid[next_position[0]][
                                next_position[1]]
                            self.current_positions.append(next_position)
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

            self.current_positions = new_positions
            if is_word_move:
                self.logic_input()
            elif is_push_move:
                self.find_push_pos()
            render.update_cubes(self)
            if len(self.current_positions) == 0:
                QMessageBox.information(self, "Поражение!", "Вы проиграли!")
                self.close()

            if len(intersection(self.current_positions,self.current_win)) > 0:
                QMessageBox.information(self, "Победа!", "Вы выйграли!")
                self.close()
    def check_win_condition(self):
        for current_position in self.current_positions:
            if current_position in self.win_positions:
                return True
        return False




