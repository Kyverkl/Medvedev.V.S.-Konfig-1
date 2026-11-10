from repl.commands.base import Command, CommandError
from repl.vfs import Dir, File, Node, mode_string

DIR_SIZE = 4096


class Ls(Command):
    name = "ls"
    usage = "ls [-l] [путь...]"
    description = "содержимое каталогов; -l — подробный формат"

    def run(self, shell, args: list[str]) -> str:
        long, paths = self._parse_args(args)
        paths = paths or ["."]
        blocks = [
            self._format_path(shell, path, long, paths)
            for path in paths
        ]
        return "\n\n".join(blocks)

    def _parse_args(self, args: list[str]) -> tuple[bool, list[str]]:
        long = False
        paths = []
        for arg in args:
            if arg == "-l":
                long = True
            elif arg.startswith("-"):
                raise CommandError(f"ls: неверный ключ: {arg}")
            else:
                paths.append(arg)
        return long, paths

    def _format_path(
        self, shell, path: str, long: bool, paths: list[str]
    ) -> str:
        node = shell.lookup(path)
        if node is None:
            raise CommandError(
                f"ls: {path}: нет такого файла или каталога"
            )
        items = self._list_items(node, path)
        if long:
            text = "\n".join(
                self.long_line(n, name) for n, name in items
            )
        else:
            text = "  ".join(name for _, name in items)
        if len(paths) > 1:
            text = f"{path}:\n{text}"
        return text

    @staticmethod
    def _list_items(node: Node, path: str) -> list[tuple[Node, str]]:
        if isinstance(node, Dir):
            children = sorted(
                node.children.values(), key=lambda n: n.name
            )
            return [(child, child.name) for child in children]
        return [(node, path)]

    @staticmethod
    def long_line(node: Node, name: str) -> str:
        if isinstance(node, File):
            size = len(node.content)
        else:
            size = DIR_SIZE
        return f"{mode_string(node)} {size:>6} {name}"
