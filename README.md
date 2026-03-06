# SQL Merge Tool

A simple Python script to recursively scan all `.sql` files under a configured absolute path and generate one merged SQL file in that same directory.

## Features

- Recursive scan for all `.sql` files
- Stable sorting by relative path
- Output merged SQL file to target directory
- Supports UTF-8 / UTF-8-SIG / GBK fallback reading

## Usage

1. Edit the `ROOT_DIR` in `merge_sql_files.py`
2. Run:

```bash
python merge_sql_files.py
