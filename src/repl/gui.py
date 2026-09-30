from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from repl.shell import Shell


class MainWindow(QMainWindow):
    def __init__(self, shell: Shell):
        super().__init__()
        self.shell = shell
        shell.output = self.write
        self.setWindowTitle(f"Эмулятор - [{shell.user}@{shell.host}]")
        self.resize(900, 600)

        font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        self.log = QPlainTextEdit(readOnly=True)
        self.log.setFont(font)
        self.prompt = QLabel()
        self.prompt.setFont(font)
        self.input = QLineEdit()
        self.input.setFont(font)
        self.input.returnPressed.connect(self.on_enter)

        line = QHBoxLayout()
        line.addWidget(self.prompt)
        line.addWidget(self.input)
        layout = QVBoxLayout()
        layout.addWidget(self.log)
        layout.addLayout(line)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.refresh()
        self.input.setFocus()

    def write(self, text: str) -> None:
        self.log.appendPlainText(text)

    def on_enter(self) -> None:
        line = self.input.text()
        self.input.clear()
        self.write(self.shell.prompt() + line)
        self.shell.execute(line)
        self.refresh()

    def run_script(self, path: str) -> None:
        self.shell.run_script(path)
        self.refresh()

    def refresh(self) -> None:
        self.prompt.setText(self.shell.prompt())
        if self.shell.exited:
            self.close()
