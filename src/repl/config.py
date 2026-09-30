import argparse
from dataclasses import dataclass


@dataclass
class Config:
    vfs: str | None
    script: str | None


def parse_args(argv: list[str] | None = None) -> Config:
    parser = argparse.ArgumentParser(prog="repl", description="Эмулятор командной оболочки")
    parser.add_argument("--vfs", help="путь к физическому расположению VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    args = parser.parse_args(argv)
    return Config(vfs=args.vfs, script=args.script)
