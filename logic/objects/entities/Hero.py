from PyQt5.QtCore import QRect

from game.logic.objects.guns.AssaultRifle import AssaultRifle
from game.logic.game.Controllable import Controllable
from game.logic.objects.guns.Gun import Gun
from game.logic.objects.guns.Pistol import Pistol
from game.logic.objects.guns.ShootGun import ShootGun


class Hero(Controllable):
    def __init__(self, x=100, y=100, sprite_dir="sprites/animated_sprites/main_hero/blue/"):
        all_sprites = {
            "idle_r": sprite_dir + "hero_stand_r.png",
            "idle_l": sprite_dir + "hero_stand_l.png",
            "idle_g_r": sprite_dir + "with_gun/" + "hero_stand_r.png",
            "idle_g_l": sprite_dir + "with_gun/" + "hero_stand_l.png",

            "run_r": sprite_dir + "hero_run_r.png",
            "run_l": sprite_dir + "hero_run_l.png",
            "run_g_r": sprite_dir + "with_gun/" + "hero_run_r.png",
            "run_g_l": sprite_dir + "with_gun/" + "hero_run_l.png",
        }
        super().__init__(x, y, all_sprites)
        self.sprite_init()

        self.hp = 100
        self.step = 5
        self.angle_step = 4
        self.inventory: list[Gun] = []
        self.current_gun: [Gun, None] = None

        self.mouse_pos = ()
        self.x, self.y = x, y

        self.rect = QRect(self.x + 35, self.y, 64, 128)

        # TEST
        self.append_gun(Pistol(self.x, self.y))
        self.append_gun(AssaultRifle(self.x, self.y))
        self.append_gun(ShootGun(self.x, self.y))
        self.change_current_gun(0)

    def append_gun(self, gun: Gun):
        if gun not in self.inventory:
            self.inventory.append(gun)
            self.current_gun = gun
        else:
            self.current_gun = self.inventory[self.inventory.index(gun)]

    def change_current_gun(self, index):
        self.current_gun = self.inventory[index]
        for gun in self.inventory:
            gun.active = False
        self.current_gun.active = True

    def set_mouse_pos(self, x, y):
        self.mouse_pos = (x, y)

    def update(self):
        self.change_direction("l" if self.x + 67 > self.mouse_pos[0] else "r")
        self.current_gun.change_direction("l" if self.x > self.mouse_pos[0] else "r")
        super().update()
        self.rect = QRect(self.x + 35, self.y, 64, 128)

    def __repr__(self):
        return f"Герой: {self.x}, {self.y}"
