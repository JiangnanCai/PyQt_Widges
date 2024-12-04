import sys

from PyQt5 import QtWidgets, QtCore


from article_line import ArticleLine
# from articleWord import ArticleWord
from audio_player import AudioPlayer


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


class AudioArticlePage(QtWidgets.QWidget):
    def __init__(self, article, title, date, audio, parent=None):
        super(AudioArticlePage, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.audio_play = AudioPlayer(title, date, audio)
        self.layout.addWidget(self.audio_play)

        self.select_buttons = SelectButtons()
        self.layout.addWidget(self.select_buttons)

        self.stack_widget = QtWidgets.QStackedWidget(self)
        self.layout.addWidget(self.stack_widget)

        self.page_line = SentenceLineScrollArea(article)
        for segment in self.page_line.article_widget.stc_lines:
            segment.audio_play_signal.connect(self.audio_play.slider.play_range)
            segment.audio_play_signal.connect(self.audio_play.on_play_stop_clicked)
            segment.audio_pause_signal.connect(self.audio_play.slider.play_pause)
            self.audio_play.slider.end_signal.connect(segment.set_not_checked)

            # todo: 播放的时候，随着语音进度点亮
        # self.page_word = SentenceWordScrollArea(article)

        self.stack_widget.addWidget(self.page_line)
        # self.stack_widget.addWidget(self.page_word)

        self.select_buttons.sentence_base.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        # self.select_buttons.word_base.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))


if __name__ == '__main__':
    art = [
        "Imagine a wheelchair equipped with wheels flexible enough to move over all kinds of barriers, including the raised edges of streets.",
        "A robotic delivery vehicle could use the same wheels to go up stairs to deliver food or other purchases.",
        "This is what researchers from the Korea Institute of Machinery and Materials, or KIMM,",
        "see as the future for their morphing wheel. The wheels can change their shape and can roll over barriers",
        "up to 1.3 times their radius. The radius of a wheel is half its height. Other possible applications for the morphing wheel include robots that gather information about an enemy in the battlefield.",
        "The KIMM team also hopes that morphing wheels will one day be used with two and four legad robots.",
        "Now the movement of those machines is limited. Too much shaking is also a problem. With the morphing wheels, the robots could carry objects that need",
        "smooth movement for industrial use. Songhook is the lead researcher at South Korea's KIMM and a member of the AI robotics research team.",
        "He said the goal is to make the wheels work at the average speed of a car. That is about 100 kilometers per hour.",
        "Wheels developed for a similar purpose, such as airless wheels have flexibility, but are limited in their ability to overcome barriers.",
        "Said Songhook. The difference between airless wheels and the morphing wheel is that airless wheels are always soft,",
        "but the morphing wheels can change from hard to soft when they meet a barrier.",
        "They can then return to being hard to permit faster travel where there are no barriers.",
        "The morphing wheel is made of an outer circle of chain and a series of wires running through its central hub.",
        "A sensor controls the stiffness of the wires in reaction to the barriers in its path.",
        "Song's team demonstrated to riders a model of a wheelchair riding on morphing wheels as it climbed stairs with 18 centimeter steps.",
        "The team has also tested a device using the wheel at speeds of up to 30 kilometers an hour.",
        "I'm Andrew Smith.",
    ]
    from data_parser import article_object
    app = QtWidgets.QApplication(sys.argv)
    aud = r"D:\cai_dev\PyQt_Widges\audio\123.mp3"
    cc = AudioArticlePage(article_object, "美丽湾", "2024-12-03", aud)
    # cc = SelectButtons()
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())

