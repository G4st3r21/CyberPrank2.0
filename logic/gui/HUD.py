from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush

from game.logic.game.Controllable import Controllable


class HUD:
    @staticmethod
    def draw_hp(painter: QPainter, obj: Controllable):
        x, y = obj.x + 15, obj.y - 15
        hp = int(obj.hp) if obj.hp > 0 else 0

        # Наполнение
        rect = QRect(x, y, hp, 10)
        painter.setPen(QPen(Qt.red, 5))
        painter.fillRect(rect, QColor(Qt.red))

        # Обводка(наложение)
        rect = QRect(x, y, 100, 10)
        painter.setBrush(QBrush(QColor(255, 0, 0, 128), Qt.SolidPattern))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(rect)
