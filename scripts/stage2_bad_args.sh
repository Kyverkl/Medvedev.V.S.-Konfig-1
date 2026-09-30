#!/usr/bin/env bash
# Несуществующий скрипт, затем запуск без параметров
cd "$(dirname "$0")/.."
uv run repl --vfs /nonexistent/vfs --script startup/missing.txt
uv run repl
