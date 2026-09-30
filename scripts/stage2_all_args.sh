#!/usr/bin/env bash
# Оба параметра заданы корректно
cd "$(dirname "$0")/.."
uv run repl --vfs vfs/minimal --script startup/stage2.txt
