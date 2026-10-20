#!/usr/bin/env python3
"""Tidy files into folders by extension.

Preview changes by default. Add --apply to move files.
"""
import argparse
import shutil
from pathlib import Path

EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".rtf": "Documents",
    ".md": "Documents",
    # Spreadsheets
    ".csv": "Spreadsheets",
    ".xls": "Spreadsheets",
    ".xlsx": "Spreadsheets",
    ".ods": "Spreadsheets",
    # Images
    ".png": "Images",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".tif": "Images",
    ".tiff": "Images",
    ".webp": "Images",
}


def categorise(file_path):
    """Return the destination category for a file."""
    extension = Path(file_path).suffix.lower()
    return EXTENSION_MAP.get(extension, "Other")


def print_summary(counts, total):
    """Print category counts and the overall total."""
    print("\nSummary:")
    for category in sorted(counts):
        print(f"{category}: {counts[category]} file(s)")
    print(f"Total: {total} file(s)")


def main():
    parser = argparse.ArgumentParser(
        description="Sort files into subfolders by file type."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files. Without this flag, only preview changes.",
    )
    parser.add_argument(
        "--folder",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Folder to tidy (defaults to the folder containing this script).",
    )
    args = parser.parse_args()

    folder = args.folder.resolve()
    if not folder.is_dir():
        parser.error(f"Folder does not exist: {folder}")

    counts = {}
    total = 0
    planned_moves = []

    # Only inspect files directly inside the target folder, not its subfolders.
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item == Path(__file__).resolve():
            continue

        category = categorise(item)
        counts[category] = counts.get(category, 0) + 1
        total += 1
        destination_folder = folder / category
        destination = destination_folder / item.name

        if destination.exists():
            print(f"SKIP (destination already exists): {item.name} -> {destination}")
            continue

        planned_moves.append((item, destination_folder, destination, category))

    if args.apply:
        for source, destination_folder, destination, category in planned_moves:
            destination_folder.mkdir(parents=True, exist_ok=True)
            # Re-check immediately before moving so an existing file is never overwritten.
            if destination.exists():
                print(f"SKIP (destination already exists): {source.name} -> {destination}")
                continue
            shutil.move(str(source), str(destination))
            print(f"MOVED: {source.name} -> {category}/")
        print("\nFolder tidy complete.")
    else:
        for source, destination_folder, destination, category in planned_moves:
            print(f"DRY RUN: {source.name} -> {category}/")
        print("\nDry run only: no files were moved. Add --apply to make these changes.")

    print_summary(counts, total)


if __name__ == "__main__":
    main()
