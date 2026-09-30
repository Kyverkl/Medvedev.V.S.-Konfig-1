#!/usr/bin/env bash
# VFS «minimal»; работаем с копией, так как vfs-init очищает каталог
cd "$(dirname "$0")/.."
tmp=$(mktemp -d)
cp -r vfs/minimal/. "$tmp"
uv run repl --vfs "$tmp" --script startup/stage3.txt
rm -rf "$tmp"
