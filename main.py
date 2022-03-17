from PyQt5 import QtWidgets
import sys
from view import Interface

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Interface()
    sys.exit(app.exec_())