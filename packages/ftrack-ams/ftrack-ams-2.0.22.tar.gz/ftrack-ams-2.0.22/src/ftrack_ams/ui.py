from PyQt5 import QtWidgets


def user_interface():
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    window.show()

    app.exec_()
