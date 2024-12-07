import os
import sys
import functools

from PyQt5 import QtWidgets, QtCore

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.page_audio_detail.article_line import ArticleLine
from src.page_audio_detail.article_word import ArticleWord
from src.page_audio_detail.audio_player import AudioPlayer
from src.common_widget.top_bar import TopBar


class MyAudioDetailScrollArea(QtWidgets.QScrollArea):
    def __init__(self,
                 article,
                 width: int,
                 height: int,
                 keyword: str,
                 parent=None):
        super(MyAudioDetailScrollArea, self).__init__(parent)
        self.setFixedSize(width - 30, height - 240)

        self.setWidget(
            ArticleLine(article, self.width())
            if keyword == "Line"
            else ArticleWord(article, self.width())
        )

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("QWidget {border: 0px; background-color: white; border-radius: 10px;}")


class PageAudioDetail(QtWidgets.QWidget):
    return_signal = QtCore.pyqtSignal()

    def __init__(self,
                 article,
                 title,
                 date,
                 audio,
                 width,
                 height,
                 parent=None):
        super(PageAudioDetail, self).__init__(parent)

        self.setFixedSize(width, height)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.top_bar = TopBar(title)
        self.top_bar.setFixedHeight(50)
        self.top_bar.button_left.clicked.connect(self._return_signal_emit)

        self.audio_play = AudioPlayer(title, date, audio)
        self.audio_play.setFixedHeight(130)

        self.page_line = MyAudioDetailScrollArea(article, width, height, "Line")
        self.page_line_signal_slot()

        self.page_word = MyAudioDetailScrollArea(article, width, height, "Word")
        self.page_word_signal_slot()

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.page_line, "分句")
        self.tab_widget.addTab(self.page_word, "分词")

        self.layout.addWidget(self.top_bar)
        self.layout.addWidget(self.audio_play)
        self.layout.addWidget(self.tab_widget)

    def page_line_signal_slot(self):
        for segment in self.page_line.widget().stc_lines:
            segment.audio_play_signal.connect(self.audio_play.slider.play_range)
            segment.audio_pause_signal.connect(self.audio_play.slider.player.pause)

            segment.audio_play_signal.connect(self.audio_play.on_play_stop_clicked)
            segment.audio_pause_signal.connect(self.audio_play.on_play_stop_clicked)

            self.audio_play.slider.end_signal.connect(segment.set_not_checked)
            self.audio_play.slider.player.positionChanged.connect(
                functools.partial(self.play_in_range_segment, segment)
            )

    def page_word_signal_slot(self):
        for stc_words in self.page_word.widget().sentence_lines:
            for word in stc_words.words:
                word.audio_play_signal.connect(self.audio_play.slider.play_range)

                # # todo: 应该是一个时间轴，而不是这样的文件，类似字幕的 srt 文件吧
                self.audio_play.slider.player.positionChanged.connect(
                    functools.partial(self.play_in_range_word, word)
                )

    def _return_signal_emit(self):
        self.return_signal.emit()

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
    cc = PageAudioDetail(article_object, "美丽湾", "2024-12-03", aud, 360, 640)

    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
