import sys

from PyQt5 import QtWidgets
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
                    border-radius: 5;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #9A9A9A;
                    border-radius: 5;
                    border: none;
                }
                QPushButton:checked {
                    background-color: #93D2F3;
                    border-radius: 5;
                    border: none;
                }
            """
        self.setStyleSheet(css)


class SentenceLine(QtWidgets.QWidget):
    def __init__(self, text, width, parent=None):
        super(SentenceLine, self).__init__(parent)
        self.text = text
        self.setFixedWidth(width)
        self.setWindowFlag(Qt.FramelessWindowHint)

        clickable_line = ClickableLine("")
        self.font = clickable_line.font()
        self.font_metrics = QFontMetrics(self.font)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)

        self.clickable_lines = []
        self.lines = self.get_lines()
        max_len = len(max(self.lines, key=len))
        for index, line in enumerate(self.lines):

            new_line = line + ' ' * (max_len - len(line)) \
                if len(line) < max_len \
                   and index != len(self.lines)-1 \
                else line

            c_line = ClickableLine(new_line, self)
            c_line.clicked.connect(self.state_synchronize)

            self.clickable_lines.append(c_line)
            self.layout.addWidget(c_line)

    def state_synchronize(self):
        sender = self.sender()  # 获取发送信号的复选框
        for c_line in self.clickable_lines:
            c_line.setChecked(sender.isChecked())

    def get_lines(self):
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
                lines.append(' '.join(words[start:end-1]))
                start = end-1

        if start != len(words):
            lines.append(' '.join(words[start:len(words)]))

        return lines


if __name__ == '__main__':

    # app = QApplication(sys.argv)
    # st = "The human body has an estimated 37.2 trillion cells. Each type of cell has a unique job. " \
    #      "Knowing each cell's job can help scientists better understand health and diseases such as cancer."
    # cc = ClickableLine(st)
    # cc.setWindowTitle('PyQt5 Demo')
    # cc.show()
    # sys.exit(app.exec_())
    # ------------------------------------------------------------------------------------------------------------------
    app = QApplication(sys.argv)
    st = "The human body has an estimated 37.2 trillion cells. Each type of cell has a unique job. " \
         "Knowing each cell's job can help scientists better understand health and diseases such as cancer."
    cc = SentenceLine(st, 100)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
    # ------------------------------------------------------------------------------------------------------------------
