import sys
from dataclasses import asdict

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from repl.config import parse_args
from repl.gui import MainWindow
from repl.shell import Shell


def main() -> None:
    config = parse_args()
    app = QApplication(sys.argv[:1])
    shell = Shell()
    window = MainWindow(shell)
    window.show()

    # Отладочный вывод параметров запуска
    for key, value in asdict(config).items():
        shell.output(f"[debug] {key} = {value}")

    if config.script:
        # Запуск после старта цикла событий, чтобы exit в скрипте закрывал окно
        QTimer.singleShot(0, lambda: window.run_script(config.script))
    sys.exit(app.exec())
