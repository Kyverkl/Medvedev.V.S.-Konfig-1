import sys

from PyQt6.QtWidgets import QApplication

from repl.gui import MainWindow
from repl.shell import Shell


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow(Shell())
    window.show()
    sys.exit(app.exec())
