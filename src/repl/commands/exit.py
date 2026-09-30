from repl.commands.base import Command, CommandError


class Exit(Command):
    name = "exit"
    usage = "exit"
    description = "выход из эмулятора"

    def run(self, shell, args: list[str]) -> str:
        if args:
            raise CommandError("exit: команда не принимает аргументов")
        shell.exited = True
        return ""
