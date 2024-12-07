import os.path
import sys
import time

from PyQt5 import QtWidgets, QtCore, QtMultimedia, QtGui

SIZE_EXPAND = QtWidgets.QSizePolicy.Expanding
SIZE_MINI = QtWidgets.QSizePolicy.Minimum
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSET_DIR = os.path.join(ROOT_DIR, "asset")
AUDIO_DIR = os.path.join(ROOT_DIR, "audio")


def pos2strftime(position):
    return time.strftime('%M:%S', time.localtime(position / 1000))


class TitleTimeLabel(QtWidgets.QWidget):
    def __init__(self, title, date, parent=None):
        super(TitleTimeLabel, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QtWidgets.QLabel(title)
        self.date_label = QtWidgets.QLabel(date)

        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.date_label)
        self.layout.setContentsMargins(0, 0, 0, 0)


class AudioSlider(QtWidgets.QSlider):
    is_loop = False
    start_time = None
    end_time = None
    FIFTEEN_SECOND = 15 * 1000
    time_signal = QtCore.pyqtSignal(str, str)
    end_signal = QtCore.pyqtSignal(bool)

    def __init__(self, audio, parent=None):
        super(AudioSlider, self).__init__(QtCore.Qt.Horizontal, parent)
        self.setStyleSheet("""
                   QSlider:groove:horizontal {
                       border: 0px solid #bbb;
                   }

                   QSlider:sub-page:horizontal {
                       background: #93D2F3;
                       border-radius: 2px;
                       margin-top:8px;
                       margin-bottom:8px;
                   }

                   QSlider::add-page:horizontal {
                       background: rgb(230,230,230);
                       border: 0px solid #777;
                       border-radius: 2px;
                       margin-top:9px;
                       margin-bottom:9px;
                   }

                   QSlider::handle:horizontal {
                       background: rgb(193,204,208);
                       width: 5px;
                       border: 1px solid rgb(193,204,208);
                       border-radius: 2px;
                       margin-top:6px;
                       margin-bottom:6px;
                   }

                   QSlider::handle:horizontal:hover {
                       background: rgb(193,204,208);
                       width: 10px;
                       border: 1px solid rgb(193,204,208);
                       border-radius: 5px;
                       margin-top:4px;
                       margin-bottom:4px;
                   }
               """)
        self.setSliderPosition(0)

        self.player = QtMultimedia.QMediaPlayer(None)
        self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(audio)))

        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player.positionChanged.connect(self.update_slider_position)
        self.sliderMoved.connect(self.seek_in_media)

        self.setRange(0, 10000)
        self.timer = QtCore.QTimer(self)

    def on_media_status_changed(self, status):
        if status == QtMultimedia.QMediaPlayer.LoadedMedia:
            self.setRange(0, self.player.duration())
            self.time_signal.emit(pos2strftime(self.player.position()),
                                  pos2strftime(self.player.duration()))

    def update_slider_position(self):

        self.setValue(self.player.position())
        self.time_signal.emit(pos2strftime(self.player.position()),
                              pos2strftime(self.player.duration()))
        if self.player.position() == self.player.duration():
            self.end_signal.emit(True)
            self.player.stop()

    def seek_in_media(self):
        position = self.value()
        self.player.setPosition(position)

    def play_pause(self):
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def play_range(self, start_time, end_time, once=True):
        self.play_pause()
        self.start_time = start_time
        self.end_time = end_time
        self.player.setPosition(start_time)  # 设置开始位置

        if once:
            self.timer.timeout.connect(self._end_directly)
        else:
            self.timer.timeout.connect(self._replay)  # 超时后停止播放
        self.timer.start(end_time - start_time)  # 设置超时时间为结束时间减去开始时间

        self.player.play()  # 开始播放

    def _end_directly(self):
        self.player.pause()
        self.end_signal.emit(True)
        self.timer.stop()

    def _replay(self):
        if not self.is_loop:
            self.timer.stop()
        self.play_pause()
        self.player.setPosition(self.start_time)
        self.play_pause()

    def back_15_second(self):
        self.play_pause()
        self.player.setPosition(max(self.value() - self.FIFTEEN_SECOND, 0))
        self.play_pause()

    def forward_15_second(self):
        self.play_pause()
        self.player.setPosition(min(self.value() + self.FIFTEEN_SECOND, self.player.duration()))
        self.play_pause()


