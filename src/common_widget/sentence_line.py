import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics


class ClickableLine(QtWidgets.QPushButton):
    padding = 2

    def __init__(self, text, parent=None):
        super(ClickableLine, self).__init__(parent)

        self.setText(text)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.set_style()
        self.adjust_size(text)
        self.setCheckable(True)

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


class SentenceLine(QtWidgets.QWidget):
    checked_signal = QtCore.pyqtSignal(bool)
    audio_play_signal = QtCore.pyqtSignal(float, float)
    audio_pause_signal = QtCore.pyqtSignal(bool)
    is_checked = False

    start_time = 0.
    end_time = 0.

    def __init__(self, sentence, width, parent=None):
        super(SentenceLine, self).__init__(parent)
        self.text = sentence
        self.setFixedWidth(width)
        self.setWindowFlag(Qt.FramelessWindowHint)

        clickable_line = ClickableLine("")
        self.font = clickable_line.font()
        self.font_metrics = QFontMetrics(self.font)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.lines = self._lines
        self.clickable_lines = self._clickable_lines

    @property
    def _clickable_lines(self):
        res = []
        max_len = max(len(line) for line in self.lines)

        align_lines = [
            line.ljust(max_len)
            if index != len(self.lines) - 1
            else line
            for index, line in enumerate(self.lines)
        ]

        for line in align_lines:
            c_line = ClickableLine(line, self)
            c_line.clicked.connect(self.state_synchronize)
            self.layout().addWidget(c_line)

            res.append(c_line)
        return res

    def state_synchronize(self):
        state = self.sender().isChecked()
        # state: 新状态
        # self.is_check 老状态
        # ---------------------------------------------------------------
        # 这种情况就是点击高亮，然后点击取消高亮，两种状态之间切换
        # if state:
        #     self.set_checked()
        #     self.audio_play_signal.emit(self.start_time, self.end_time)
        # else:
        #     self.set_not_checked()
        #     self.audio_pause_signal.emit(True)
        # ---------------------------------------------------------------
        # 这种就是只有一种状态，只有从非高亮 -> 高亮的状态
        self.set_checked()
        self.audio_play_signal.emit(self.start_time, self.end_time)

    def set_checked(self):
        for c_line in self.clickable_lines:
            c_line.setChecked(True)
        self.is_checked = True
        self.checked_signal.emit(True)

    def set_not_checked(self):
        for c_line in self.clickable_lines:
            c_line.setChecked(False)
        self.is_checked = False
        # self.checked_signal.emit(False)  # 点灭的时候就不需要发信号了，因为只有亮的时候才需要 exclusive

    @property
    def _lines(self):
        if not self.text:
            return []

        words = [word for word in self.text.split()]

        lines = []
        start, end = 0, 0
        while end <= len(words):
            cur_text = words[start:end]
            if self.font_metrics.width(' '.join(cur_text)) + 2 * len(cur_text) < self.width():
                end += 1
                continue
            else:
                lines.append(' '.join(words[start:end - 1]))
                start = end - 1

        if start != len(words):
            lines.append(' '.join(words[start:len(words)]))

        return lines


if __name__ == '__main__':
    app = QApplication(sys.argv)
    st = "The human body has an estimated 37.2 trillion cells. Each type of cell has a unique job. " \
         "Knowing each cell's job can help scientists better understand health and diseases such as cancer."
    cc = SentenceLine(st, 300)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
