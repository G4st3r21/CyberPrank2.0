from math import cos, sin, atan, atan2, degrees

from PyQt5.QtCore import QRect

from game.logic.graphics.Sprite import Sprite


class Bullet(Sprite):
    def __init__(self, x, y, mouse_position, bullet_characteristics, sprite_dir="sprites/fire/", resize_count=1.7):
        all_sprites = [
            sprite_dir + "red_bullet.png"
        ]
        super().__init__(all_sprites)
        self.resize_sprites(resize_count)
        self.x = x + 20
        self.y = y + 40
        self.mouse_pos = mouse_position
        self.speed = bullet_characteristics[0]
        self.freq = bullet_characteristics[-1]
        self.rect = QRect(self.x + 12, self.y + 12, 13, 13)

        self.max_distance = bullet_characteristics[1]
        self.distance = 0
        self.speed_x = 0
        self.speed_y = 0
        self.calculate_speeds()

    def calculate_speeds(self):
        dx = self.mouse_pos[0] - self.x
        dy = self.mouse_pos[1] - self.y
        angle_rad = atan2(dy, dx)
        angle_deg = degrees(angle_rad)

        if self.mouse_pos[0] < self.x:
            angle_deg += 180

        self.speed_x = int(self.speed * cos(angle_rad))
        self.speed_y = int(self.speed * sin(angle_rad))

        if not (int(angle_deg) in range(-20, 21) or int(angle_deg) in range(340, 361)):
            self.deactivate()
        self.update()

    def update(self):
        if self.active:
            self.x += self.speed_x
            self.y += self.speed_y
            self.distance += abs(self.speed_x) + abs(self.speed_y)
            if self.distance > self.max_distance:
                self.deactivate()
            self.rect = QRect(self.x + 12, self.y + 12, 13, 13)

    def deactivate(self):
        self.rect = QRect(-99999, -99999, 1, 1)
        self.active = False
