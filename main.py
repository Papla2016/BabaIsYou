import sys
from PyQt5.QtWidgets import QApplication

from main_window import MenuWindow


def main():
    app = QApplication(sys.argv)
    menu_window = MenuWindow()
    menu_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
