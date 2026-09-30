import getpass
import socket
from collections.abc import Callable

from repl.commands import CommandError, all_commands
from repl.parser import parse


class Shell:
    def __init__(self, output: Callable[[str], None] = print):
        self.output = output
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.cwd = "/"
        self.commands = all_commands()
        self.exited = False

    def prompt(self) -> str:
        return f"{self.user}@{self.host}:{self.cwd}$ "

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
