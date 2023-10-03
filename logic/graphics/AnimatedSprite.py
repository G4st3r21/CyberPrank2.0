from PIL import Image


class AnimatedSprite:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.all_frames: dict[str, list[Image]] = {"default": []}
        self.current_frame_type = "default"
        self.current_frames = self.all_frames[self.current_frame_type]
        self.current_frame = 0
        self.animate = True
        self.active = True

    def sprite_init(self, frame_multiplier=7):
        self.all_frames.clear()
        for sprite_type, sprite_name in self.all_sprites.items():
            self.cut_sheet(
                sprite_name,
                flip_v=sprite_type[-1] == "l",
                frame_type=sprite_type,
                frame_multiplier=frame_multiplier
            )
        self.change_current_frame_type("idle_r")

    def change_direction(self, direction):
        self.change_current_frame_type(self.current_frame_type[:-1] + direction)

    def change_current_frame_type(self, frame_type):
        self.current_frame_type = frame_type
        self.current_frames = self.all_frames[self.current_frame_type]

    def resize_sprites(self, x):
        for frame_type, frames in self.all_frames.items():
            for index, frame in enumerate(frames):
                width, height = frame.size
                self.all_frames[frame_type][index] = frame.resize((int(width / x), int(height / x)))

    def cut_sheet(self, sheet, flip_v, columns=8, frame_type="default", frame_multiplier=7):
        self.all_frames[frame_type] = []
        # Load image with Pillow
        image = Image.open(sheet)

        # Get image size
        width, height = image.size

        # Calculate the width and height of each slice
        slice_width = width // columns
        slice_height = height

        # Crop the image into 8 slices
        for i in range(8):
            x = (i % 8) * slice_width
            slice = image.crop((x, 0, x + slice_width, slice_height))
            for _ in range(frame_multiplier):
                self.all_frames[frame_type].append(slice)

        if flip_v:
            self.all_frames[frame_type].reverse()

    def update(self):
        if self.animate:
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)
