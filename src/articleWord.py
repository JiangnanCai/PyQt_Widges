import sys

from PyQt5 import QtWidgets, QtCore, QtGui

from sentenceWord import SentenceWord


class ArticleWord(QtWidgets.QWidget):
    def __init__(self, article, width, parent=None):
        super(ArticleWord, self).__init__(parent)
        self.lines = article
        self.setFixedWidth(width)

        self.layout = QtWidgets.QVBoxLayout(self)
        # self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        self.sentence_lines = []
        self.button_group = QtWidgets.QButtonGroup(self)
        for line in self.lines:
            sentence_word = SentenceWord(line, width-15, self)
            for word in sentence_word.words:
                self.button_group.addButton(word)
            self.sentence_lines.append(sentence_word)
            self.layout.addWidget(sentence_word)
            spacer = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.layout.addSpacerItem(spacer)
            # self.add_spliter()
        self.button_group.setExclusive(True)

    def add_spliter(self):
        h_line = QtWidgets.QFrame()
        h_line.setStyleSheet("background-color: gray;")
        h_line.setFrameShape(QtWidgets.QFrame.HLine)
        # h_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.layout.addWidget(h_line)

    def set_exclusive(self, bool_val):
        for s_line in self.sentence_lines:
            if s_line == self.sender():
                continue
            if s_line.is_checked == bool_val and bool_val:
                s_line.set_state(not bool_val)


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

    app = QtWidgets.QApplication(sys.argv)
    aud = r"D:\cai_dev\PyQt_Widges\audio\123.mp3"
    cc = ArticleWord(art, 400)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())

