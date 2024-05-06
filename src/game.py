import math

import config

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from game_objects.spaceship import Spaceship
from game_objects.asteroid import Asteroid
from game_objects.bullet import Bullet


class Game:
    def __init__(self):
        self.__spaceship = Spaceship()
        self.__asteroids = [Asteroid() for _ in range(4)]
        self.__bullets = []

        self.__score = 0
        self.__lives = 3

    def update(self):
        self.__spaceship.update()

        asteroids_to_destroy = set()
        for asteroid in self.__asteroids:
            asteroid.update()

            if not self.__spaceship.isCollide(asteroid):
                continue

            self.__lives -= 1
            if self.__lives == 0:
                return self.restart()
            self.__spaceship.reset()
            asteroids_to_destroy.add(asteroid)

        bullets_to_remove = set()
        for bullet in self.__bullets:
            bullet.update()
            if bullet.isOutOfView():
                bullets_to_remove.add(bullet)

            for asteroid in self.__asteroids:
                if bullet.isCollide(asteroid):
                    bullets_to_remove.add(bullet)
                    asteroids_to_destroy.add(asteroid)

        for asteroid in asteroids_to_destroy:
            self.destroyAsteroid(asteroid)
        for bullet in bullets_to_remove:
            self.__bullets.remove(bullet)

    def destroyAsteroid(self, asteroid: Asteroid):
        self.__asteroids.remove(asteroid)
        self.__score += {1: 100, 2: 50, 3: 20}[asteroid.rank]
        if asteroid.rank > 1:
            self.__asteroids.append(Asteroid(asteroid.rank - 1, QPoint(asteroid.location)))
            self.__asteroids.append(Asteroid(asteroid.rank - 1, QPoint(asteroid.location)))

    def draw(self, painter: QPainter):
        painter.fillRect(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT, QBrush(Qt.SolidPattern))
        self.__spaceship.draw(painter)
        for asteroid in self.__asteroids:
            asteroid.draw(painter)
        for bullet in self.__bullets:
            bullet.draw(painter)

        painter.setPen(QColor(Qt.white))
        painter.setFont(QFont('Courier New', 24))
        painter.drawText(10, 60, str(self.__score))
        painter.drawText(10, 100, "A" * self.__lives)

    def startBoosting(self):
        self.__spaceship.boosting = True

    def stopBoosting(self):
        self.__spaceship.boosting = False

    def startRotationToRight(self):
        self.__spaceship.rotation_to_right = True
        self.__spaceship.rotation_to_left = False

    def startRotationToLeft(self):
        self.__spaceship.rotation_to_right = False
        self.__spaceship.rotation_to_left = True

    def stopRotation(self):
        self.__spaceship.rotation_to_right = False
        self.__spaceship.rotation_to_left = False

    def shoot(self):
        new_bullet_x = self.__spaceship.location.x() + (1 + math.sin(math.pi / 180 * self.__spaceship.degree)) * (
                self.__spaceship.size.width() // 2)
        new_bullet_y = self.__spaceship.location.y() + (1 - math.cos(math.pi / 180 * self.__spaceship.degree)) * (
                self.__spaceship.size.height() // 2)
        self.__bullets.append(Bullet(QPoint(int(new_bullet_x), int(new_bullet_y)), self.__spaceship.degree))

    def restart(self):
        self.__init__()
