#!/usr/bin/env python3
"""
Automatic File Organizer

Walks through a root directory, classifies files by type and year/extension,
and organizes them into a destination directory.

Requirements:
- Python 3.8+
- Libraries: tqdm, os, pathlib, shutil, argparse, datetime, csv
"""

import os
import shutil
from pathlib import Path
from tqdm import tqdm
from datetime import datetime
import argparse
import csv
import time

# ----------------------------
# CATEGORY CONFIGURATION
# ----------------------------
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".svg", ".webp", ".heic", ".ico", ".raw", ".psd", ".ai", ".indd"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".mpeg", ".mpg", ".3gp", ".m4v", ".vob"],
    "Music": [".mp3", ".flac", ".wav", ".aac", ".ogg", ".wma", ".m4a", ".alac", ".aiff", ".opus"],
    "Documents": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".txt", ".odt", ".ods", ".odp", ".rtf", ".tex", ".csv", ".md", ".log"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso", ".dmg", ".cab"],
    "Executables": [".exe", ".msi", ".bat", ".cmd", ".sh", ".jar", ".app", ".apk"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".fnt"],
    "Scripts_and_Code": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".rb", ".php", ".html", ".css", ".json", ".xml", ".sql", ".sh", ".pl", ".go", ".rs", ".swift", ".kt"],
    "Disk_Images": [".iso", ".img", ".bin", ".cue", ".mdf", ".mds"],
    "3D_Models": [".obj", ".fbx", ".stl", ".dae", ".3ds", ".blend", ".ply"],
    "Others": [".bak", ".tmp", ".log", ".dat", ".cfg", ".ini"]
}

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------

def get_file_category(file_path: Path) -> str:
    """Returns the main category of the file based on its extension."""
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def get_subfolder_name(file_path: Path, category: str) -> str:
    """Returns the subfolder based on year or extension."""
    if category in ["Images", "Videos"]:
        try:
            timestamp = file_path.stat().st_mtime
            year = datetime.fromtimestamp(timestamp).year
            return f"{year}"
        except Exception:
            return "UnknownYear"
    elif category in ["Documents","Archives","Executables","Fonts","Scripts_and_Code","Disk_Images","3D_Models","Others"]:
        return file_path.suffix.lower().lstrip(".")
    else:
        return "Unknown"

def safe_move_or_copy(src: Path, dst: Path, move: bool = True):
    """Moves or copies a file, renaming if it already exists."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    counter = 1
    target = dst
    while target.exists():
        target = dst.with_name(f"{dst.stem}_{counter}{dst.suffix}")
        counter += 1
    try:
        if move:
            shutil.move(str(src), str(target))
        else:
            shutil.copy2(str(src), str(target))
        return target
    except Exception as e:
        print(f"[ERROR] Could not process {src}: {e}")
        return None

# ----------------------------
# MAIN FUNCTION
# ----------------------------

def organize_files(
    source_dir: Path,
    dest_dir: Path,
    move: bool = True,
    dry_run: bool = False,
    report_file: Path = None
):
    """
    Organizes files from the source directory into the destination.
    """
    files_to_process = []

    # 1️⃣ Recursively walk through source directory
    for root, dirs, files in os.walk(source_dir):
        # Ignore the destination folder itself
        dirs[:] = [d for d in dirs if Path(root, d) != dest_dir]
        for file in files:
            files_to_process.append(Path(root) / file)

    # 2️⃣ Prepare summary counts
    summary = {}
    for file_path in files_to_process:
        category = get_file_category(file_path)
        summary.setdefault(category, 0)
        summary[category] += 1

    # 3️⃣ Show summary to the user
    print("\nSummary of files found by category:")
    for cat, count in summary.items():
        print(f"- {cat}: {count}")
    print(f"Total: {len(files_to_process)} files\n")

    # 4️⃣ Confirm execution
    proceed = input("Do you want to continue? (y/n): ").lower()
    if proceed != "y":
        print("Operation canceled by user.")
        return

    # 5️⃣ Process files with progress bar
    processed_files = []
    for file_path in tqdm(files_to_process, desc="Organizing", unit="file"):
        category = get_file_category(file_path)
        subfolder = get_subfolder_name(file_path, category)
        target_dir = dest_dir / category / subfolder
        target_path = target_dir / file_path.name

        if dry_run:
            # Simulation only
            processed_files.append({
                "source": str(file_path),
                "destination": str(target_path),
                "action": "MOVE" if move else "COPY"
            })
            continue

        result = safe_move_or_copy(file_path, target_path, move=move)
        if result:
            processed_files.append({
                "source": str(file_path),
                "destination": str(result),
                "action": "MOVE" if move else "COPY"
            })

    # 6️⃣ Optional report generation
    if report_file:
        try:
            with open(report_file, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["source", "destination", "action"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in processed_files:
                    writer.writerow(row)
            print(f"Report saved to: {report_file}")
        except Exception as e:
            print(f"[ERROR] Could not generate report: {e}")

    print("\nOrganization completed!")
    print(f"Total execution time: {time.perf_counter() - start_time:.2f} seconds")

# ----------------------------
# ARGPARSE EXECUTION
# ----------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Automatic File Organizer"
    )
    parser.add_argument(
        "-o", "--source", required=True, type=Path,
        help="Root source directory"
    )
    parser.add_argument(
        "-d", "--destination", required=True, type=Path,
        help="Destination directory"
    )
    parser.add_argument(
        "-c", "--copy", action="store_true",
        help="Copy files instead of moving"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Simulate operation without moving/copying files"
    )
    parser.add_argument(
        "-r", "--report", type=Path,
        help="Generate CSV report after execution"
    )
    return parser.parse_args()

# ----------------------------
# ENTRY POINT
# ----------------------------

if __name__ == "__main__":
    args = parse_args()
    start_time = time.perf_counter()
    organize_files(
        source_dir=args.source.resolve(),
        dest_dir=args.destination.resolve(),
        move=not args.copy,
        dry_run=args.dry_run,
        report_file=args.report.resolve() if args.report else None
    )