import sys

from PyQt5 import QtWidgets, QtCore, QtGui

from src.common_widget.sentence_word import SentenceWord


class ArticleWord(QtWidgets.QWidget):
    def __init__(self, article, width, parent=None):
        super(ArticleWord, self).__init__(parent)
        self.setFixedWidth(width)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.sentence_lines = []
        self.button_group = QtWidgets.QButtonGroup(self)

        for segment in article.segments:
            stc_word = SentenceWord(segment, width-15, self)
            for word in stc_word.words:
                self.button_group.addButton(word)
            self.sentence_lines.append(stc_word)
            self.layout().addWidget(stc_word)
            spacer = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.layout().addSpacerItem(spacer)
        self.button_group.setExclusive(True)


if __name__ == '__main__':
    from data_parser import article_object
    app = QtWidgets.QApplication(sys.argv)
    aud = r"D:\cai_dev\PyQt_Widges\audio\123.mp3"
    cc = ArticleWord(article_object, 400)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())

