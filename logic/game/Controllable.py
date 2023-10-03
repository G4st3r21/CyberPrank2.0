from game.logic.graphics.AnimatedSprite import AnimatedSprite


class Controllable(AnimatedSprite):
    def __init__(self, x, y, all_sprites):
        super().__init__(all_sprites)
        self.hp = 0
        self.x, self.y = x, y
        self.step = 3
        self.angle_step = 2

    def set_idle(self):
        self.change_current_frame_type(
            "idle_r"
            if self.current_frame_type in ["run_r", "idle_r"]
            else "idle_l"
        )

    def run_right(self):
        self.x += self.step
        self.change_current_frame_type("run_r")

    def run_left(self):
        self.x -= self.step
        self.change_current_frame_type("run_l")

    def run_forward(self):
        self.y -= self.step
        self.change_current_frame_type("run_r" if self.current_frame_type[-1] == "r" else "run_l")

    def run_down(self):
        self.y += self.step
        self.change_current_frame_type("run_r" if self.current_frame_type[-1] == "r" else "run_l")

    def run_forward_right(self):
        self.x += self.angle_step
        self.y -= self.angle_step
        self.change_current_frame_type("run_r")

    def run_forward_left(self):
        self.x -= self.angle_step
        self.y -= self.angle_step
        self.change_current_frame_type("run_l")

    def run_down_right(self):
        self.x += self.angle_step
        self.y += self.angle_step
        self.change_current_frame_type("run_r")

    def run_down_left(self):
        self.x -= self.angle_step
        self.y += self.angle_step
        self.change_current_frame_type("run_l")
