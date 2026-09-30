from repl.commands.base import Command, CommandError
from repl.commands.cd import Cd
from repl.commands.exit import Exit
from repl.commands.ls import Ls


def all_commands() -> dict[str, Command]:
    return {cmd.name: cmd for cmd in (Ls(), Cd(), Exit())}


__all__ = ["Command", "CommandError", "all_commands"]
