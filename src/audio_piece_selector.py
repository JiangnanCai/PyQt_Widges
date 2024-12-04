import sys

from PyQt5 import QtWidgets, QtCore

from sentence_line import SentenceLine
from audio_player import AudioSlider


class AudioCheck(QtWidgets.QWidget):
    def __init__(self, audio, parent=None):
        super(AudioCheck, self).__init__(parent)
        self.audio = audio
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.layout)

        self.slider = AudioSlider(audio, self)

        self.checkbox = QtWidgets.QCheckBox(self)
        self.spacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.layout.addWidget(self.slider)
        self.layout.addSpacerItem(self.spacer)
        self.layout.addWidget(self.checkbox)


class AudioPieceSelector(QtWidgets.QWidget):
    def __init__(self, audio, text, parent=None):
        super(AudioPieceSelector, self).__init__(parent)

        self.setFixedWidth(400)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.audio_check = AudioCheck(audio)
        self.layout().addWidget(self.audio_check)

        self.stc_line = SentenceLine(text, self.width())
        self.layout().addWidget(self.stc_line)

        for c_line in self.stc_line.clickable_lines:
            c_line.clicked.connect(self.audio_check.slider.play_pause)
        self.audio_check.slider.end_signal.connect(self.play_end)

    def play_end(self):
        for c_line in self.stc_line.clickable_lines:
            c_line.setChecked(not c_line.isChecked())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    st = "The human body has an estimated 37.2 trillion cells. Each type of cell has a unique job. " \
         "Knowing each cell's job can help scientists better understand health and diseases such as cancer."
    mu = r"D:\cai_dev\PyQt_Widges\audio\123.mp3"
    cc = AudioPieceSelector(mu, st)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
