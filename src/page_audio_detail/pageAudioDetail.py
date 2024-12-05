import sys
import functools

from PyQt5 import QtWidgets, QtCore


from src.page_audio_detail.article_line import ArticleLine
from src.page_audio_detail.article_word import ArticleWord
from src.page_audio_detail.audio_player import AudioPlayer
from src.common_widget.top_bar import TopBar


class SelectButtons(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SelectButtons, self).__init__(parent)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.button_group = QtWidgets.QButtonGroup(self)

        self.sentence_base = QtWidgets.QPushButton("分句")
        self.sentence_base.setCheckable(True)
        self.button_group.addButton(self.sentence_base)

        self.word_base = QtWidgets.QPushButton("分词")
        self.word_base.setCheckable(True)
        self.button_group.addButton(self.word_base)

        self.button_group.setExclusive(True)

        self.spacer_left = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacer_right = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.layout.addSpacerItem(self.spacer_left)
        self.layout.addWidget(self.sentence_base)
        self.layout.addWidget(self.word_base)
        self.layout.addSpacerItem(self.spacer_right)


class SentenceLineScrollArea(QtWidgets.QScrollArea):
    def __init__(self, article, parent=None):
        super(SentenceLineScrollArea, self).__init__(parent)
        self.setFixedSize(400, 400)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.article_widget = ArticleLine(article, 380)
        self.article_widget.setFixedWidth(self.width())

        self.setWidget(self.article_widget)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("QWidget {border: 0px; background-color: white; border-radius: 10px;}")


class SentenceWordScrollArea(QtWidgets.QScrollArea):
    def __init__(self, article, parent=None):
        super(SentenceWordScrollArea, self).__init__(parent)
        self.setFixedSize(400, 400)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.article_widget = ArticleWord(article, 380)
        self.setWidget(self.article_widget)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("QWidget {border: 0px; background-color: white; border-radius: 10px;}")


class PageAudioDetail(QtWidgets.QWidget):
    def __init__(self, article, title, date, audio, parent=None):
        super(PageAudioDetail, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.top_bar = TopBar(title)
        self.layout.addWidget(self.top_bar)

        self.audio_play = AudioPlayer(title, date, audio)
        self.layout.addWidget(self.audio_play)

        self.select_buttons = SelectButtons()
        self.layout.addWidget(self.select_buttons)

        self.stack_widget = QtWidgets.QStackedWidget(self)
        self.layout.addWidget(self.stack_widget)

        self.page_line = SentenceLineScrollArea(article)
        self.page_word = SentenceWordScrollArea(article)

        self.stack_widget.addWidget(self.page_line)
        self.stack_widget.addWidget(self.page_word)

        self.select_buttons.sentence_base.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        self.select_buttons.word_base.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))
        self.stack_widget.currentChanged.connect(self.on_change)

        for segment in self.page_line.article_widget.stc_lines:
            segment.audio_play_signal.connect(self.audio_play.slider.play_range)
            segment.audio_pause_signal.connect(self.audio_play.slider.player.pause)

            segment.audio_play_signal.connect(self.audio_play.on_play_stop_clicked)
            segment.audio_pause_signal.connect(self.audio_play.on_play_stop_clicked)

            self.audio_play.slider.end_signal.connect(segment.set_not_checked)
            self.audio_play.slider.player.positionChanged.connect(
                functools.partial(self.play_in_range_segment, segment)
            )

    def on_change(self):

        if self.stack_widget.currentIndex() == 1:
            for stc_words in self.page_word.article_widget.sentence_lines:
                for word in stc_words.words:
                    word.audio_play_signal.connect(self.audio_play.slider.play_range)

                    # # todo: 应该是一个时间轴，而不是这样的文件，类似字幕的 srt 文件吧
                    self.audio_play.slider.player.positionChanged.connect(
                        functools.partial(self.play_in_range_word, word)
                    )

    def play_in_range_segment(self, segment):
        # 随着录音播放的进度高亮句子

        pos = self.audio_play.slider.player.position()
        if pos in range(int(segment.start_time), int(segment.end_time)):
            if not segment.is_checked:
                segment.set_checked()
        else:
            if segment.is_checked:
                segment.set_not_checked()

        # todo: 某一段高亮的时候，自动放置在中心位置
        # 简易版本，后续优化
        max_scroll_value = self.page_line.verticalScrollBar().maximum()
        max_pos_value = self.audio_play.slider.player.duration()
        set_scroll_value = int((pos / max_pos_value) * max_scroll_value)
        self.page_line.verticalScrollBar().setValue(set_scroll_value)

    def play_in_range_word(self, word):
        pos = self.audio_play.slider.player.position()

        if pos in range(int(word.start_time * 1000), int(word.end_time * 1000)):
            if not word.isChecked():
                word.setChecked(True)
        else:
            if word.isChecked():
                word.setChecked(False)


if __name__ == '__main__':
    from src.data_parser import article_object
    app = QtWidgets.QApplication(sys.argv)
    aud = r"D:\cai_dev\PyQt_Widges\audio\123.mp3"
    cc = PageAudioDetail(article_object, "美丽湾", "2024-12-03", aud)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())

