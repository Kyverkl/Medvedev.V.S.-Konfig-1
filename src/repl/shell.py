import getpass
import socket
from collections.abc import Callable

from repl.commands import CommandError, all_commands
from repl.parser import parse
from repl.vfs import VFS, VFSError


class Shell:
    def __init__(self, output: Callable[[str], None] = print):
        self.output = output
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.vfs = VFS.default()
        self.cwd = "/"
        self.commands = all_commands()
        self.exited = False

    def prompt(self) -> str:
        return f"{self.user}@{self.host}:{self.cwd}$ "

    def load_vfs(self, path: str) -> None:
        try:
            self.vfs = VFS.load(path)
        except VFSError as e:
            self.output(f"Ошибка загрузки VFS: {e}. Используется VFS по умолчанию")
            return
        self.cwd = "/"
        files, dirs = self.vfs.stats()
        self.output(f"VFS загружена из {path}: файлов {files}, каталогов {dirs}")

    def execute(self, line: str) -> bool:
        """Выполняет строку, возвращает False при ошибке."""
        tokens = parse(line)
        if not tokens:
            return True
        name, args = tokens[0], tokens[1:]
        try:
            command = self.commands.get(name)
            if command is None:
                raise CommandError(f"{name}: команда не найдена")
            result = command.run(self, args)
        except CommandError as e:
            self.output(str(e))
            return False
        if result:
            self.output(result.rstrip("\n"))
        return True

    def run_script(self, path: str) -> None:
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except OSError as e:
            self.output(f"Ошибка: не удалось открыть скрипт {path}: {e.strerror}")
            return
        for number, raw in enumerate(lines, 1):
            # Комментарии в стиле Python: всё после '#'
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            self.output(self.prompt() + line)
            if not self.execute(line):
                self.output(f"Ошибка в скрипте {path}, строка {number}")
            if self.exited:
                break
