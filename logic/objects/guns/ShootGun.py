from random import randrange

from game.logic.objects.entities.Bullet import Bullet
from game.logic.objects.guns.Gun import Gun


class ShootGun(Gun):
    def __init__(self, x, y, sprite_dir="sprites/animated_sprites/guns/shoot_gun/"):
        all_sprites = {
            "idle_r": sprite_dir + "shoot_guns_r.png",
            "idle_l": sprite_dir + "shoot_guns_l.png",
        }
        super().__init__(x, y, all_sprites, frame_multiplier=10)
        # self.resize_sprites(1.3)
        self.shift = (30, 55, -2, 55)

    def __repr__(self):
        return f"Дробовик: x={self.x}, y={self.y}"

    def fire(self):
        bullet_characteristics = (
            self.bullet_speed, 300, self.bullet_freq
        )
        self.bullets.append(
            Bullet(
                self.x - self.shift[0], self.y - self.shift[1],
                self.mouse_pos, bullet_characteristics, resize_count=2.5
            )
        )
        for i in range(6):
            bullet_characteristics = (
                self.bullet_speed + i, 700, self.bullet_freq
            )
            mouse_pos = (
                randrange(self.mouse_pos[0] - 100, self.mouse_pos[0] + 100),
                randrange(self.mouse_pos[1] - 100, self.mouse_pos[1] + 100)
            )
            self.bullets.append(
                Bullet(
                    self.x - self.shift[0], self.y - self.shift[1],
                    mouse_pos, bullet_characteristics
                )
            )
