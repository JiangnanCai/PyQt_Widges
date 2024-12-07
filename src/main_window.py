import functools
import os
import sys
from datetime import datetime

from PyQt5 import QtWidgets, QtCore, QtGui

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.page_audio_detail.pageAudioDetail import PageAudioDetail
from src.page_folder.pageAudioList import PageAudioList
from src.data_parser import Article


class MainWindow(QtWidgets.QMainWindow):
    _width = 360
    _height = 640

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedSize(self._width, self._height)

        self.center_widget = QtWidgets.QWidget()
        self.center_widget.setLayout(QtWidgets.QVBoxLayout())

        self.stack_widget = QtWidgets.QStackedWidget(self)

        self.audio_list_page = PageAudioList(self._width, self._height)
        self.stack_widget.addWidget(self.audio_list_page)

        self.audio_list_page.audio_list.audio_detail_signal.connect(self.new_audio_detail_page)

        self.center_widget.layout().addWidget(self.stack_widget)
        self.setCentralWidget(self.center_widget)

    def new_audio_detail_page(self, article_datas):
        audio_detail_page = PageAudioDetail(
            article=Article(article_datas),
            title=article_datas.get("title"),
            date=article_datas.get("date"),
            audio=article_datas.get("file_path"),
            width=self._width,
            height=self._height,
        )
        audio_detail_page.return_signal.connect(functools.partial(self.stack_widget.setCurrentIndex, 0))
        self.stack_widget.addWidget(audio_detail_page)
        self.stack_widget.setCurrentIndex(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    cc = MainWindow()
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
