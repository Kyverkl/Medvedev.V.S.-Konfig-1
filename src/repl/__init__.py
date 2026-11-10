def main() -> None:
    """Точка входа: GUI, параметры запуска, VFS и стартовый скрипт."""
    import sys
    from dataclasses import asdict

    from PyQt6.QtCore import QTimer
    from PyQt6.QtWidgets import QApplication

    from repl.config import parse_args
    from repl.gui import MainWindow
    from repl.shell import Shell

    config = parse_args()
    app = QApplication(sys.argv[:1])
    shell = Shell()
    window = MainWindow(shell)
    window.show()

    for key, value in asdict(config).items():
        shell.output(f"[debug] {key} = {value}")

    if config.vfs:
        shell.load_vfs(config.vfs)
    if config.script:
        path = config.script
        QTimer.singleShot(0, lambda: window.run_script(path))
    sys.exit(app.exec())
