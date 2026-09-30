from repl.commands.base import Command, CommandError
from repl.commands.cal import Cal
from repl.commands.cat import Cat
from repl.commands.cd import Cd
from repl.commands.chmod import Chmod
from repl.commands.exit import Exit
from repl.commands.help import Help
from repl.commands.ls import Ls
from repl.commands.vfs_init import VfsInit
from repl.commands.wc import Wc


def all_commands() -> dict[str, Command]:
    return {cmd.name: cmd for cmd in (Ls(), Cd(), Cat(), Wc(), Cal(), Chmod(), VfsInit(), Help(), Exit())}


__all__ = ["Command", "CommandError", "all_commands"]
