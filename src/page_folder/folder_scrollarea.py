import sys
from uuid import uuid4

from PyQt5 import QtWidgets, QtCore, QtGui

from folder_swipe_action import FolderSwipeAction


class FolderScrollArea(QtWidgets.QScrollArea):
    width = 250
    height = 50
    widget_group = []  # 用于维护列表，新增，删除

    def __init__(self, parent=None):
        super(FolderScrollArea, self).__init__(parent)
        self.setFixedWidth(250)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMinimumHeight(400)
        self.widget_group = []

        self.widget.setLayout(QtWidgets.QVBoxLayout(self.widget))
        self.widget.layout().setContentsMargins(0, 2, 0, 2)

        # self.add_audio_file("录音1", "2024.12.04", "06:30")
        # self.add_audio_file("录音2", "2024.12.04", "06:30")
        # self.add_audio_file("录音3", "2024.12.04", "06:30")
        # self.add_audio_file("录音3", "2024.12.04", "06:30")
        # self.add_audio_file("录音3", "2024.12.04", "06:30")
        self.add_audio_file("录音3", "2024.12.04", "06:30")
        self.widget.layout().addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum,
                                                           QtWidgets.QSizePolicy.Expanding))
        self.setWidget(self.widget)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def add_audio_file(self, title, date, end_time):
        for i in range(self.widget.layout().count()):
            print(self.widget.layout().itemAt(i))
            if isinstance(self.widget.layout().itemAt(i), QtWidgets.QSpacerItem):
                self.widget.layout().removeItem(self.widget.layout().itemAt(i))

        tmp_obj_name = str(uuid4())
        folder = FolderSwipeAction(title, date, end_time, self.width, self.height)
        folder.delete_signal.connect(self.delete_audio_file)
        folder.setObjectName(tmp_obj_name)
        folder.setVisible(True)
        folder.setEnabled(True)

        line = QtWidgets.QFrame()
        line.setObjectName(tmp_obj_name)
        line.setFixedWidth(self.width - int(self.width / 10))
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Plain)
        line.setStyleSheet("QWidget {color: #BEBEBE;}")
        line.setVisible(True)

        self.widget_group.append(folder)
        self.widget_group.append(line)

        self.widget.layout().addWidget(folder)
        self.widget.layout().addWidget(line)
        self.widget.layout().setAlignment(line, QtCore.Qt.AlignCenter)
        self.widget.layout().addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum,
                                                                 QtWidgets.QSizePolicy.Expanding))

    def delete_audio_file(self, obj_name):
        tmp_widget_group = []
        for i in self.widget_group:
            if i.objectName() == obj_name:
                self.widget.layout().removeWidget(i)
                i.setVisible(False)
                i.deleteLater()
            else:
                tmp_widget_group.append(i)
        self.widget_group = tmp_widget_group

        self.widget.layout().addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum,
                                                                 QtWidgets.QSizePolicy.Expanding))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # cc = FolderCover("新录音1", "2024.11.21", "06:30")
    cc = FolderScrollArea()
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
