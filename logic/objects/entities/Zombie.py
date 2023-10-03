from PyQt5.QtCore import QRect

from game.logic.game.Controllable import Controllable


class Zombie(Controllable):
    def __init__(self, x, y, wave, sprite_dir="sprites/animated_sprites/zombie/"):
        all_sprites = {
            "idle_r": sprite_dir + "zombie_stand_r.png",
            "idle_l": sprite_dir + "zombie_stand_l.png",

            "run_r": sprite_dir + "zombie_run_r.png",
            "run_l": sprite_dir + "zombie_run_l.png",
        }
        super().__init__(x, y, all_sprites)
        self.sprite_init()

        self.hp = 100 + wave * 2
        self.damage = 1 + wave / 2
        self.step = 2
        self.angle_step = 1
        self.hero_coords = None
        self.rect = QRect(self.x + 35, self.y, 64, 128)

    def update(self):
        if self.hp < 100:
            self.hp += 0.1
        else:
            self.hp = 100
        if self.hp < 0:
            self.hp = 0
            self.active = False
        self.run_to_hero()
        super().update()
        self.rect = QRect(self.x + 35, self.y, 64, 128)

    def run_to_hero(self):
        if self.hero_coords:
            coord_range = self.hero_coords[0] - self.x, self.hero_coords[1] - self.y

            need_l = coord_range[0] < 0
            need_r = coord_range[0] > 0
            need_w = coord_range[1] < 0
            need_d = coord_range[1] > 0

            match (need_l, need_r, need_w, need_d):
                case (False, True, True, False):
                    self.run_forward_right()
                case (True, False, True, False):
                    self.run_forward_left()
                case (False, True, False, True):
                    self.run_down_right()
                case (True, False, False, True):
                    self.run_down_left()
                case (False, False, True, False):
                    self.run_forward()
                case (False, False, False, True):
                    self.run_down()
                case (False, True, False, False):
                    self.run_right()
                case (True, False, False, False):
                    self.run_left()
                case _:
                    self.set_idle()

    def __repr__(self):
        return f"Зомби: {int(self.hp)} HP"
