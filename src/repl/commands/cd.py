from repl.commands.base import Command, CommandError
from repl.vfs import Dir


class Cd(Command):
    name = "cd"
    usage = "cd [путь]"
    description = "смена текущего каталога; без аргумента — переход в корень"

    def run(self, shell, args: list[str]) -> str:
        if len(args) > 1:
            raise CommandError("cd: слишком много аргументов")
        path = args[0] if args else "/"
        node = shell.lookup(path)
        if node is None:
            raise CommandError(f"cd: {path}: нет такого каталога")
        if not isinstance(node, Dir):
            raise CommandError(f"cd: {path}: не является каталогом")
        shell.cwd = shell.abspath(path)
        return ""
