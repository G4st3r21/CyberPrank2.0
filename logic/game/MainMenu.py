import os
import random

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPainter, QPixmap, QImage, QTransform, QFont, QColor, QMovie
from PyQt5.QtMultimedia import QMediaContent


class MainMenu:
    def __init__(self):
        self.floating_heroes: list[FloatingHero] = []
        self.buttons = []
        self.background = QImage()
        self.logo = QImage("sprites/main_menu/logo/logo_for_menu.png")
        logo_size_transform = QTransform().scale(0.6, 0.6)
        self.logo = self.logo.transformed(logo_size_transform)

        self.painter = None
        self.pixmap = QPixmap(1920, 1080)
        self.window_size = (1920, 1080)

        self.choose_background()
        self.init_buttons()
        self.init_floating_heroes()

    def choose_background(self):
        background_number = random.randrange(0, 3)
        self.background = QImage(f"sprites/main_menu/backgrounds/{background_number}.jpg")

    def get_dead_animation(self):
        path = "sprites/dead_frames/"
        frames = []
        for filename in os.listdir(path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                pixmap = QPixmap(os.path.join(path, filename))
                image = pixmap.toImage()
                image = image.scaled(1920, 1080)
                for _ in range(8):
                    frames.append(image)
        return frames

    def init_floating_heroes(self):
        heroes = [
            QPixmap("sprites/main_menu/floating_heroes/blue.png"),
            QPixmap("sprites/main_menu/floating_heroes/turquoise.png"),
            QPixmap("sprites/main_menu/floating_heroes/zombie.png")
        ]
        for hero in heroes:
            for _ in range(4):
                rotate_direction = random.choice([-1, 1])
                dir_x, dir_y = random.choice([-1, 1]), random.choice([-1, 1])
                x, y = random.randrange(0, 1920), random.randrange(0, 1080)
                self.floating_heroes.append(FloatingHero(hero, x, y, dir_x, dir_y, rotate_direction))

    def init_buttons(self):
        self.buttons.append(Button(self.pixmap.width() // 2, self.pixmap.height() // 2, "играть"))

    def update(self, mouse_pos):
        for hero in self.floating_heroes:
            hero.update()
        for button in self.buttons:
            button.mouse_pos = mouse_pos
            button.update()

    def paint_main_menu(self, mouse_pos):
        self.update(mouse_pos)
        self.painter = QPainter(self.pixmap)
        font = QFont()
        font.setPointSize(40)
        font.setWeight(QFont.Bold)
        self.painter.setFont(font)
        self.painter.setPen(QColor(Qt.white))

        self.painter.drawImage(0, 0, self.background)
        for hero in self.floating_heroes:
            self.painter.drawPixmap(hero.x, hero.y, hero.pixmap)

        for button in self.buttons:
            self.painter.drawImage(button.x, button.y, button.button_image)
            text_pos = button.x + button.image.width() // 4, button.y + button.image.height() // 2 + 10
            self.painter.drawText(*text_pos, button.text)

        self.painter.drawImage(self.window_size[0] // 4, self.window_size[1] // 64, self.logo)
        self.painter.end()
        return self.pixmap


class FloatingHero:
    def __init__(self, pixmap: QPixmap, x, y, dir_x, dir_y, rotate_dir):
        self.x, self.y = x, y
        self.bias_x = 0
        self.bias_y = 0
        self.dir_x, self.dir_y = dir_x, dir_y
        self.rotate_dir = rotate_dir
        self.angle = rotate_dir

        self.pixmap: QPixmap = pixmap

    def update(self):
        if self.x > 1920:
            self.x = -200
        if self.x < -200:
            self.x = 1920
        if self.y > 1080:
            self.y = -200
        if self.y < -200:
            self.y = 1080

        self.x += self.dir_x
        self.y += self.dir_y


class Button:
    def __init__(self, x, y, text):
        self.text = text

        transform = QTransform().scale(0.7, 0.7)
        self.image = QImage(f"sprites/main_menu/buttons/button1.2.png")
        self.image_hover = QImage(f"sprites/main_menu/buttons/button1.1.png")
        self.image = self.image.transformed(transform)
        self.image_hover = self.image_hover.transformed(transform)
        self.button_image = self.image
        self.mouse_pos = None

        self.x, self.y = x - self.button_image.width() // 2, y - self.button_image.height() // 2

    def is_mouse_on_button(self):
        min_coords = self.x, self.y
        max_coords = self.x + self.image.width(), self.y + self.image.height()

        return self.mouse_pos and \
            max_coords[0] > self.mouse_pos.x() > min_coords[0] and \
            max_coords[1] > self.mouse_pos.y() - 35 > min_coords[1]

    def update(self):
        if self.is_mouse_on_button():
            self.button_image = self.image_hover
        else:
            self.button_image = self.image
