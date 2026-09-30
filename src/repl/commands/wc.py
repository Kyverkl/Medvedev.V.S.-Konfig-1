from repl.commands.base import Command, CommandError, get_file

# Ключ -> индекс счётчика: строки, слова, байты
FLAGS = {"-l": 0, "-w": 1, "-c": 2}


class Wc(Command):
    name = "wc"
    usage = "wc [-l] [-w] [-c] файл..."
    description = "число строк, слов и байт в файлах"

    def run(self, shell, args: list[str]) -> str:
        columns = set()
        paths = []
        for arg in args:
            if arg in FLAGS:
                columns.add(FLAGS[arg])
            elif arg.startswith("-"):
                raise CommandError(f"wc: неверный ключ: {arg}")
            else:
                paths.append(arg)
        if not paths:
            raise CommandError("wc: не указан файл")

        rows = []
        total = [0, 0, 0]
        for path in paths:
            data = get_file(shell, "wc", path).content
            counts = [data.count(b"\n"), len(data.split()), len(data)]
            total = [a + b for a, b in zip(total, counts)]
            rows.append((counts, path))
        if len(paths) > 1:
            rows.append((total, "итого"))

        shown = sorted(columns) or [0, 1, 2]
        return "\n".join("".join(f"{counts[i]:>7}" for i in shown) + f" {name}" for counts, name in rows)
