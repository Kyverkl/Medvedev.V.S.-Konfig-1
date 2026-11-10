"""Тесты парсера командной строки."""
from repl.parser import parse


def test_empty():
    assert parse("") == []
    assert parse("   ") == []


def test_command_only():
    assert parse("ls") == ["ls"]


def test_command_with_args():
    assert parse("ls -l /home") == ["ls", "-l", "/home"]
    assert parse("chmod 755 a b") == ["chmod", "755", "a", "b"]
