import calendar
from datetime import date

from repl.commands.base import Command, CommandError


class Cal(Command):
    name = "cal"
    usage = "cal [[месяц] год]"
    description = "календарь на текущий месяц, заданный месяц или год"

    def run(self, shell, args: list[str]) -> str:
        if len(args) > 2:
            raise CommandError("cal: слишком много аргументов")
        try:
            numbers = [int(arg) for arg in args]
        except ValueError:
            raise CommandError(f"cal: неверный аргумент: {' '.join(args)}")

        cal = calendar.TextCalendar(calendar.MONDAY)
        today = date.today()
        if not numbers:
            return cal.formatmonth(today.year, today.month)
        year = numbers[-1]
        if not 1 <= year <= 9999:
            raise CommandError(f"cal: год {year} вне диапазона 1..9999")
        if len(numbers) == 1:
            return cal.formatyear(year)
        month = numbers[0]
        if not 1 <= month <= 12:
            raise CommandError(f"cal: месяц {month} вне диапазона 1..12")
        return cal.formatmonth(year, month)
