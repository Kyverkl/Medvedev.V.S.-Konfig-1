#!/usr/bin/env bash
# Скрипт запуска эмулятора
set -e
cd "$(dirname "$0")"
uv run repl "$@"
