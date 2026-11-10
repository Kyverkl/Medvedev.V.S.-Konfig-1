from repl.commands.base import Command, CommandError
from repl.vfs import VFS


class VfsInit(Command):
    name = "vfs-init"
    usage = "vfs-init"
    description = (
        "заменить VFS на VFS по умолчанию "
        "и очистить её физическое представление"
    )

    def run(self, shell, args: list[str]) -> str:
        if args:
            raise CommandError(
                "vfs-init: команда не принимает аргументов"
            )
        source = shell.vfs.source
        try:
            shell.vfs.wipe_source()
        except OSError as e:
            raise CommandError(
                f"vfs-init: не удалось очистить "
                f"{source}: {e.strerror}"
            )
        shell.vfs = VFS.default(source)
        shell.cwd = "/"
        if source:
            where = f", каталог {source} очищен"
        else:
            where = ""
        return f"VFS заменена на VFS по умолчанию{where}"
