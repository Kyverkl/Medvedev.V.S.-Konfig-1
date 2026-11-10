from repl.commands.base import Command, CommandError, get_file

IDX_LINES = 0
IDX_WORDS = 1
IDX_BYTES = 2
FLAGS = {"-l": IDX_LINES, "-w": IDX_WORDS, "-c": IDX_BYTES}
ALL_COLUMNS = [IDX_LINES, IDX_WORDS, IDX_BYTES]


class Wc(Command):
    name = "wc"
    usage = "wc [-l] [-w] [-c] файл..."
    description = "число строк, слов и байт в файлах"

    def run(self, shell, args: list[str]) -> str:
        columns, paths = self._parse_args(args)
        if not paths:
            raise CommandError("wc: не указан файл")
        rows, total = self._count_all(shell, paths)
        if len(paths) > 1:
            rows.append((total, "итого"))
        shown = sorted(columns) or ALL_COLUMNS
        return self._format_rows(rows, shown)

    def _parse_args(
        self, args: list[str]
    ) -> tuple[set[int], list[str]]:
        columns: set[int] = set()
        paths: list[str] = []
        for arg in args:
            if arg in FLAGS:
                columns.add(FLAGS[arg])
            elif arg.startswith("-"):
                raise CommandError(f"wc: неверный ключ: {arg}")
            else:
                paths.append(arg)
        return columns, paths

    def _count_all(
        self, shell, paths: list[str]
    ) -> tuple[list[tuple[list[int], str]], list[int]]:
        rows = []
        total = [0, 0, 0]
        for path in paths:
            data = get_file(shell, "wc", path).content
            counts = self._count_data(data)
            total = [a + b for a, b in zip(total, counts)]
            rows.append((counts, path))
        return rows, total

    @staticmethod
    def _count_data(data: bytes) -> list[int]:
        return [
            data.count(b"\n"),
            len(data.split()),
            len(data),
        ]

    @staticmethod
    def _format_rows(
        rows: list[tuple[list[int], str]], shown: list[int]
    ) -> str:
        lines = []
        for counts, name in rows:
            nums = "".join(f"{counts[i]:>7}" for i in shown)
            lines.append(f"{nums} {name}")
        return "\n".join(lines)
