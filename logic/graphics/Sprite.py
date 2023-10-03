from PIL import Image


class Sprite:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.current_frames = [Image.open(sprite) for sprite in self.all_sprites]
        self.current_frame = 0
        self.active = True

    def resize_sprites(self, x):
        for index, frame in enumerate(self.current_frames):
            width, height = frame.size
            self.current_frames[index] = frame.resize((int(width / x), int(height / x)))
