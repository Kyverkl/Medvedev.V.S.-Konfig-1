from repl.commands.base import Command, CommandError
from repl.vfs import Dir, File, Node, mode_string


class Ls(Command):
    name = "ls"
    usage = "ls [-l] [путь...]"
    description = "содержимое каталогов; -l — подробный формат"

    def run(self, shell, args: list[str]) -> str:
        long = False
        paths = []
        for arg in args:
            if arg == "-l":
                long = True
            elif arg.startswith("-"):
                raise CommandError(f"ls: неверный ключ: {arg}")
            else:
                paths.append(arg)
        paths = paths or ["."]

        blocks = []
        for path in paths:
            node = shell.lookup(path)
            if node is None:
                raise CommandError(f"ls: {path}: нет такого файла или каталога")
            if isinstance(node, Dir):
                items = [(child, child.name) for child in sorted(node.children.values(), key=lambda n: n.name)]
            else:
                items = [(node, path)]
            if long:
                text = "\n".join(self.long_line(n, name) for n, name in items)
            else:
                text = "  ".join(name for _, name in items)
            if len(paths) > 1:
                text = f"{path}:\n{text}"
            blocks.append(text)
        return "\n\n".join(blocks)

    @staticmethod
    def long_line(node: Node, name: str) -> str:
        size = len(node.content) if isinstance(node, File) else 4096
        return f"{mode_string(node)} {size:>6} {name}"
