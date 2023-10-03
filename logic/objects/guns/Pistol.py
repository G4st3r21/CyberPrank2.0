from game.logic.objects.guns.Gun import Gun


class Pistol(Gun):
    def __init__(self, x, y, sprite_dir="sprites/animated_sprites/guns/pistol/"):
        all_sprites = {
            "idle_r": sprite_dir + "pistol_r.png",
            "idle_l": sprite_dir + "pistol_l.png",
        }
        super().__init__(x, y, all_sprites, frame_multiplier=7)
        self.resize_sprites(1.3)
        self.shift = (30, 20, 2, 20)

    def __repr__(self):
        return f"Пистолет: x={self.x}, y={self.y}"
