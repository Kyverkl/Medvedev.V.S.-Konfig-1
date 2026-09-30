from repl.commands.base import Command, CommandError


class Cd(Command):
    name = "cd"
    usage = "cd [путь]"
    description = "смена текущего каталога"

    def run(self, shell, args: list[str]) -> str:
        if len(args) > 1:
            raise CommandError("cd: слишком много аргументов")
        return f"cd {args}"
