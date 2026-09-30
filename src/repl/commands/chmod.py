import re

from repl.commands.base import Command, CommandError

OCTAL = re.compile(r"[0-7]{1,4}")
SYMBOLIC = re.compile(r"([ugoa]*)([+\-=])([rwx]*)")
WHO = {"u": 0o700, "g": 0o070, "o": 0o007, "a": 0o777}
PERMS = {"r": 0o444, "w": 0o222, "x": 0o111}


def apply_mode(mode: int, spec: str) -> int:
    """Новые права по восьмеричной (755) или символьной (u+x,go-w) записи."""
    if OCTAL.fullmatch(spec):
        return int(spec, 8) & 0o777
    for clause in spec.split(","):
        match = SYMBOLIC.fullmatch(clause)
        if match is None:
            raise ValueError(spec)
        who, op, perms = match.groups()
        who_mask = 0
        for c in who or "a":
            who_mask |= WHO[c]
        bits = 0
        for c in perms:
            bits |= PERMS[c]
        bits &= who_mask
        if op == "+":
            mode |= bits
        elif op == "-":
            mode &= ~bits
        else:
            mode = (mode & ~who_mask) | bits
    return mode & 0o777


class Chmod(Command):
    name = "chmod"
    usage = "chmod режим путь..."
    description = "изменение прав доступа (755, u+x, go-w, a=r); только в памяти"

    def run(self, shell, args: list[str]) -> str:
        if len(args) < 2:
            raise CommandError("chmod: нужно указать режим и хотя бы один путь")
        spec, paths = args[0], args[1:]
        nodes = []
        for path in paths:
            node = shell.lookup(path)
            if node is None:
                raise CommandError(f"chmod: {path}: нет такого файла или каталога")
            nodes.append(node)
        for node in nodes:
            try:
                node.mode = apply_mode(node.mode, spec)
            except ValueError:
                raise CommandError(f"chmod: неверный режим: {spec}")
        return ""
