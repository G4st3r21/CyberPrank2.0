from game.logic.objects.guns.Gun import Gun


class AssaultRifle(Gun):
    def __init__(self, x, y, sprite_dir="sprites/animated_sprites/guns/assault_rifle/"):
        all_sprites = {
            "idle_r": sprite_dir + "assault_rifle_r.png",
            "idle_l": sprite_dir + "assault_rifle_l.png",
        }
        super().__init__(x, y, all_sprites, frame_multiplier=2)
        # self.resize_sprites(1.3)
        self.shift = (30, 50, 7, 50)

    def __repr__(self):
        return f"Штурмовая винтовка: x={self.x}, y={self.y}"
