import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics


class ClickableWord(QtWidgets.QPushButton):
    padding = 1
    start_time = 0.0
    end_time = 0.0
    audio_play_signal = QtCore.pyqtSignal(float, float)

    def __init__(self, text, parent=None):
        super(ClickableWord, self).__init__(parent)
        self.setText(text)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.text = text
        self.set_style()
        self.adjust_size(text)
        self.setCheckable(True)

        self.clicked.connect(self.word_play)

    def word_play(self):
        self.audio_play_signal.emit(int(self.start_time * 1000), int(self.end_time * 1000))

    def adjust_size(self, text):
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(text)
        text_height = font_metrics.height()

        self.setFixedSize(text_width + 2 * self.padding,
                          text_height + 2 * self.padding)

    def set_style(self):
        css = """
            QPushButton {
                background-color: #CECECE;
                border-radius: 3px;
                border: none;
            }
            QPushButton:hover {
                background-color: #9A9A9A;
                border-radius: 3px;
                border: none;
            }
            QPushButton:checked {
                background-color: #93D2F3;
                border-radius: 3px;
                border: none;
            }
        """
        self.setStyleSheet(css)


class LineWord(QtWidgets.QWidget):
    def __init__(self, text_buttons, width, parent=None):
        super(LineWord, self).__init__(parent)

        self.setFixedWidth(width)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.words = text_buttons
        for word in self.words:
            self.layout.addWidget(word)
        self.spacer_h = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout.addItem(self.spacer_h)


class SentenceWord(QtWidgets.QWidget):
    def __init__(self, segment, width, parent=None):
        super(SentenceWord, self).__init__(parent)

        self.setFixedWidth(width)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setLayout( QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.segment = segment
        self.words = self._words
        self.lines = self._lines

        for line in self.lines:
            line_word = LineWord(line, self.width(), self)
            self.layout().addWidget(line_word)

        self.spacer_v = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout().addSpacerItem(self.spacer_v)

    @property
    def _words(self):
        if not self.segment.words:
            return []

        words = []
        button_group = QtWidgets.QButtonGroup(self)
        button_group.setExclusive(True)

        for word in self.segment.words:
            c_word = ClickableWord(word.text)

            c_word.start_time = word.start
            c_word.end_time = word.end

            button_group.addButton(c_word)
            words.append(c_word)

        return words

    @property
    def _lines(self):
        if not self.words:
            return []

        lines = []
        cur_line = []
        cur_width = 0

        for word in self.words:
            word_width = word.width() + 5
            if cur_width + word_width <= self.width():
                cur_line.append(word)
                cur_width += word_width
            else:
                lines.append(cur_line)
                cur_line = [word]
                cur_width = word_width

        if cur_line:
            lines.append(cur_line)

        return lines


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # cc = ClickableWord("day")
    # cc.setWindowTitle('PyQt5 Demo')
    # cc.show()
    # sys.exit(app.exec_())
    # ------------------------------------------------------------------------------------------------------------------
    # app = QApplication(sys.argv)
    #
    # sentence = "It's a good day."
    # buttons = [ClickableWord(word) for word in sentence.split()]
    # buttons_width = sum([button.width() for button in buttons])
    # w = buttons_width + len(buttons) * 7
    #
    # cc = LineWord(buttons, w)
    # cc.setWindowTitle('PyQt5 Demo')
    # cc.show()
    # sys.exit(app.exec_())
    # ------------------------------------------------------------------------------------------------------------------
    app = QApplication(sys.argv)
    st = "The human body has an estimated 37.2 trillion cells. Each type of cell has a unique job. " \
        "Knowing each cell's job can help scientists better understand health and diseases such as cancer."
    cc = SentenceWord(st, 400)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())



