import calendar
from datetime import date

from repl.commands.base import Command, CommandError

MAX_ARGS = 2
MIN_YEAR = 1
MAX_YEAR = 9999
MIN_MONTH = 1
MAX_MONTH = 12


class Cal(Command):
    name = "cal"
    usage = "cal [[месяц] год]"
    description = "календарь на текущий месяц, заданный месяц или год"

    def run(self, shell, args: list[str]) -> str:
        if len(args) > MAX_ARGS:
            raise CommandError("cal: слишком много аргументов")
        try:
            numbers = [int(arg) for arg in args]
        except ValueError:
            joined = " ".join(args)
            raise CommandError(f"cal: неверный аргумент: {joined}")

        cal = calendar.TextCalendar(calendar.MONDAY)
        today = date.today()
        if not numbers:
            return cal.formatmonth(today.year, today.month)
        year = numbers[-1]
        if not MIN_YEAR <= year <= MAX_YEAR:
            raise CommandError(
                f"cal: год {year} вне диапазона "
                f"{MIN_YEAR}..{MAX_YEAR}"
            )
        if len(numbers) == 1:
            return cal.formatyear(year)
        month = numbers[0]
        if not MIN_MONTH <= month <= MAX_MONTH:
            raise CommandError(
                f"cal: месяц {month} вне диапазона "
                f"{MIN_MONTH}..{MAX_MONTH}"
            )
        return cal.formatmonth(year, month)
