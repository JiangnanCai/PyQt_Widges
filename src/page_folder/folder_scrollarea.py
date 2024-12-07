import sys
from uuid import uuid4

from PyQt5 import QtWidgets, QtCore, QtGui

from src.page_folder.folder_swipe_action import AudiSwipeAction


class FolderScrollArea(QtWidgets.QScrollArea):
    widget_group = []  # 用于维护列表，新增，删除
    audio_detail_signal = QtCore.pyqtSignal(dict)
    _height = 40

    def __init__(self, parent=None):
        super(FolderScrollArea, self).__init__(parent)

        self.widget = QtWidgets.QWidget(self)
        self.widget_group = []
        self.folders = []

        self.widget.setLayout(QtWidgets.QVBoxLayout(self.widget))

        self.setWidget(self.widget)
        self.setWidgetResizable(True)

        self.widget.layout().setContentsMargins(0, 5, 0, 0)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def audio_detail_signal_emit(self):
        self.audio_detail_signal.emit(self.sender().article_datas)

    def add_audio_item(self, title, date, end_time):

        tmp_obj_name = str(uuid4())
        audio_item = AudiSwipeAction(title, date, end_time, self.width(), self._height)
        audio_item.setObjectName(tmp_obj_name)
        audio_item.delete_signal.connect(self.delete_audio_file)
        audio_item.enter_signal.connect(self.audio_detail_signal_emit)

        line = QtWidgets.QFrame()
        line.setObjectName(tmp_obj_name)
        line.setFixedWidth(self.width())
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Plain)
        line.setStyleSheet("QFrame {color: #BEBEBE;}")

        self.folders.append(audio_item)
        self.widget_group.append(audio_item)
        self.widget_group.append(line)

        self.widget.layout().addWidget(audio_item)
        self.widget.layout().addWidget(line)

        self.ensureWidgetVisible(audio_item)
        self.ensureWidgetVisible(line)
        self.widget.layout().setAlignment(QtCore.Qt.AlignTop)
        return audio_item

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # cc = FolderCover("新录音1", "2024.11.21", "06:30")
    cc = FolderScrollArea()
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
