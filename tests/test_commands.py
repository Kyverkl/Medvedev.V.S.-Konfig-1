"""Тесты команд без GUI."""
from repl.shell import Shell
from repl.vfs import Dir, File, VFS


def make_shell():
    root = Dir("")
    content = b"a b" + b"\n" + b"c" + b"\n"
    root.children["hello.txt"] = File("hello.txt", 0o644, content)
    root.children["dir"] = Dir("dir", 0o755)
    shell = Shell(output=lambda s: None)
    shell.vfs = VFS(root)
    return shell


def test_ls():
    shell = make_shell()
    out = shell.commands["ls"].run(shell, [])
    assert "hello.txt" in out
    assert "dir" in out


def test_cat():
    shell = make_shell()
    out = shell.commands["cat"].run(shell, ["hello.txt"])
    assert "a b" in out


def test_wc():
    shell = make_shell()
    out = shell.commands["wc"].run(shell, ["hello.txt"])
    assert "hello.txt" in out


def test_cd():
    shell = make_shell()
    shell.commands["cd"].run(shell, ["dir"])
    assert shell.cwd == "/dir"


def test_unknown_command():
    shell = make_shell()
    ok = shell.execute("nope")
    assert ok is False

