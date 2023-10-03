from PyQt5.QtCore import QRect


class Camera:
    def __init__(self, x, y, max_map_coordinates, max_x=1920, max_y=1080):
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y
        self.max_map_coordinates = max_map_coordinates
        self.rect = QRect(self.x, self.y, 200, 200)

        self.block_x = False
        self.block_y = False

        self.hero_positions = []

    def get_top_left_corner(self):
        return self.x - self.max_x // 2, self.y - self.max_y // 2

    def can_go_x(self, value):
        return self.max_x // 2 < value < self.max_map_coordinates[0] - self.max_x // 2

    def can_go_y(self, value):
        return self.max_y // 2 < value < self.max_map_coordinates[1] - self.max_y // 2

    def update(self):
        if len(self.hero_positions) > 15:
            if self.can_go_x(self.hero_positions[0][0] + 64):
                self.x = self.hero_positions[0][0] + 64
            if self.can_go_y(self.hero_positions[0][1] + 64):
                self.y = self.hero_positions[0][1] + 64

            self.rect = QRect(self.x, self.y, 200, 200)
            self.hero_positions.remove(self.hero_positions[0])
