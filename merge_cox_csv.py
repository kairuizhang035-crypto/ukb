#!/usr/bin/env python3
"""Merge model Cox result CSV files into a single output CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

DEFAULT_INPUT_FILES = [
    Path("01_五分类_Model1_Cox结果.csv"),
    Path("02_五分类_Model2_Cox结果.csv"),
    Path("03_五分类_Model3_Cox结果.csv"),
]
DEFAULT_OUTPUT_FILE = Path("合并_五分类_Cox结果.csv")


def merge_csv_files(input_files: list[Path], output_file: Path, add_bom: bool = False) -> int:
    header: list[str] | None = None
    row_count = 0

    encoding = "utf-8-sig" if add_bom else "utf-8"
    with output_file.open("w", newline="", encoding=encoding) as out_fp:
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT_FILE})",
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        default=DEFAULT_INPUT_FILES,
        help="Input CSV files (default: Model1/Model2/Model3 files)",
    )
    parser.add_argument("--bom", action="store_true", help="Write UTF-8 BOM for Excel compatibility")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    merged_rows = merge_csv_files(args.inputs, args.output, add_bom=args.bom)
    print(f"Merged {len(args.inputs)} files into {args.output} with {merged_rows} data rows.")
