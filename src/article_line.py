import sys

from PyQt5 import QtWidgets, QtCore, QtGui

from sentence_line import SentenceLine


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
        for stc_line in self.stc_lines:
            if stc_line == self.sender():
                continue
            if state:
                stc_line.set_not_checked()


if __name__ == '__main__':
    # art = [
    #     "Imagine a wheelchair equipped with wheels flexible enough to move over all kinds of barriers, including the raised edges of streets.",
    #     "A robotic delivery vehicle could use the same wheels to go up stairs to deliver food or other purchases.",
    #     "This is what researchers from the Korea Institute of Machinery and Materials, or KIMM,",
    #     "see as the future for their morphing wheel. The wheels can change their shape and can roll over barriers",
    #     "up to 1.3 times their radius. The radius of a wheel is half its height. Other possible applications for the morphing wheel include robots that gather information about an enemy in the battlefield.",
    #     "The KIMM team also hopes that morphing wheels will one day be used with two and four legad robots.",
    #     "Now the movement of those machines is limited. Too much shaking is also a problem. With the morphing wheels, the robots could carry objects that need",
    #     "smooth movement for industrial use. Songhook is the lead researcher at South Korea's KIMM and a member of the AI robotics research team.",
    #     "He said the goal is to make the wheels work at the average speed of a car. That is about 100 kilometers per hour.",
    #     "Wheels developed for a similar purpose, such as airless wheels have flexibility, but are limited in their ability to overcome barriers.",
    #     "Said Songhook. The difference between airless wheels and the morphing wheel is that airless wheels are always soft,",
    #     "but the morphing wheels can change from hard to soft when they meet a barrier.",
    #     "They can then return to being hard to permit faster travel where there are no barriers.",
    #     "The morphing wheel is made of an outer circle of chain and a series of wires running through its central hub.",
    #     "A sensor controls the stiffness of the wires in reaction to the barriers in its path.",
    #     "Song's team demonstrated to riders a model of a wheelchair riding on morphing wheels as it climbed stairs with 18 centimeter steps.",
    #     "The team has also tested a device using the wheel at speeds of up to 30 kilometers an hour.",
    #     "I'm Andrew Smith.",
    # ]
    #
    # app = QtWidgets.QApplication(sys.argv)
    # aud = r"D:\cai_dev\PyQt_Widges\audio\123.mp3"
    # cc = ArticleLine(art)
    # cc.setWindowTitle('PyQt5 Demo')
    # cc.show()
    # sys.exit(app.exec_())
    # ------------------------------------------------------------------------------------------------------------------
    from data_parser import article_object

    app = QtWidgets.QApplication(sys.argv)
    a2 = ArticleLine2(article_object, 400)
    a2.show()
    sys.exit(app.exec_())


