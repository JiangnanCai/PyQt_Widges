import os.path
import sys
from typing import Dict

from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.common_widget.top_bar import TopBar
from src.page_folder.folder_scrollarea import FolderScrollArea
from src.data_parser import Article
import whisper_timestamped as whisper

W_EXPANDING = (0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
H_EXPANDING = (0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)


class TitleWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TitleWidget, self).__init__(parent)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.title = QtWidgets.QLabel("所有音频")
        self.title.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                font-size: 30px; 
                font-family: 'Microsoft YaHei';
            }
        """)
        self.layout().addWidget(self.title)
        self.layout().addItem(QtWidgets.QSpacerItem(*W_EXPANDING))


class ImportRecordWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImportRecordWidget, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.middle_widget = QtWidgets.QWidget()
        self.middle_widget.setLayout(QtWidgets.QHBoxLayout())
        self.middle_widget.layout().setContentsMargins(0, 0, 0, 0)

        self.import_button = QtWidgets.QPushButton("导入")
        self.record_button = QtWidgets.QPushButton("录音")
        self.middle_widget.layout().addItem(QtWidgets.QSpacerItem(*W_EXPANDING))
        self.middle_widget.layout().addWidget(self.import_button)
        self.middle_widget.layout().addWidget(self.record_button)
        self.middle_widget.layout().addItem(QtWidgets.QSpacerItem(*W_EXPANDING))

        self.layout().addWidget(self.middle_widget)


class WhisperThread(QtCore.QThread):
    finished = QtCore.pyqtSignal(dict)

    def __init__(self, audio_datas, parent=None):
        super(WhisperThread, self).__init__(parent)
        self.audio_datas = audio_datas
        self.file_path = audio_datas.get("file_path")
        self.language = audio_datas.get("language")

    def run(self):
        res = whisper.transcribe(
            model=whisper.load_model("tiny", device="cpu"),
            audio=whisper.load_audio(self.file_path),
            language=self.language
        )
        res.update(self.audio_datas)
        self.finished.emit(res)


class PageAudioList(QtWidgets.QWidget):
    def __init__(self, width, height, parent=None):
        super(PageAudioList, self).__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.top_bar = TopBar("")
        self.top_bar.setMaximumHeight(50)
        self.layout().addWidget(self.top_bar)

        self.title = TitleWidget()
        self.layout().addWidget(self.title)

        self.search_line = QtWidgets.QLineEdit()
        self.search_line.setFixedHeight(30)
        self.search_line.setStyleSheet("""
            QLineEdit {
                border: 0px;
                border-radius: 10px;
                font-size: 16px;
                font-family: 'Microsoft YaHei';
            }
        """)

        self.layout().addWidget(self.search_line)

        self.audio_list = FolderScrollArea()
        self.audio_list.setFixedHeight(400)
        self.layout().addWidget(self.audio_list)

        self.import_record = ImportRecordWidget()
        self.layout().addWidget(self.import_record)
        self.layout().setAlignment(QtCore.Qt.AlignTop)

        self.import_record.import_button.clicked.connect(self.read_file)
        self.new_audio_item = None
        self.thread = None

    def read_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "导入音频文件",
                                                             r"D:\cai_dev\PyQt_Widges\audio",
                                                             "All Files(*);;Wav(*.wav);;Txt (*.txt)")

        if not file_path:
            return

        audio_datas = {
            "date": datetime.now().strftime('%Y.%m.%d'),
            "end_time": "xx:xx",
            "title": os.path.basename(file_path).split('.')[0],
            "file_path": file_path,
            "language": "en"
        }

        self.new_audio_item = self.audio_list.add_audio_item(
            title=audio_datas.get("title"),
            date=audio_datas.get("date"),
            end_time=audio_datas.get("end_time"),
        )

        self.thread = WhisperThread(audio_datas)
        self.thread.finished.connect(self.task_finished)
        self.thread.start()

    def task_finished(self, res):
        self.new_audio_item.article_datas = res


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # cc = FolderCover("新录音1", "2024.11.21", "06:30")
    cc = PageAudioList()
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