class TimeLabel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TimeLabel, self).__init__(parent)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.start = QtWidgets.QLabel()
        self.end = QtWidgets.QLabel()

        self.layout.addWidget(self.start)
        self.layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, SIZE_EXPAND, SIZE_MINI))
        self.layout.addWidget(self.end)


class AudioButtons(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AudioButtons, self).__init__(parent)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.play_mode = QtWidgets.QPushButton()
        self.play_mode.setIcon(QtGui.QIcon(os.path.join(ASSET_DIR, "循环.svg")))

        self.back_15 = QtWidgets.QPushButton()
        self.back_15.setIcon(QtGui.QIcon(os.path.join(ASSET_DIR, "后退15s.svg")))

        # button: play and stop
        self.play_stop = QtWidgets.QPushButton()
        self.play()

        self.forward_15 = QtWidgets.QPushButton()
        self.forward_15.setIcon(QtGui.QIcon(os.path.join(ASSET_DIR, "快进15s.svg")))

        self.delete = QtWidgets.QPushButton()
        # self.delete.setVisible(False)
        self.delete.setIcon(QtGui.QIcon(os.path.join(ASSET_DIR, "删除.svg")))

        self.layout.addWidget(self.play_mode)
        self.layout.addStretch(1)
        self.layout.addWidget(self.back_15)
        self.layout.addWidget(self.play_stop)
        self.layout.addWidget(self.forward_15)
        self.layout.addStretch(1)
        self.layout.addWidget(self.delete)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 5;
                padding: 3,3,3,3;
            }
            QPushButton:hover {
                background-color: #CECECE;
                border-radius: 5;
                padding: 3,3,3,3;
            }
        """)

    def play(self):
        self.play_stop.setIcon(QtGui.QIcon(os.path.join(ASSET_DIR, "播放2.svg")))

    def stop(self):
        self.play_stop.setIcon(QtGui.QIcon(os.path.join(ASSET_DIR, "暂停.svg")))


class AudioPlayer(QtWidgets.QWidget):
    audio_piece_signal = QtCore.pyqtSignal(int, int, bool)

    def __init__(self, title, date, audio, parent=None):
        super(AudioPlayer, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.title_date = TitleTimeLabel(title, date)
        self.layout.addWidget(self.title_date)

        self.slider = AudioSlider(audio)
        self.layout.addWidget(self.slider)

        self.time_label = TimeLabel()
        self.layout.addWidget(self.time_label)

        self.audio_buttons = AudioButtons()
        self.layout.addWidget(self.audio_buttons)

        self.spacer = QtWidgets.QSpacerItem(0, 0, SIZE_MINI, SIZE_EXPAND)
        self.layout.addSpacerItem(self.spacer)

        self.audio_buttons.play_stop.clicked.connect(self.slider.play_pause)
        self.audio_buttons.play_stop.clicked.connect(self.on_play_stop_clicked)
        self.audio_buttons.back_15.clicked.connect(self.slider.back_15_second)
        self.audio_buttons.forward_15.clicked.connect(self.slider.forward_15_second)

        self.audio_piece_signal.connect(self.slider.play_range)
        self.slider.time_signal.connect(self.update_time)
        self.slider.end_signal.connect(self.on_play_stop_clicked)

        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtCore.Qt.white)
        self.setPalette(palette)

    def update_time(self, cur_time, end_time):
        self.time_label.start.setText(cur_time)
        self.time_label.end.setText(end_time)

    def on_play_stop_clicked(self, *args):
        if self.slider.player.state() != QtMultimedia.QMediaPlayer.PlayingState:
            self.audio_buttons.play()
        else:
            self.audio_buttons.stop()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mu = os.path.join(AUDIO_DIR, "123.mp3")
    cc = AudioPlayer("珠海", "2024-11-22", mu)
    # cc = AudioSlider(mu)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
