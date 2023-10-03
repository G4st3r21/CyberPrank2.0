from PyQt5.QtCore import QThread, pyqtSignal, Qt


class KeyThread(QThread):
    key_signal = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        while True:
            if self.is_key_down(Qt.Key_W) and self.is_key_down(Qt.Key_D):
                self.parent.game.hero.run_forward_right()
            elif self.is_key_down(Qt.Key_W) and self.is_key_down(Qt.Key_A):
                self.parent.game.hero.run_forward_left()
            elif self.is_key_down(Qt.Key_S) and self.is_key_down(Qt.Key_D):
                self.parent.game.hero.run_down_right()
            elif self.is_key_down(Qt.Key_S) and self.is_key_down(Qt.Key_A):
                self.parent.game.hero.run_down_left()
            elif self.is_key_down(Qt.Key_W):
                self.parent.game.hero.run_forward()
            elif self.is_key_down(Qt.Key_A):
                self.parent.game.hero.run_left()
            elif self.is_key_down(Qt.Key_S):
                self.parent.game.hero.run_down()
            elif self.is_key_down(Qt.Key_D):
                self.parent.game.hero.run_right()
            if self.is_key_down(Qt.Key_1):
                self.parent.game.hero.change_current_gun(0)
            elif self.is_key_down(Qt.Key_2):
                self.parent.game.hero.change_current_gun(1)
            elif self.is_key_down(Qt.Key_3):
                self.parent.game.hero.change_current_gun(2)
            self.msleep(10)

    def is_key_down(self, key):
        return int(key) in self.parent.pressed_keys
