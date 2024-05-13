import config

import math

from PyQt5.QtGui import *
from PyQt5.QtCore import *

from abc import ABC, abstractmethod


class GameObject(ABC):
    def __init__(self, location: QPointF, size: QSize, speed: float = 0, degree: int = 0):
        self.location = location
        self.size = size

        self.speed = speed
        self.degree = degree

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self, painter: QPainter) -> None:
        pass

    @abstractmethod
    def isCollide(self, other) -> bool:
        pass