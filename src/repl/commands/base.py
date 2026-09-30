from repl.vfs import Dir, File


class CommandError(Exception):
    pass


class Command:
    name = ""
    usage = ""
    description = ""

    def run(self, shell, args: list[str]) -> str:
        raise NotImplementedError


def get_file(shell, command: str, path: str) -> File:
    node = shell.lookup(path)
    if node is None:
        raise CommandError(f"{command}: {path}: нет такого файла или каталога")
    if isinstance(node, Dir):
        raise CommandError(f"{command}: {path}: это каталог")
    return node
