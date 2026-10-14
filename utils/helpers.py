"""
Helper utilities for terminal rendering, headers, tables, and conversions.
"""
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_header(title: str, width: int = 60):
    print("=" * width)
    print(title.center(width))
    print("=" * width)

def print_separator(char: str = "-", width: int = 60):
    print(char * width)

def print_success(message: str):
    print("\n" + "-" * 50)
    print(f"SUCCESS: {message}")
    print("-" * 50)

def print_error(message: str):
    print("\n" + "!" * 50)
    print(f"ERROR: {message}")
    print("!" * 50)

def print_table(headers: list[str], rows: list[list[str]], col_widths: list[int] = None):
    if not rows:
        print("No records found.")
        return

    num_cols = len(headers)
    if not col_widths:
        col_widths = [len(h) for h in headers]
        for row in rows:
            for idx in range(num_cols):
                val_len = len(str(row[idx]))
                if val_len > col_widths[idx]:
                    col_widths[idx] = val_len

    col_widths = [w + 2 for w in col_widths]
    row_fmt = "".join([f"{{:<{w}}}" for w in col_widths])
    sep = "".join(["-" * w for w in col_widths])

    print(sep)
    print(row_fmt.format(*headers))
    print(sep)
    for r in rows:
        print(row_fmt.format(*[str(cell) for cell in r]))
    print(sep)