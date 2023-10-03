from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QKeyEvent, QCursor, QPainter
from PyQt5.QtCore import Qt, QTimer

from game.logic.game.MainGame import MainGame
from game.logic.game.MainMenu import MainMenu
from game.logic.gui.KeyThread import KeyThread


class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dead_frames = []
        self.game = MainGame()
        self.menu = MainMenu()
        self.cursor = QCursor()
        self.mediaPlayer = QMediaPlayer(self)
        self.state = 0

        self.pressed_keys = set()
        self.key_thread = KeyThread(self)
        self.key_thread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_update)
        self.timer.start(13)

        self.initUI()

    def change_state(self):
        self.state = 0 if self.state else 1

    def timer_update(self):
        if self.state:
            self.game.update(self.get_cursor_global_pos())
            if self.game.hero.hp <= 0:
                self.change_state()
                self.dead_frames = self.menu.get_dead_animation()
                self.dead_frames.reverse()
                self.game = MainGame()
            self.game.check_collisions()
            self.game.collect_garbage()

        self.repaint()

    def initUI(self):
        self.setWindowTitle("White Background")
        self.setGeometry(0, 0, 1920, 1080)
        self.show()

    def change_cursor(self, fire=False):
        if not fire:
            pixmap = QPixmap('sprites/arrows/Arrow1.png')
        else:
            pixmap = QPixmap('sprites/arrows/Arrow1.1.png')
        pixmap = pixmap.scaled(pixmap.width() // 3, pixmap.height() // 3)

        cursor = QCursor(pixmap)
        self.setCursor(cursor)

    def paintEvent(self, event):
        if self.state:
            self.game.paint_game(self)
        elif self.dead_frames:
            painter = QPainter(self)
            frame = self.dead_frames.pop()
            painter.drawImage(0, 0, frame)
        else:
            painter = QPainter(self)
            pixmap = self.menu.paint_main_menu(self.cursor.pos())
            painter.drawPixmap(0, 0, pixmap)

    def get_cursor_global_pos(self):
        global_pos = self.cursor.pos()
        widget_pos = self.mapFromGlobal(global_pos)
        camera_pos = self.game.camera.get_top_left_corner()

        return widget_pos.x() + camera_pos[0], widget_pos.y() + camera_pos[1]

    def mousePressEvent(self, event):
        if self.state:
            self.game.hero.current_gun.animate = True
            self.change_cursor(fire=True)
        else:
            for button in self.menu.buttons:
                if button.is_mouse_on_button():
                    self.change_state()

    def mouseReleaseEvent(self, event):
        self.game.hero.current_gun.animate = False
        self.game.hero.current_gun.current_frame = 0
        self.change_cursor(fire=False)

    def keyPressEvent(self, event):
        self.pressed_keys.add(event.key())
        print(event.key())

    def keyReleaseEvent(self, event: QKeyEvent):
        key = event.key()
        if key in [Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D] and not event.isAutoRepeat():
            self.game.hero.set_idle()
        self.pressed_keys.remove(event.key())
