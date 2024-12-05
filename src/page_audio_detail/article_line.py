import sys

from PyQt5 import QtWidgets, QtCore, QtGui

from src.common_widget.sentence_line import SentenceLine


class ArticleLine(QtWidgets.QWidget):
    def __init__(self, article, width, parent=None):
        super(ArticleLine, self).__init__(parent)
        self.segments = article.segments

        self.setFixedWidth(width)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)

        self.stc_lines = []
        for seg in self.segments:
            stc_line = SentenceLine(seg.text, width, self)
            stc_line.start_time = seg.start * 1000
            stc_line.end_time = seg.end * 1000

            stc_line.checked_signal.connect(self.set_exclusive)
            self.stc_lines.append(stc_line)
            self.layout().addWidget(stc_line)

    def set_exclusive(self, state):
        # 只有 state 是 True 的时候才会采用，将除 sender 之外的变成暗的
        for stc_line in self.stc_lines:
            if stc_line == self.sender():
                continue
            if state and stc_line.is_checked:
                stc_line.set_not_checked()


if __name__ == '__main__':
    from data_parser import article_object

    app = QtWidgets.QApplication(sys.argv)
    a2 = ArticleLine(article_object, 400)
    a2.show()
    sys.exit(app.exec_())


