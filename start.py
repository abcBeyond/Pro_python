import sys

from Py_2048 import MainWidget
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWidget.MainWidget()
    mw.show()
    sys.exit(app.exec_())
