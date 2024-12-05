import os.path
import sys

from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.common_widget.top_bar import TopBar
from folder_scrollarea import FolderScrollArea
import whisper_timestamped as whisper


class TitleWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TitleWidget, self).__init__(parent)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.title = QtWidgets.QLabel("所有音频")
        self.title.setStyleSheet("QLabel {font-weight: bold; font-size: 40px;}")
        self.layout().addWidget(self.title)
        self.layout().addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                          QtWidgets.QSizePolicy.Minimum))


class ImportRecordWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImportRecordWidget, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.middle_widget = QtWidgets.QWidget()
        self.middle_widget.setLayout(QtWidgets.QHBoxLayout())
        self.middle_widget.layout().setContentsMargins(0, 0, 0, 0)

        self.import_button = QtWidgets.QPushButton("导入")
        self.record_button = QtWidgets.QPushButton("录音")
        self.middle_widget.layout().addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                                        QtWidgets.QSizePolicy.Minimum))
        self.middle_widget.layout().addWidget(self.import_button)
        self.middle_widget.layout().addWidget(self.record_button)
        self.middle_widget.layout().addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                                        QtWidgets.QSizePolicy.Minimum))

        self.layout().addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum,
                                                          QtWidgets.QSizePolicy.Expanding))
        self.layout().addWidget(self.middle_widget)
        self.layout().addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum,
                                                          QtWidgets.QSizePolicy.Expanding))


class WorkerThread(QtCore.QThread):
    finished = QtCore.pyqtSignal(dict, str)

    def __init__(self, file_path, language="en", parent=None):
        super(WorkerThread, self).__init__(parent)
        self.file_path = file_path
        self.language = language

    def run(self):
        # 耗时操作
        model = whisper.load_model("tiny", device="cpu")
        audio = whisper.load_audio(self.file_path)
        res = whisper.transcribe(model, audio, language=self.language)
        self.finished.emit(res, self.file_path)  # 发送完成信号


class PageAudioList(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PageAudioList, self).__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.top_bar = TopBar("")
        self.layout().addWidget(self.top_bar)

        self.title = TitleWidget()
        self.layout().addWidget(self.title)

        self.search_line = QtWidgets.QLineEdit()
        self.layout().addWidget(self.search_line)
        self.search_line.setFixedSize(250, 30)

        self.audio_list = FolderScrollArea()
        self.layout().addWidget(self.audio_list)

        self.import_record = ImportRecordWidget()
        self.layout().addWidget(self.import_record)

        self.import_record.import_button.clicked.connect(self.read_file)

    def read_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "导入音频文件",
                                                             r"D:\cai_dev\PyQt_Widges\audio",
                                                             "All Files(*);;Wav(*.wav);;Txt (*.txt)")
        file_name = os.path.basename(file_path).split('.')[0]
        date = datetime.now().strftime('%Y.%m.%d')
        end_time = "xx:xx"
        self.audio_list.add_audio_file(file_name, date, end_time)

        # 本来想整个进度条的，目前看来没啥意义
        self.thread = WorkerThread(file_path)
        self.thread.finished.connect(self.task_finished)
        self.thread.start()

    def task_finished(self, res, file_path):
        file_name = os.path.basename(file_path).split('.')[0]

        print(res)
        print(file_name)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    # cc = FolderCover("新录音1", "2024.11.21", "06:30")
    cc = PageAudioList()
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
