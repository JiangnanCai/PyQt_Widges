from typing import List
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEvent, Qt


class SmoothScrollBar(QtWidgets.QScrollBar):
    """ Smooth scroll bar
        # https://www.cnblogs.com/zhiyiYo/p/17066835.html
    """

    scrollFinished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QScrollBar.__init__(self, parent)
        self.ani = QtCore.QPropertyAnimation()
        self.ani.setTargetObject(self)
        self.ani.setPropertyName(b"value")
        self.ani.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.ani.setDuration(500)
        self.__value = self.value()
        self.ani.finished.connect(self.scrollFinished)

    def setValue(self, value: int):
        if value == self.value():
            return

        # stop running animation
        self.ani.stop()
        self.scrollFinished.emit()

        self.ani.setStartValue(self.value())
        self.ani.setEndValue(value)
        self.ani.start()

    def scrollValue(self, value: int):
        """ scroll the specified distance """
        self.__value += value
        self.__value = max(self.minimum(), self.__value)
        self.__value = min(self.maximum(), self.__value)
        self.setValue(self.__value)

    def scrollTo(self, value: int):
        """ scroll to the specified position """
        self.__value = value
        self.__value = max(self.minimum(), self.__value)
        self.__value = min(self.maximum(), self.__value)
        self.setValue(self.__value)

    def resetValue(self, value):
        self.__value = value

    def mousePressEvent(self, e):
        self.ani.stop()
        super().mousePressEvent(e)
        self.__value = self.value()

    def mouseReleaseEvent(self, e):
        self.ani.stop()
        super().mouseReleaseEvent(e)
        self.__value = self.value()

    def mouseMoveEvent(self, e):
        self.ani.stop()
        super().mouseMoveEvent(e)
        self.__value = self.value()


class SmoothScrollArea(QtWidgets.QScrollArea):
    """ Smooth scroll area """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hScrollBar = SmoothScrollBar()
        self.vScrollBar = SmoothScrollBar()
        self.hScrollBar.setOrientation(Qt.Horizontal)
        self.vScrollBar.setOrientation(Qt.Vertical)
        self.setVerticalScrollBar(self.vScrollBar)
        self.setHorizontalScrollBar(self.hScrollBar)

    def setScrollAnimation(self, orient, duration, easing=QtCore.QEasingCurve.OutCubic):
        bar = self.hScrollBar if orient == Qt.Horizontal else self.vScrollBar
        bar.ani.setDuration(duration)
        bar.ani.setEasingCurve(easing)

    def wheelEvent(self, e):
        if e.modifiers() == Qt.NoModifier:
            self.vScrollBar.scrollValue(-e.angleDelta().y())
        else:
            self.hScrollBar.scrollValue(-e.angleDelta().x())


class SwipeAction(SmoothScrollArea):
    _ALWAYS_OFF = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    _FRAME_LESS = Qt.FramelessWindowHint

    start_pos = None
    is_mouse_pressed = False
    delta = QtCore.QPoint()
    RIGHT = "right"

    def __init__(self,
                 widgets: List[QtWidgets.QWidget],
                 drag_orient: str = "right",
                 parent=None):
        super(SwipeAction, self).__init__(parent)

        self.widgets = SwipeAction.validate_widgets(widgets)
        self.orient = drag_orient
        self.sa_w = self._sa_w
        self.sa_h = self._sa_h

        self.h_bar = self.horizontalScrollBar()

        self.widget = QtWidgets.QWidget(self)
        self.widget.setFixedSize(self.sa_w, self.sa_h)

        self.init_inner_widget()
        self.init_UI()

    @staticmethod
    def validate_widgets(widgets: List[QtWidgets.QWidget]):
        if widgets is not None:
            return widgets
        raise Exception("no widgets")

    @property
    def _sa_w(self) -> int:
        return int(sum([wid.width() for wid in self.widgets]))

    @property
    def _sa_h(self) -> int:
        height = self.widgets[0].height()
        # 如果列表内的组件的高度不一致，则不符合要求
        if any(wid.height() != height for wid in self.widgets):
            raise Exception("all widgets should have same height.")
        return height

    def init_UI(self):
        self.setWidget(self.widget)

        self.setFixedSize(
            self.widgets[0].width()
            if self.orient == self.RIGHT
            else self.widgets[-1].width(),
            self.sa_h  # 消除垂直方向的微小垂直空间
        )
        self.setWindowFlag(self._FRAME_LESS)
        self.setVerticalScrollBarPolicy(self._ALWAYS_OFF)
        self.setHorizontalScrollBarPolicy(self._ALWAYS_OFF)
        self.setStyleSheet("QScrollArea { border: none; } QScrollBar { border: none; }")

        # 注意：这里我们不能直接对滚动条调用 setValue()，因为内容小部件还没有被完全布局
        # 所以我们需要使用 QTimer 来在事件循环开始后设置滚动条位置
        QtCore.QTimer.singleShot(0, self.scrollToRight)

    def scrollToRight(self):
        init_val = self.h_bar.minimum() if self.orient == self.RIGHT else self.h_bar.maximum()
        self.h_bar.setValue(init_val)

    def init_inner_widget(self):
        start_w = 0
        for inner_widget in self.widgets:
            inner_widget.setParent(self.widget)
            inner_widget.move(start_w, 0)
            inner_widget.installEventFilter(self)
            start_w += inner_widget.width()

    def mouse_press_handle(self, event) -> bool:
        self.is_mouse_pressed = True
        self.start_pos = event.pos()
        return False

    def mouse_move_handle(self, event):
        if not self.is_mouse_pressed:
            return
        self.delta = event.pos() - self.start_pos
        set_val = self.h_bar.maximum() if self.delta.x() < 0 else self.h_bar.minimum()
        self.h_bar.setValue(set_val)
        return True

    def mouse_release_handle(self):
        self.is_mouse_pressed = False
        if abs(self.delta.x()) < 10 and abs(self.delta.y()) < 10:
            return False
        else:
            self.delta = QtCore.QPoint()
            return True

    def eventFilter(self, source, event) -> bool:
        if source not in self.widgets:
            pass
        if event.type() == QEvent.MouseButtonPress:
            return self.mouse_press_handle(event)
        elif event.type() == QEvent.MouseMove:
            return self.mouse_move_handle(event)
        elif event.type() == QEvent.MouseButtonRelease:
            return self.mouse_release_handle()
        return super().eventFilter(source, event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    buttons = []
    buttons_config = [
        {"text": "Btn 1", "width": 200, "height": 50},
        {"text": "Btn 2", "width": 50, "height": 50},
        {"text": "Btn 3", "width": 50, "height": 50},
    ]
    for button_data in buttons_config:
        button_height = button_data.get("height")
        button_width = button_data.get("width")
        button_text = button_data.get("text")

        button = QtWidgets.QPushButton(text=button_text)
        button.setFixedSize(button_width, button_height)
        buttons.append(button)

    swipe_action = SwipeAction(widgets=buttons, drag_orient="right")
    swipe_action.show()
    sys.exit(app.exec())
