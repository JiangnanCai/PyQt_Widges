import sys

import datetime
from collections import defaultdict

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPalette

datas = {
    "2024-07-28": "2",
    "2024-07-29": "5",
    "2024-07-30": "8",
    "2024-07-31": "2",
    "2024-08-01": "1",
    "2024-08-08": "2",
    "2024-08-20": "12",
    "2024-08-25": "5",
    "2024-08-28": "2",
    "2024-08-31": "7",
    "2024-09-01": "2",
    "2024-09-18": "2",
    "2024-09-28": "5",
    "2024-09-30": "32",
    "2024-10-28": "1",
    "2024-11-28": "2",
    "2024-12-21": "12",
    "2024-12-28": "2",
    "2024-02-14": "4",
    "2024-02-26": "15",
    "2024-11-26": "32",
}


class QCommitCalendar(QWidget):
    naive = ('#ebedf0', '#c6e48b', '#7bc96f', '#239a3b', '#196127')  # GitHub原配色
    velvet = ('#ebedf0', '#e1eec3', '#e6bea1', '#ea8e7f', '#f05053')  # 桃阳红配色
    week = {0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"}
    month = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
             7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    def __init__(self,
                 commit_data: dict,
                 block_size: int = 15,  # commit方块的大小
                 block_spacing: int = 5,  # commit方块的空隙
                 orientation: str = 'right',  # 图表的朝向，GitHub是朝右的，这里还可以朝左
                 parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        assert block_size >= 10
        assert block_spacing > 0
        assert orientation in ('right', 'left')

        self.commit_dict = commit_data
        self.b_size = block_size
        self.b_spacing = block_spacing
        self.orient = orientation

        self.item_size = self.b_size + block_spacing

        self.color_map = self.naive

        self._today = datetime.date.today()

        self._painter = QPainter(self)
        self.init_ui()

    def init_ui(self):
        self.resize(250, self.item_size * 10)
        self.setMinimumSize(250, self.item_size * 10)
        self.setMaximumWidth(self.item_size * 60)
        self.setMaximumHeight(self.item_size * 10)
        self.setStyleSheet("background-color: white")

    @property
    def _num_cols(self):
        return int(self.width() / self.item_size) - 4

    def _num2color(self, num_commit: int):
        # commit number to color.
        level = int(num_commit / 5)
        color = self.color_map[3 if level > 3 else level]
        return color

    def get_x(self, col):
        return self.width() - self.item_size * (col + 2) if self.orient == "right" else self.item_size * (col + 1)

    def paint_rect(self):
        delta = 0  # 日期偏移
        month_col = defaultdict(list)
        for cur_col in range(self._num_cols):
            num_rows = self._today.weekday() + 2 if cur_col == 0 else 7
            for cur_row in range(num_rows):
                # get coordinate: x, y
                x = self.get_x(cur_col)
                y = self.item_size * (num_rows - cur_row)

                # get color
                date_delta = self._today - datetime.timedelta(days=delta)
                num_commit = int(self.commit_dict.get(str(date_delta), 0))
                color = self._num2color(num_commit)
                self._painter.setPen(QColor(color))
                self._painter.setBrush(QColor(color))

                # draw rect with color and coordinate
                self._painter.drawRect(x, y, self.b_size, self.b_size)

                month_col[cur_col].append(date_delta.month)
                delta += 1
        return month_col

    def paint_week(self):
        self._painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # 设置画笔颜色和宽度
        self._painter.setFont(QFont('Arial', self.b_size - self.b_spacing))  # 设置字体
        x = self.get_x(self._num_cols + 1)
        for row in range(7):
            y = self.item_size * (7 - row) + self.b_size
            self._painter.drawText(QPoint(x, y), self.week.get(row))

    def paint_month(self, month_col):
        y = self.item_size * 8 + self.b_size - self.b_spacing
        tmp_month = self._today.month
        for key, value in month_col.items():
            cur_month = max(list(set(value)))
            if cur_month != tmp_month:
                x = self.get_x(key)
                self._painter.drawText(QPoint(x, y), self.month.get(tmp_month))
                tmp_month = cur_month

    def paintEvent(self, paint_event):

        self._painter.begin(self)

        month_cols = self.paint_rect()
        self.paint_week()
        self.paint_month(month_cols)

        self._painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cc = QCommitCalendar(commit_data=datas)
    cc.setWindowTitle('PyQt5 Demo')
    cc.show()
    sys.exit(app.exec_())
