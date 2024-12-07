import sys

from PyQt5 import QtWidgets, QtCore, QtGui

from src.common_widget.swipe_action import SwipeAction


class AudioCover(QtWidgets.QWidget):
    clicked_signal = QtCore.pyqtSignal()

    def __init__(self, title, date, end_time, parent=None):
        super(AudioCover, self).__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(10, 0, 10, 0)

        self.time_widget = QtWidgets.QWidget()
        self.time_widget.setLayout(QtWidgets.QHBoxLayout())
        self.time_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.time_widget.layout().addWidget(QtWidgets.QLabel(date))
        self.time_widget.layout().addStretch(1)
        self.time_widget.layout().addWidget(QtWidgets.QLabel(end_time))

        self.layout().addWidget(QtWidgets.QLabel(title))
        self.layout().addWidget(self.time_widget)

        self.layout().setAlignment(QtCore.Qt.AlignLeft)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked_signal.emit()


class AudiSwipeAction(QtWidgets.QWidget):
    delete_signal = QtCore.pyqtSignal(str)
    rename_signal = QtCore.pyqtSignal(str)
    enter_signal = QtCore.pyqtSignal(dict)
    article_datas = None

    def __init__(self, title, date, end_time, width, height, parent=None):
        super(AudiSwipeAction, self).__init__(parent)

        self.setFixedSize(width, height)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.cover = AudioCover(title, date, end_time)
        self.cover.setFixedSize(width, height)

        self.rename_button = QtWidgets.QPushButton("重命名")
        self.rename_button.setStyleSheet("QWidget {background-color: blue; color: white;}")
        self.rename_button.setFixedSize(height, height)

        self.delete_button = QtWidgets.QPushButton("删除")
        self.delete_button.setStyleSheet("QWidget {background-color: red; color: white;}")
        self.delete_button.setFixedSize(height, height)

        buttons = [self.cover, self.rename_button, self.delete_button]

        swipe_action = SwipeAction(widgets=buttons, drag_orient="right", parent=self)
        self.layout().addWidget(swipe_action)

        self.rename_button.clicked.connect(self.rename_signal_emit)
        self.delete_button.clicked.connect(self.delete_signal_emit)
        self.cover.clicked_signal.connect(self.enter_signal_emit)

    def enter_signal_emit(self):
        self.enter_signal.emit(self.article_datas)

    def delete_signal_emit(self):
        self.delete_signal.emit(self.objectName())

    def rename_signal_emit(self):
        self.rename_signal.emit(self.objectName())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # cc = FolderCover("新录音1", "2024.11.21", "06:30")
    cc = AudiSwipeAction("新录音1", "2024.11.21", "06:30", 250, 50)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
