<div align="center">
  <h1 align="center">Pyletree</h1>

  <img src="https://img.shields.io/badge/python-3.8%2B-blue">
  <img src="https://img.shields.io/badge/license-MIT-green">
  <img src="https://img.shields.io/badge/version-2.0.0-orange">

  <img src="https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/pypi-%23ececec.svg?logo=pypi&logoColor=1f73b7">
  <img src="https://img.shields.io/badge/github%20actions-%232671E5.svg?logo=githubactions&logoColor=white">
</div>

<p align="right"><i>Pyletree is a simple and fast CLI tool to generate directory tree diagrams.</i></p>

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
  - [General](#general)
  - [Modes](#modes)
  - [Ordering](#ordering)
  - [Display](#display)
  - [Ignoring](#ignoring)
  - [Depth](#depth)
- [Examples](#examples)
- [Python API](#python-api)
- [Sample Output](#sample-output)
- [Features](#features)
- [Release History](#release-history)
- [Authors](#authors)
- [License](#license)

## Installation

### From PyPI

```bash
pip install pyletree
```

### Local

```bash
git clone https://github.com/davi-furtado/pyletree.git
cd pyletree
pip install -e .
```

## Usage

```bash
pyletree [ROOT_DIR]
```

If no directory is provided, the current directory is used:

```bash
pyletree
```

Show help:

```bash
pyletree -h
```

## Options

### General

- `-h`, `--help` Show help message
- `-v`, `--version` Show version

### Modes

- `-do`, `--dir-only` Show directories only
- `-fo`, `--files-only` Show files only

### Ordering

- `-d`, `--dirs-first` List directories before files
- `-f`, `--files-first` List files before directories

> Alphabetical order is always applied as base sorting.

### Display

- `-n`, `--no-pipes` Remove vertical pipes between branches

### Ignoring

- `-g [DIR_OR_FILE ...]`, `--git [DIR_OR_FILE ...]` Ignore `.git` folder and respect rules from given `.gitignore` paths/dirs (defaults to current dir if omitted but flag is used)
- `-gi [DIR_OR_FILE ...]`, `--gitignore [DIR_OR_FILE ...]` Respect `.gitignore` rules from given paths/dirs (defaults to current dir if omitted)
- `-i`, `--ignore PATTERN [PATTERN ...]` Ignore files/directories

### Depth

- `-dl`, `--depth-level N` Limit depth

## Examples

Basic:

```bash
pyletree
```

Directories first:

```bash
pyletree . -d
```

Files only:

```bash
pyletree . -fo
```

Limit depth:

```bash
pyletree . -dl 2
```

Ignore entries:

```bash
pyletree . -i node_modules dist .git
```

Use `.gitignore`:

```bash
pyletree . -gi
```

No pipes mode:

```bash
pyletree . -n
```

## Python API

You can also use Pyletree programmatically in your own Python code using the `FileTree` class. It returns an iterable that can also be printed directly:

```python
from pyletree import FileTree

# Create a tree for the current directory
tree = FileTree()

# Print the tree directly
print(tree)

# Or iterate over its lines
for line in tree:
    print(line)

# You can configure it with the same options of the CLI
custom_tree = FileTree(
    root_dir='src/',
    dir_only=True,
    ignore=['__pycache__']
)
print(custom_tree)
```

## Sample Output

### Default

```text
project/
│
├── src/
│   ├── main.py
│   └── utils.py
│
├── tests/
│   └── test_main.py
│
└── README.md
```

### No pipes (`-n`)

```text
project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
└── README.md
```

## Features

- Clean and readable tree output
- `.gitignore` support (it does not ignore either the `.git` directory or the `.gitignore` file; if you want to ignore them, add them to the ignore patterns)
- Custom ignore patterns
- Depth limiting
- Flexible sorting
- Optional compact mode (`--no-pipes`)

## Release History

### 2.0.0

#### Visual & Metadata

- `-p`/`--path-tree` | Path Tree: generates a view focused exclusively on the paths of files and directories.
- `-o [N]` | Text-Only Mode: generates the tree in plain text (without special characters). Accepts an optional parameter `N` to define the indentation (default: 2 spaces). Can't be used with `-n`.
- `-fs`/`--file-size` | File Sizes: toggle visibility of individual file sizes.
- `-ds`/`--dir-size` | Directory Sizes: display cumulative sizes for folders.
- [`-b`/`--big-first` | `-s`/`--small-first`] | Smart Sorting: order tree entries by size (descending/ascending).

#### Filtering & Data Structures

- `-dt`/`--dict-tree` | Dictionary format: output the tree structure as a native Python dictionary.
- Global File Filter: support for excluding/including files based on patterns or extensions.
- Add patterns to `-i` / `--ignore` option.

#### API Enhancements

- `FileTree.getPath(name)`: new method to programmatically retrieve the full path of a specific file or directory within the tree.
- Add `dict(FileTree)` method to convert the tree to a dictionary.
- Add `FileTree.getTree()` method to convert the tree to a string.
- Add `FileTree.getDictTree()` method to convert the tree to a dictionary.

### 1.1.0

- Removed `-o` / `--output-file` option
- Added `FileTree` class for programmatic usage in Python scripts.

### 1.0.0

- Initial release

## Authors

Davi Reis Furtado

**Original RP Tree Author:**
Leodanis Pozo Ramos

## License

_Pyletree_ is distributed under the MIT license. See [LICENSE](LICENSE) for more information.
