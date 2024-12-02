import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics


class ClickableWord(QtWidgets.QPushButton):
    padding = 1

    def __init__(self, text, parent=None):
        super(ClickableWord, self).__init__(parent)
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


class LineWord(QtWidgets.QWidget):
    def __init__(self, text_buttons, width, parent=None):
        super(LineWord, self).__init__(parent)

        self.setFixedWidth(width)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(self.layout)

        self.words = text_buttons
        for word in self.words:
            self.layout.addWidget(word)
        self.spacer_h = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout.addItem(self.spacer_h)


class SentenceWord(QtWidgets.QWidget):
    def __init__(self, text, width, parent=None):
        super(SentenceWord, self).__init__(parent)

        self.setFixedWidth(width)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.text = text
        self.words = self._words
        for line in self.get_lines():
            line_word = LineWord(line, self.width(), self)
            self.layout.addWidget(line_word)

        self.spacer_v = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout.addSpacerItem(self.spacer_v)

    @property
    def _words(self):
        if not self.text:
            return []

        words = [ClickableWord(word) for word in self.text.split()]
        button_group = QtWidgets.QButtonGroup(self)
        button_group.setExclusive(True)
        for word in words:
            button_group.addButton(word)
        return words

    def get_lines(self):
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



