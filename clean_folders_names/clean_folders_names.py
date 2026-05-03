#!/usr/bin/env python3
import os
import re
import sys
import argparse

def clean_name(name: str) -> str:
    """Convert _ to space, replace en/em dashes with hyphen, keep only allowed chars, collapse spaces, strip edges."""
    name = name.replace('_', ' ')
    name = name.replace('–', '-').replace('—', '-')
    # Keep only: a-z, A-Z, 0-9, space, standard hyphen, dot
    cleaned = re.sub(r'[^a-zA-Z0-9\s\-\.]', '', name)
    cleaned = re.sub(r'\s+', ' ', cleaned)          # collapse multiple spaces
    # cleaned = re.sub(r'-{2,}', '-', cleaned)     # optional hyphen collapse
    cleaned = cleaned.strip(' -')                   # strip leading/trailing spaces and hyphens
    return cleaned

def get_all_renames(root_dir: str):
    """Walk bottom-up and collect (old_path, new_name, new_path) for all needed renames."""
    changes = []
    for dirpath, dirnames, _ in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            old_path = os.path.join(dirpath, dirname)
            new_name = clean_name(dirname)
            if new_name == dirname or not new_name:
                continue
            new_path = os.path.join(dirpath, new_name)
            # Avoid duplicate targets from different source folders
            if any(new_path == existing_old for existing_old, _, _ in changes):
                continue
            changes.append((old_path, new_name, new_path))
    return changes

def preview_changes(changes):
    if not changes:
        print("No folders need renaming.")
        return False
    print(f"\nFound {len(changes)} folder(s) that will change:\n")
    for old, new_name, new_path in changes:
        print(f"  {old}")
        print(f"  → {new_path}\n")
    return True

def apply_renames(changes):
    print("\nProceeding with actual renaming...")
    renamed_count = 0
    for old, new_name, new_path in changes:
        if os.path.exists(new_path):
            print(f"⚠️ Conflict: {old} → {new_path} already exists. Skipping.")
            continue
        try:
            os.rename(old, new_path)
            print(f"✓ Renamed: {old} → {new_path}")
            renamed_count += 1
        except Exception as e:
            print(f"✗ Error renaming {old}: {e}")
    print(f"\nDone. Renamed {renamed_count} of {len(changes)} folders.")
    return renamed_count

def main():
    parser = argparse.ArgumentParser(description="Clean folder names: keep letters/numbers/spaces/hyphens/dots, convert _ to space, replace dashes.")
    parser.add_argument("path", nargs="?", default=None, help="Root folder to process (default: current directory)")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Preview changes without renaming (forces interactive path if not given)")
    parser.add_argument("-a", "--actual", action="store_true", help="Actually rename folders (forces interactive path if not given)")
    args = parser.parse_args()

    # Determine root directory
    if args.path:
        root_dir = args.path
    else:
        # Interactive path input if not provided
        path_input = input("Enter folder path (or press Enter for current directory): ").strip()
        root_dir = path_input if path_input else '.'

    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a valid directory.")
        sys.exit(1)

    # Decide mode: command line args override interactive
    if args.actual:
        mode = 'actual'
    elif args.dry_run:
        mode = 'dry-run'
    else:
        # Interactive mode: ask BEFORE scanning
        print("\n=== Folder Name Cleaner ===")
        print("Keeps: letters, numbers, spaces, hyphens (en/em → -), dots")
        print("Converts underscores (_) to spaces, collapses multiple spaces, strips edges.\n")
        mode_input = input("Run in (d)ry-run mode or (a)ctual rename? (d/a): ").strip().lower()
        if mode_input == 'a':
            mode = 'actual'
        else:
            mode = 'dry-run'   # default to dry-run if anything else

    # Now scan (only once, after mode is chosen)
    print(f"\nScanning '{root_dir}' for folders to rename...")
    changes = get_all_renames(root_dir)

    if not preview_changes(changes):
        return

    if mode == 'dry-run':
        print("[DRY RUN] No changes were made.")
        # Ask if user wants to proceed for real
        proceed = input("\nWould you like to proceed with actual renaming now? (y/n): ").strip().lower()
        if proceed == 'y':
            apply_renames(changes)
        else:
            print("Exiting without changes.")
    else:  # actual mode
        apply_renames(changes)

if __name__ == "__main__":
    main()