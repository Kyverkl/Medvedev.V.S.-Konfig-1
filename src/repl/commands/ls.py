from repl.commands.base import Command


class Ls(Command):
    name = "ls"
    usage = "ls [путь...]"
    description = "список файлов каталога"

    def run(self, shell, args: list[str]) -> str:
        return f"ls {args}"
