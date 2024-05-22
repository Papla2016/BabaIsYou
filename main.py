import sys
from main_window import *
app = QApplication(sys.argv)
menu_window = MenuWindow()
menu_window.show()
sys.exit(app.exec_())