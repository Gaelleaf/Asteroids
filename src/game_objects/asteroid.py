import config
import math

from random import uniform, randint

from PyQt5.QtGui import *
from PyQt5.QtCore import *

from game_objects.game_object import GameObject


class Asteroid(GameObject):
    def __init__(self, rank: int = 3, location: QPointF = None):
        location = location or QPointF(randint(0, config.WINDOW_WIDTH), randint(0, config.WINDOW_HEIGHT))
        size = QSize(rank * 40, rank * 40)
        speed = uniform(1.5, 3)
        degree = randint(0, 11) * 30
        super().__init__(location, size, speed, degree)

        self.rank = rank
        self.shape = randint(1, 3)
    
    def update(self):
        self.location.setX(int(self.location.x() + self.speed * math.sin(math.pi / 180 * self.degree)))
        self.location.setY(int(self.location.y() - self.speed * math.cos(math.pi / 180 * self.degree)))

        self.location.setX((self.location.x() + config.WINDOW_WIDTH) % config.WINDOW_WIDTH)
        self.location.setY((self.location.y() + config.WINDOW_HEIGHT) % config.WINDOW_HEIGHT)

    def draw(self, painter: QPainter):
        painter.setPen(QColor(Qt.white))
        painter.translate(self.location.x(), self.location.y())

        width = self.size.width()
        height = self.size.height()

        painter.drawPolygon({
            1: [
                QPointF(width * 0.5, 0), QPointF(width * 0.75, height * 0.1),
                QPointF(width * 0.6, height * 0.55), QPointF(width * 0.9, height * 0.8),
                QPointF(width * 0.9, height * 0.8), QPointF(width * 0.55, height * 0.7),
                QPointF(width * 0.4, height * 0.85), QPointF(width * 0.25, height * 0.6),
                QPointF(width * 0.08, height * 0.75), QPointF(width * 0.125, height * 0.5),
                QPointF(width * 0.04, height * 0.4), QPointF(width * 0.15, height * 0.15)],
            2: [
                QPointF(width * 0.25, 0), QPointF(width * 0.85, height * 0.15),
                QPointF(width * 0.9, height * 0.9), QPointF(width * 0.55, height),
                QPointF(width * 0.35, height * 0.8), QPointF(width * 0.15, height * 0.88),
                QPointF(width * 0.2, height * 0.6), QPointF(0, height * 0.25),
                QPointF(width * 0.3, height * 0.45)],
            3: [
                QPointF(width, height), QPointF(width * 0.15, height * 0.95),
                QPointF(width * 0.075, height * 0.6), QPointF(width * 0.25, height * 0.45),
                QPointF(width * 0.2, height * 0.15), QPointF(width * 0.5, height * 0.03),
                QPointF(width * 0.45, height * 0.35), QPointF(width * 0.75, height * 0.2),
                QPointF(width * 0.9, height * 0.48), QPointF(width, height * 0.55),
                QPointF(width * 0.8, height * 0.8)]
        }[self.shape])

        painter.translate(-self.location.x(), -self.location.y())

    def isCollide(self, other):
        return (self.location.x() < other.location.x() + other.size.width() and
                self.location.x() + self.size.width() > other.location.x() and
                self.location.y() < other.location.y() + other.size.height() and
                self.location.y() + self.size.height() > other.location.y())

    def __repr__(self):
        return f"({self.rank}, {self.speed.__round__(2)}, {self.degree})"