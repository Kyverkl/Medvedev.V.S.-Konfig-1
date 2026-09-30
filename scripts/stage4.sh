#!/usr/bin/env bash
# Команды этапа 4 на VFS с тремя и более уровнями вложенности
cd "$(dirname "$0")/.."
uv run repl --vfs vfs/deep --script startup/stage4.txt
