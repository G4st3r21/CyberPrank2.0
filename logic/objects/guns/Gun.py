from game.logic.graphics.AnimatedSprite import AnimatedSprite
from game.logic.objects.entities.Bullet import Bullet


class Gun(AnimatedSprite):
    def __init__(self, x, y, all_sprites, frame_multiplier=7):
        super().__init__(all_sprites)
        self.sprite_init(frame_multiplier=frame_multiplier)
        self.frame_multiplier = frame_multiplier
        self.x, self.y = x, y
        self.mouse_pos = None
        self.animate = False
        self.shift = (0, 0, 0, 0)

        self.bullets_per_shoot = 0
        self.ammo = 30
        self.bullet_speed = 20
        self.bullet_freq = 1
        self.bullets: list[Bullet] = []

    def change_coordinate(self, x, y, frame_type):
        self.change_current_frame_type("idle_" + frame_type)
        if frame_type == "r":
            self.x, self.y = x + self.shift[0], y + self.shift[1]
        else:
            self.x, self.y = x + self.shift[2], y + self.shift[3]

    def update(self):
        if self.current_frame == 8 * self.frame_multiplier - 1 and self.active:
            self.fire()
        if not self.active:
            self.current_frame = 0
        super().update()

    def fire(self):
        bullet_characteristics = (
            self.bullet_speed, 1200, self.bullet_freq
        )
        self.bullets.append(
            Bullet(self.x - self.shift[0], self.y - self.shift[1], self.mouse_pos, bullet_characteristics))
