from Task5 import *


def initUI(Main_Pyqt):
    Main_Pyqt.setWindowTitle("Кубикон")
    Main_Pyqt.setGeometry(100, 100, 22 * Main_Pyqt.columns + 2, 22 * Main_Pyqt.rows + 2)
    central_widget = QWidget(Main_Pyqt)
    Main_Pyqt.setCentralWidget(central_widget)

    main_layout = QVBoxLayout()
    main_layout.setSpacing(0)
    central_widget.setLayout(main_layout)

    Main_Pyqt.cube_labels = []
    for i in range(Main_Pyqt.rows):
        row_layout = QHBoxLayout()
        for j in range(Main_Pyqt.columns):
            cube_label = QLabel()
            if i == 0 or j == 0 or i == Main_Pyqt.rows - 1 or j == Main_Pyqt.columns - 1 or Main_Pyqt.grid[i][j] == "grey":
                cube_label.setStyleSheet("background-color:grey;")
            else:
                cube_label.setStyleSheet("""
                background-color: black;
                background-image: url({}.gif);
                -webkit-background-size: cover;
                background-repeat: no-repeat;""".format(Main_Pyqt.grid[i][j]))
            cube_label.setFixedSize(25, 25)

            row_layout.addWidget(cube_label)
            Main_Pyqt.cube_labels.append(cube_label)
        main_layout.addLayout(row_layout)

    Main_Pyqt.rules_button = QPushButton("Правила", Main_Pyqt)
    Main_Pyqt.rules_button.setWindowModality(Qt.WindowModal)
    Main_Pyqt.rules_button.clicked.connect(Main_Pyqt.show_rules)
    main_layout.addWidget(Main_Pyqt.rules_button)
def update_cubes(Main_Pyqt):
    for i, label in enumerate(Main_Pyqt.cube_labels):
        row = i // Main_Pyqt.columns
        col = i % Main_Pyqt.columns
        if row == 0 or col == 0 or row == Main_Pyqt.rows - 1 or col == Main_Pyqt.columns - 1 or Main_Pyqt.grid[row][col] == "grey":
            label.setStyleSheet("background-color:grey;")
        else:
            label.setStyleSheet("""
            background-color: black;
            background-image: url({}.gif);
            -webkit-background-size: cover;
            background-repeat: no-repeat;""".format(Main_Pyqt.grid[row][col]))
def menu_render(menu):
    menu.setWindowTitle("Меню")
    menu.setGeometry(100, 100, 300, 200)

    central_widget = QWidget(menu)
    menu.setCentralWidget(central_widget)

    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    level1_button = QPushButton("Уровень 1", menu)
    level1_button.clicked.connect(lambda: menu.start_level("level1.txt"))
    layout.addWidget(level1_button)

    level2_button = QPushButton("Уровень 2", menu)
    level2_button.clicked.connect(lambda: menu.start_level("level2.txt"))
    layout.addWidget(level2_button)

    level3_button = QPushButton("Уровень 3", menu)
    level3_button.clicked.connect(lambda: menu.start_level("level3.txt"))
    layout.addWidget(level3_button)