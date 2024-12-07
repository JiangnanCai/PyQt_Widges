import sys

from PyQt5 import QtWidgets, QtCore, QtGui

W_EXPANDING = (0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
H_EXPANDING = (0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)


class TopBar(QtWidgets.QWidget):
    def __init__(self, title,  parent=None):
        super(TopBar, self).__init__(parent)
        self.setLayout(QtWidgets.QHBoxLayout())

        self.button_left = QtWidgets.QPushButton("<")
        self.title = QtWidgets.QLabel(title)
        self.button_right = QtWidgets.QPushButton()

        self.layout().addWidget(self.button_left)
        self.layout().addItem(QtWidgets.QSpacerItem(*W_EXPANDING))
        self.layout().addWidget(self.title)
        self.layout().addItem(QtWidgets.QSpacerItem(*W_EXPANDING))
        self.layout().addWidget(self.button_right)

        self.layout().setContentsMargins(0, 0, 0, 0)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    a2 = TopBar("sss")
    a2.show()
    sys.exit(app.exec_())
