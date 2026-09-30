#!/usr/bin/env bash
# Ошибки загрузки VFS: каталог не найден, неверный формат (файл вместо каталога)
cd "$(dirname "$0")/.."
uv run repl --vfs vfs/not-exists --script startup/stage2.txt
uv run repl --vfs README.md --script startup/stage2.txt
