from repl.commands.base import Command, CommandError, get_file


class Cat(Command):
    name = "cat"
    usage = "cat файл..."
    description = "вывод содержимого файлов"

    def run(self, shell, args: list[str]) -> str:
        if not args:
            raise CommandError("cat: не указан файл")
        return "".join(get_file(shell, "cat", path).content.decode("utf-8", errors="replace") for path in args)
