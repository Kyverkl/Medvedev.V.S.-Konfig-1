from repl.commands.base import Command, CommandError


class Help(Command):
    name = "help"
    usage = "help [команда]"
    description = "список команд или справка по одной команде"

    def run(self, shell, args: list[str]) -> str:
        if len(args) > 1:
            raise CommandError("help: слишком много аргументов")
        if args:
            command = shell.commands.get(args[0])
            if command is None:
                raise CommandError(f"help: нет такой команды: {args[0]}")
            commands = [command]
        else:
            commands = list(shell.commands.values())
        width = max(len(c.usage) for c in commands)
        return "\n".join(f"{c.usage:<{width}}  {c.description}" for c in commands)
