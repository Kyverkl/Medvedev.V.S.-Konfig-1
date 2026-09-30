class CommandError(Exception):
    pass


class Command:
    name = ""
    usage = ""
    description = ""

    def run(self, shell, args: list[str]) -> str:
        raise NotImplementedError
