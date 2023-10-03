import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication

from game.logic.game.MainMenu import MainMenu


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu = MainMenu()
        self.setWindowTitle("CyberPrank")
        self.setGeometry(0, 0, 1920, 1080)
        self.cursor = QCursor()

        self.repaint_timer = QTimer()
        self.repaint_timer.timeout.connect(self.repaint)
        self.repaint_timer.start(13)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = self.menu.paint_main_menu(self.cursor.pos())
        painter.drawPixmap(0, 0, pixmap)

    def mousePressEvent(self, event):
        for button in self.menu.buttons:
            if button.is_mouse_on_button():
                print("Button clicked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Menu()
    sys.exit(app.exec_())
