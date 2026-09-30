#!/usr/bin/env bash
# chmod меняет права только в памяти: права на диске до и после запуска совпадают
cd "$(dirname "$0")/.."
ls -l vfs/deep/etc vfs/deep/home/user/docs
uv run repl --vfs vfs/deep --script startup/stage5.txt
ls -l vfs/deep/etc vfs/deep/home/user/docs
