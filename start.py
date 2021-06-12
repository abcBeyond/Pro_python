import sys

from Py_2048 import MainWidget, loadconfig
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    config = loadconfig.ConfigYaml("./Py_2048/config.yaml")

    mw = MainWidget.MainWidget(config=config)
    mw.show()
    sys.exit(app.exec_())
