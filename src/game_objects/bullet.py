import math

import config
from game_objects.game_object import GameObject

from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Bullet(GameObject):

    def __init__(self, location: QPoint, degree: int):
        super().__init__(location, QSize(4, 4), 12, degree)

    def update(self):
        self.location.setX(int(self.location.x() + self.speed * math.sin(math.pi / 180 * self.degree)))
        self.location.setY(int(self.location.y() - self.speed * math.cos(math.pi / 180 * self.degree)))
        

    def draw(self, painter: QPainter):
        painter.setPen(QPen(QColor(Qt.white), 2))
        painter.translate(self.location.x(), self.location.y())
        painter.drawRoundedRect(0, 0, self.size.width(), self.size.height(), 1, 1)
        painter.translate(-self.location.x(), -self.location.y())

    def isOutOfView(self):
        return not (0 <= self.location.x() <= config.WINDOW_WIDTH and 0 <= self.location.y() <= config.WINDOW_HEIGHT)

    def isCollide(self, other):
        return (self.location.x() < other.location.x() + other.size.width() and
                self.location.x() + self.size.width() > other.location.x() and
                self.location.y() < other.location.y() + other.size.height() and
                self.location.y() + self.size.height() > other.location.y())

    def __repr__(self):
        return f"({self.location.x()}, {self.location.y()})"

