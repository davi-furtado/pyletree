# Usage

## CLI options

### General

- `-h`, `--help` Show help message
- `-v`, `--version` Show version

### Modes

- `-do`, `--dir-only` Show directories only
- `-fo`, `--files-only` Show files only

### Ordering

- `-d`, `--dirs-first` List directories before files
- `-f`, `--files-first` List files before directories
- `-r`, `--reverse` Reverse alphabetical sort order

### Size

- `-fs`, `--file-size` Display individual file sizes
- `-ds`, `--dir-size` Display cumulative directory sizes
- `-b`, `--big-first` Order entries by size (largest first)
- `-s`, `--small-first` Order entries by size (smallest first)

### Display

- `-n`, `--no-pipes` Remove vertical pipes between branches
- `-p`, `--path-tree` Generate a view focused exclusively on full paths
- `-t [N]`, `--text-only [N]` Text-only mode: tree in plain text with `N` spaces indentation (default: 2)

### Ignoring

- `-git [DIR ...]`, `--git [DIR ...]` Ignore `.git` folder and respect `.gitignore` rules from specific directories or `.git` folders.
- `-g [DIR_OR_FILE ...]`, `--gitignore [DIR_OR_FILE ...]` Respect `.gitignore` rules from given paths or directories.
- `-i PATTERN [PATTERN ...]`, `--ignore PATTERN [PATTERN ...]` Ignore files/directories matching gitignore-style patterns.
- `-fi PATTERN [PATTERN ...]`, `--filter PATTERN [PATTERN ...]` Include only files or directories matching gitignore-style patterns.

### Depth and output

- `-dl N`, `--depth-level N` Limit tree depth (must be >= 0)
- `-dt [N]`, `--dict-tree [N]` Output the tree as a JSON dictionary. `N` defines indentation spaces for CLI display only (default: 2). Use `0` for compact output.

## Examples

```bash
pyletree .
pyletree . -d
pyletree . -fo
pyletree . -dl 2
pyletree . -dt 4
pyletree . -i node_modules dist .git
pyletree . -fi *.py docs/
pyletree . -g
pyletree . -git
pyletree . -n
pyletree . -t 4
pyletree . -fs
pyletree . -ds
pyletree . -b -fs
pyletree . -s -fs
pyletree . -r
pyletree . -p
pyletree src/ -d -fs -dl 3 -i __pycache__
```
