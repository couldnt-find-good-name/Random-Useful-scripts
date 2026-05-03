# clean_folders_names.py

A Python script to recursively sanitize folder names:  
- Keep only **letters, numbers, spaces, hyphens, and dots**  
- Convert **underscores (`_`) to spaces**  
- Replace **en/em dashes (`–`, `—`) with standard hyphens**  
- Collapse **multiple spaces into one**  
- Strip **leading/trailing spaces and hyphens**  
- Remove **all other special characters** (`! @ # $ % ^ & * ( ) { } [ ] | \ : ; " ' < > , ? / ~`, etc.)

The script walks through all subfolders (deepest first), shows a preview of all changes, and asks for confirmation before applying.

---

## ✨ Features

- **Interactive & non‑interactive** modes – choose at runtime or via command‑line flags.
- **Safe preview** – shows exactly what will be renamed before any changes.
- **Bottom‑up traversal** – avoids breaking paths during renaming.
- **Conflict detection** – skips renaming if the new name already exists.
- **Cross‑platform** – works on Windows, macOS, and Linux.
- **No external dependencies** – uses only Python’s standard library.

---

## 📦 Requirements

- **Python 3.6+** (no additional packages needed)

---

## 🚀 Installation

Clone the repository or download the script directly:

```bash
git clone https://github.com/couldnt-find-good-name/Random-Useful-scripts.git
cd Random-Useful-scripts
```

Make the script executable on Unix‑like systems (optional):
```bash
chmod +x clean_folders_names.py

```

## 🧪 Usage

1. Interactive mode (recommended for first time)

```bash
python clean_folders_names.py
```

The script will:

Ask for the target folder path.

Ask for dry‑run or actual rename mode before scanning.

Show a full preview of all proposed changes.

If in dry‑run mode, ask whether to proceed with real renaming.

2. Command‑line flags (non‑interactive)
Flag	Description
-d, --dry-run	Preview changes without renaming. Exits after showing preview.
-a, --actual	Actually rename folders (after showing preview).
You can also provide the folder path as an argument:

```bash
# Dry‑run on a specific folder
python clean_folders_names.py /path/to/folder -d

# Actually rename on a specific folder
python clean_folders_names.py /path/to/folder -a

# If no path is given, the script will ask for it interactively (even with -d/-a)
python clean_folders_names.py -d
```

## 📝 Examples

| Original folder names | After running the script |
|-----------------------|---------------------------|
| `My_Folder_(2024)!` | `My Folder 2024` |
| `project_alpha-v1.2` | `project alpha-v1.2` |
| `SomeProject – Cool Feature` | `SomeProject - Cool Feature` |
| `My Files - Backup - -` | `My Files - Backup` |
| `..hidden..folder` | `hidden.folder` |


## 🔧 Customisation
You can easily modify the clean_name() function in the script:

You can easily modify the `clean_name()` function in the script:

| Change | Code to uncomment / modify |
|--------|----------------------------|
| Collapse multiple hyphens into one | `# cleaned = re.sub(r'-{2,}', '-', cleaned)` |
| Keep underscores as underscores | Remove the line `name = name.replace('_', ' ')` |
| Keep additional characters (e.g., apostrophe) | Add them to the regex `[^a-zA-Z0-9\s\-\.']` |

## ⚠️ Important Notes
Always backup important data before running the script in actual mode.

If two different folder names become identical after cleaning, the script skips the second one and shows a warning.

Empty folder names (after cleaning) are also skipped – rename them manually.

## 📄 License
MIT License – free to use and modify.

## 🤝 Contributing
Issues and pull requests are welcome. Feel free to suggest improvements or report bugs.

## 📬 Contact
For questions, open an issue on GitHub
