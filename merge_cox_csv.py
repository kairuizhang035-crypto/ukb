#!/usr/bin/env python3
"""Merge model Cox result CSV files into a single output CSV."""

from __future__ import annotations

import csv
from pathlib import Path

INPUT_FILES = [
    Path("01_五分类_Model1_Cox结果.csv"),
    Path("02_五分类_Model2_Cox结果.csv"),
    Path("03_五分类_Model3_Cox结果.csv"),
]
OUTPUT_FILE = Path("合并_五分类_Cox结果.csv")


def merge_csv_files(input_files: list[Path], output_file: Path) -> int:
    header: list[str] | None = None
    row_count = 0

    with output_file.open("w", newline="", encoding="utf-8") as out_fp:
        writer = csv.writer(out_fp)

        for file_path in input_files:
            if not file_path.exists():
                raise FileNotFoundError(f"Input file not found: {file_path}")

            with file_path.open("r", newline="", encoding="utf-8") as in_fp:
                reader = csv.reader(in_fp)
                current_header = next(reader, None)
                if current_header is None:
                    continue

                if header is None:
                    header = current_header
                    writer.writerow(header)
                elif current_header != header:
                    raise ValueError(
                        f"Header mismatch in {file_path}. Expected {header}, got {current_header}"
                    )

                for row in reader:
                    if row:
                        writer.writerow(row)
                        row_count += 1

    return row_count


if __name__ == "__main__":
    merged_rows = merge_csv_files(INPUT_FILES, OUTPUT_FILE)
    print(f"Merged {len(INPUT_FILES)} files into {OUTPUT_FILE} with {merged_rows} data rows.")
