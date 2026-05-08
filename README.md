<div align="center">
  <h1 align="center">Pyletree</h1>

  <img src="https://img.shields.io/badge/python-3.8%2B-blue">
  <img src="https://img.shields.io/badge/license-MIT-green">
  <img src="https://img.shields.io/badge/version-2.4.0-orange">

  <br>

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
  - [Size](#size)
  - [Display](#display)
  - [Ignoring](#ignoring)
  - [Depth](#depth)
  - [Output Formats](#output-formats)
- [Examples](#examples)
- [Python API](#python-api)
  - [Basic Usage](#basic-usage)
  - [Parameters](#parameters)
  - [Methods](#methods)
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
- `-r`, `--reverse` Reverse alphabetical sort order

> Alphabetical order is always applied as base sorting.

### Size

- `-fs`, `--file-size` Display individual file sizes
- `-ds`, `--dir-size` Display cumulative sizes for directories
- `-b`, `--big-first` Order entries by size (largest first)
- `-s`, `--small-first` Order entries by size (smallest first)

> Size sorting (`-b`/`-s`) is mutually exclusive with ordering (`-d`/`-f`).

### Display

- `-n`, `--no-pipes` Remove vertical pipes between branches
- `-p`, `--path-tree` Generate a view focused exclusively on full paths
- `-o [N]` Text-only mode: tree in plain text with `N` spaces indentation (default: 2). Cannot be used with `-n`

### Ignoring

- `-g [DIR ...]`, `--git [DIR ...]` Ignore `.git` folder and respect rules from given `.git` directories or directories containing `.git` (defaults to current dir if omitted but flag is used)
- `-gi [DIR_OR_FILE ...]`, `--gitignore [DIR_OR_FILE ...]` Respect `.gitignore` rules from given paths/dirs (defaults to current dir if omitted)
- `-i PATTERN [PATTERN ...]`, `--ignore PATTERN [PATTERN ...]` Ignore files/directories matching gitignore-style patterns
- `-fi PATTERN [PATTERN ...]`, `--filter PATTERN [PATTERN ...]` Include only files or directories matching gitignore-style patterns

### Depth

- `-dl N`, `--depth-level N` Limit tree depth (must be >= 0)

### Output Formats

- `-dt [N]`, `--dict-tree [N]` Output the tree structure as a JSON dictionary. `N` defines indentation spaces (default: 2). Use `0` for compact output

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

Dictionary output:

```bash
pyletree . -dt 4
```

Ignore entries:

```bash
pyletree . -i node_modules dist .git
```

Filter entries with patterns:

```bash
pyletree . -fi *.py docs/
```

Use `.gitignore`:

```bash
pyletree . -gi
```

No pipes mode:

```bash
pyletree . -n
```

Show file sizes:

```bash
pyletree . -fs
```

Show directory sizes:

```bash
pyletree . -ds
```

Sort by size (biggest first):

```bash
pyletree . -b -fs
```

Sort by size (smallest first):

```bash
pyletree . -s -fs
```

Reverse alphabetical order:

```bash
pyletree . -r
```

Path tree mode:

```bash
pyletree . -p
```

Text-only mode (4-space indent):

```bash
pyletree . -o 4
```

Git mode (ignore `.git` and apply `.gitignore` rules):

```bash
pyletree . -g
```

Combine options:

```bash
pyletree src/ -d -fs -dl 3 -i __pycache__
```

## Python API

You can also use Pyletree programmatically in your own Python code using the `FileTree` class. It returns an iterable that can also be printed directly.

### Basic Usage

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

### Parameters

All parameters (except `root_dir`) are keyword-only:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `root_dir` | `str \| Path` | `'.'` | Root directory path |
| `dir_only` | `bool` | `False` | Show directories only |
| `files_only` | `bool` | `False` | Show files only |
| `dirs_first` | `bool` | `False` | List directories before files |
| `files_first` | `bool` | `False` | List files before directories |
| `no_pipes` | `bool` | `False` | Remove vertical pipes between branches |
| `ignore` | `list[str] \| None` | `None` | Gitignore-style patterns to ignore |
| `filter` | `list[str] \| None` | `None` | Gitignore-style patterns to include only |
| `use_gitignore` | `bool \| str \| Path \| list` | `False` | Respect `.gitignore` rules. `True` uses current dir, or pass path(s) |
| `depth_level` | `int \| None` | `None` | Limit tree depth |
| `path_tree` | `bool` | `False` | Display full paths instead of names |
| `text_only` | `bool` | `False` | Plain text mode (no special characters) |
| `text_only_indent` | `int` | `2` | Indentation spaces for text-only mode |
| `file_size` | `bool` | `False` | Show individual file sizes |
| `dir_size` | `bool` | `False` | Show cumulative directory sizes |
| `sort_size` | `str \| None` | `None` | Sort by size: `'big'` or `'small'` |
| `reverse` | `bool` | `False` | Reverse alphabetical sort order |

### Methods

#### `getTree() -> str`

Returns the tree as a formatted string:

```python
tree = FileTree('src/')
output = tree.getTree()
```

#### `getDictTree() -> dict`

Returns the tree as a nested dictionary. Files map to `None` (or their size string if `file_size=True`):

```python
tree = FileTree('src/')
data = tree.getDictTree()
# {'src/': {'main.py': None, 'utils.py': None}}

# With file sizes
tree = FileTree('src/', file_size=True)
data = tree.getDictTree()
# {'src/': {'main.py': '1.2 KB', 'utils.py': '856 B'}}
```

#### `getPath(pattern) -> list[Path]`

Search for files or directories matching a pattern. Returns a list of resolved `Path` objects:

```python
tree = FileTree()

# Exact name match
tree.getPath('main.py')

# Glob pattern
tree.getPath('*.py')

# Path pattern
tree.getPath('src/*.py')
```

#### `dict(tree)`

`FileTree` supports `dict()` conversion through `keys()` and `__getitem__()`:

```python
tree = FileTree('src/')
data = dict(tree)
```

#### Iterating

`FileTree` is iterable — each iteration yields one line of the tree:

```python
tree = FileTree()
for line in tree:
    print(line)
```

#### String conversion

`str(tree)` or `print(tree)` returns the full tree as a string:

```python
tree = FileTree()
print(tree)           # prints the tree
text = str(tree)      # stores as string
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

### Text-only mode (`-o`)

```text
project/
  src/
    main.py
    utils.py
  tests/
    test_main.py
  README.md
```

### Path tree (`-p`)

```text
C:/Users/user/project/
│
├── C:/Users/user/project/src/
│   ├── C:/Users/user/project/src/main.py
│   └── C:/Users/user/project/src/utils.py
│
├── C:/Users/user/project/tests/
│   └── C:/Users/user/project/tests/test_main.py
│
└── C:/Users/user/project/README.md
```

### File sizes (`-fs`)

```text
project/
│
├── src/
│   ├── main.py (1.2 KB)
│   └── utils.py (856 B)
│
├── tests/
│   └── test_main.py (420 B)
│
└── README.md (3.1 KB)
```

### Directory sizes (`-ds`)

```text
project/ (5.6 KB)
│
├── src/ (2.1 KB)
│   ├── main.py
│   └── utils.py
│
├── tests/ (420 B)
│   └── test_main.py
│
└── README.md
```

### Dictionary output (`-dt`)

```json
{
  "project/": {
    "src/": {
      "main.py": null,
      "utils.py": null
    },
    "tests/": {
      "test_main.py": null
    },
    "README.md": null
  }
}
```

## Features

- Clean and readable tree output
- `.gitignore` support (it does not ignore either the `.git` directory or the `.gitignore` file; if you want to ignore them, add them to the ignore patterns)
- Custom ignore patterns
- Include-only filter patterns with smart directory inclusion
- Depth limiting
- Flexible sorting (alphabetical, directories/files first, by size)
- Reverse sort order
- File and directory size display
- Path-focused tree view
- Text-only mode with configurable indentation
- Dictionary (JSON) output format
- Optional compact mode (`--no-pipes`)
- Full Python API with `FileTree` class

## Release History

### 2.4.0

#### API Changes

- `FileTree` instance attributes are now **public**. All user-configured parameters (`root_dir`, `dir_only`, `files_only`, `dirs_first`, `files_first`, `no_pipes`, `ignore`, `depth_level`, `path_tree`, `text_only`, `text_only_indent`, `file_size`, `dir_size`, `sort_size`, `reverse`) can be accessed directly without the `_` prefix.
  - Example: `tree.root_dir`, `tree.depth_level`, `tree.dir_only`
  - Internal attributes (`_tree_deque`, `_size_cache`, `_gitignore_list`, `_filter_cache`, `_ignore_spec`, `_filter_spec`) remain private.

#### Documentation

- Complete README with all CLI options, full API reference, and expanded examples.

### 2.3.1

- Improve README.md
- Improve code

### 2.3.0

#### Enhancements

- Integrated `-di`/`--dict-indent` into `-dt`/`--dict-tree`.
  - Example: `pyletree . -dt 4` (4-space indentation)
  - Example: `pyletree . -dt 0` (compact, no indentation)

### 2.2.0

#### Enhancements

- `-dt`/`--dict-tree` | Enhanced Dictionary Output: improved dictionary format with configurable indentation. Now returns `{root: {tree...}}` format and supports custom indentation via `-dt N`/`--dict-tree N` (default 2).
  - Example: `pyletree . -dt 4` (4-space indentation)
  - Example: `pyletree . -dt 0` (compact, no indentation)
  - Better structured output for programmatic use

### 2.1.0

#### New Features

- `-fi`/`--filter` | Include Patterns: display only files and directories matching gitignore-style patterns. Supports multiple patterns and maintains tree hierarchy by including parent directories of matching files.
  - Example: `pyletree . -fi *.py src/`
  - Smart directory inclusion: shows parent folders even if they don't match the pattern directly
  - Caching optimization for large directory trees

### 2.0.1

- `-g`/`--git` now accepts only directories or `.git` directories, or directories containing a `.git` folder.
- `-gi`/`--gitignore` continues to accept either a `.gitignore` file or the containing directory.

### 2.0.0

#### Visual & Metadata

- `-p`/`--path-tree` | Path Tree: generates a view focused exclusively on the paths of files and directories.
- `-o [N]` | Text-Only Mode: generates the tree in plain text (without special characters). Accepts an optional parameter `N` to define the indentation (default: 2 spaces). Can't be used with `-n`.
- `-fs`/`--file-size` | File Sizes: toggle visibility of individual file sizes.
- `-ds`/`--dir-size` | Directory Sizes: display cumulative sizes for folders.
- [`-b`/`--big-first` | `-s`/`--small-first`] | Smart Sorting: order tree entries by size (descending/ascending).

#### Filtering & Data Structures

- `-dt`/`--dict-tree` | Dictionary format: output the tree structure as a native Python dictionary. Use `-dt N`/`--dict-tree N` for indentation (default 2). Format: {root: {tree...}}
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
