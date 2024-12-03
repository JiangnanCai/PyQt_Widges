
import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt, QTime, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from sentenceLine import SentenceLine


class MySlider(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super(MySlider, self).__init__(parent)

        self.setOrientation(Qt.Horizontal)
        self.setStyleSheet("""
            QSlider:groove:horizontal {
                border: 0px solid #bbb;
            }

            QSlider:sub-page:horizontal {
                background: rgb(90,49,255);
                border-radius: 2px;
                margin-top:8px;
                margin-bottom:8px;
            }

            QSlider::add-page:horizontal {
                background: rgb(255,255, 255);
                border: 0px solid #777;
                border-radius: 2px;
                margin-top:9px;
                margin-bottom:9px;
            }

            QSlider::handle:horizontal {
                background: rgb(193,204,208);
                width: 5px;
                border: 1px solid rgb(193,204,208);
                border-radius: 2px;
                margin-top:6px;
                margin-bottom:6px;
            }

            QSlider::handle:horizontal:hover {
                background: rgb(193,204,208);
                width: 10px;
                border: 1px solid rgb(193,204,208);
                border-radius: 5px;
                margin-top:4px;
                margin-bottom:4px;
            }
        """)
        self.setRange(0, 0)  # 初始范围设置为0，稍后在音频加载后更新
        self.setSliderPosition(0)


class AudioCheck(QtWidgets.QWidget):
    is_pause = True
    play_end_signal = QtCore.pyqtSignal(bool)

    def __init__(self, audio, parent=None):
        super(AudioCheck, self).__init__(parent)
        self.audio = audio
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.layout)

        self.slider = MySlider(self)
        self.checkbox = QtWidgets.QCheckBox(self)
        self.spacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.layout.addWidget(self.slider)
        self.layout.addSpacerItem(self.spacer)
        self.layout.addWidget(self.checkbox)

        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio)))

        self.timer = QtCore.QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.update_slider)
        self.slider.sliderMoved.connect(lambda: self.player.setPosition(self.slider.value()))

    def audio_play(self):

        if self.is_pause:
            self.player.play()
            self.is_pause = False
        else:
            self.player.pause()
            self.is_pause = True

    def update_slider(self):
        if self.is_pause:
            self.player.pause()
        else:
            self.slider.setRange(0, self.player.duration())
            self.slider.setValue(self.slider.value() + 1000)
            if self.slider.value() == self.player.duration():
                self.slider.setValue(0)
                self.is_pause = True
                self.player.setPosition(self.slider.value())
                self.play_end_signal.emit(True)


class AudioCheckText(QtWidgets.QWidget):
    def __init__(self, audio, text, parent=None):
        super(AudioCheckText, self).__init__(parent)

        self.setFixedWidth(400)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.audio_check = AudioCheck(audio, self)
        self.audio_check.play_end_signal.connect(self.play_end)
        self.layout.addWidget(self.audio_check)

        self.sentence_line = SentenceLine(text, self.width())
        self.play_start()
        self.layout.addWidget(self.sentence_line, Qt.AlignCenter)

    def play_start(self):
        for button in self.sentence_line.clickable_lines:
            button.clicked.connect(self.audio_check.audio_play)

    def play_end(self):
        for c_line in self.sentence_line.clickable_lines:
            c_line.setChecked(not c_line.isChecked())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    st = "The human body has an estimated 37.2 trillion cells. Each type of cell has a unique job. " \
         "Knowing each cell's job can help scientists better understand health and diseases such as cancer."
    mu = r"D:\cai_dev\PyQt_Widges\audio\123.mp3"
    cc = AudioCheckText(mu, st)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
