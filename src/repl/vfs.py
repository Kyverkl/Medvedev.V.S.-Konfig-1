import shutil
from pathlib import Path


class VFSError(Exception):
    pass


class Node:
    def __init__(self, name: str, mode: int):
        self.name = name
        self.mode = mode


class File(Node):
    def __init__(self, name: str, mode: int, content: bytes):
        super().__init__(name, mode)
        self.content = content


class Dir(Node):
    def __init__(self, name: str, mode: int = 0o755):
        super().__init__(name, mode)
        self.children: dict[str, Node] = {}


class VFS:
    """Виртуальная файловая система, целиком хранящаяся в памяти."""

    def __init__(self, root: Dir, source: Path | None = None):
        self.root = root
        self.source = source

    @classmethod
    def default(cls, source: Path | None = None) -> VFS:
        return cls(Dir(""), source)

    @classmethod
    def load(cls, path: str) -> VFS:
        source = Path(path)
        if not source.exists():
            raise VFSError(f"VFS не найдена: {path}")
        if not source.is_dir():
            raise VFSError(f"неверный формат VFS, ожидается директория: {path}")
        try:
            root = _read_dir(source, "")
        except OSError as e:
            raise VFSError(f"ошибка чтения VFS: {e}")
        return cls(root, source)

    def wipe_source(self) -> None:
        """Очищает физическое представление VFS."""
        if self.source is None or not self.source.is_dir():
            return
        for entry in self.source.iterdir():
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()

    def stats(self) -> tuple[int, int]:
        """Количество файлов и каталогов (без корня)."""
        files = dirs = 0
        stack = [self.root]
        while stack:
            for child in stack.pop().children.values():
                if isinstance(child, Dir):
                    dirs += 1
                    stack.append(child)
                else:
                    files += 1
        return files, dirs


def _read_dir(path: Path, name: str) -> Dir:
    node = Dir(name, path.stat().st_mode & 0o777)
    for entry in path.iterdir():
        if entry.is_symlink():
            continue
        if entry.is_dir():
            node.children[entry.name] = _read_dir(entry, entry.name)
        elif entry.is_file():
            mode = entry.stat().st_mode & 0o777
            node.children[entry.name] = File(entry.name, mode, entry.read_bytes())
    return node
