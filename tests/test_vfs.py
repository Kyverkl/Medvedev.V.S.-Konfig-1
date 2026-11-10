"""Тесты VFS: normalize и права."""
from repl.vfs import Dir, File, normalize, mode_string


def test_normalize_absolute():
    assert normalize("/a", "/b/c") == "/b/c"


def test_normalize_relative():
    assert normalize("/home", "user") == "/home/user"
    assert normalize("/home/user", "..") == "/home"
    assert normalize("/home/user", "../..") == "/"


def test_normalize_dot():
    assert normalize("/a", "./b") == "/a/b"
    assert normalize("/a", ".") == "/a"


def test_mode_string_file():
    node = File("x", 0o644, b"")
    assert mode_string(node) == "-rw-r--r--"


def test_mode_string_dir():
    node = Dir("d", 0o755)
    assert mode_string(node) == "drwxr-xr-x"
