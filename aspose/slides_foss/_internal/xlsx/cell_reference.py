"""
Cell reference utilities for A1-notation parsing and formatting.

All row/col indices are 0-based internally.
A1 notation uses 1-based rows and letter-based columns (A=0, B=1, ..., Z=25, AA=26).
"""

from __future__ import annotations
import re
from typing import Iterator

_CELL_RE = re.compile(r'^\$?([A-Z]+)\$?(\d+)$')


def col_letter_to_index(letters: str) -> int:
    """Convert column letters to 0-based index. 'A'->0, 'Z'->25, 'AA'->26."""
    result = 0
    for ch in letters.upper():
        result = result * 26 + (ord(ch) - ord('A') + 1)
    return result - 1


def col_index_to_letter(index: int) -> str:
    """Convert 0-based column index to letters. 0->'A', 25->'Z', 26->'AA'."""
    result = []
    n = index + 1
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result.append(chr(ord('A') + remainder))
    return ''.join(reversed(result))


def parse_cell_ref(ref: str) -> tuple[int, int]:
    """
    Parse A1-notation cell reference to (row, col), both 0-based.
    Strips '$' signs for absolute references.

    'A1' -> (0, 0), 'B3' -> (2, 1), '$C$5' -> (4, 2)
    """
    m = _CELL_RE.match(ref.strip())
    if not m:
        raise ValueError(f"Invalid cell reference: {ref!r}")
    col = col_letter_to_index(m.group(1))
    row = int(m.group(2)) - 1
    return (row, col)


def format_cell_ref(row: int, col: int) -> str:
    """
    Format (row, col) as A1-notation. Both inputs are 0-based.

    (0, 0) -> 'A1', (2, 1) -> 'B3'
    """
    return f"{col_index_to_letter(col)}{row + 1}"


def parse_range_ref(ref: str) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Parse range reference to ((top_row, left_col), (bottom_row, right_col)), 0-based.
    Strips '$' signs and 'SheetName!' prefix.

    'A1:D5' -> ((0, 0), (4, 3))
    'Sheet1!$A$1:$D$5' -> ((0, 0), (4, 3))
    """
    # Strip sheet name prefix
    if '!' in ref:
        ref = ref.split('!', 1)[1]
    parts = ref.split(':')
    if len(parts) != 2:
        raise ValueError(f"Invalid range reference: {ref!r}")
    return (parse_cell_ref(parts[0]), parse_cell_ref(parts[1]))


def iterate_range(ref: str) -> Iterator[tuple[int, int, str]]:
    """
    Yield (row, col, cell_ref) for each cell in a range, row by row.

    'A1:B2' yields: (0,0,'A1'), (0,1,'B1'), (1,0,'A2'), (1,1,'B2')
    """
    (r1, c1), (r2, c2) = parse_range_ref(ref)
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            yield (r, c, format_cell_ref(r, c))
