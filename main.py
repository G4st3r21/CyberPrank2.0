import sys

from PyQt5.QtWidgets import QApplication

from game.logic.gui.MainGUI import MainGUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainGUI()
    sys.exit(app.exec_())
