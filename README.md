<div align="center">
  <h1 align="center">Pyletree</h1>
  
  <img src="https://img.shields.io/badge/python-3.8%2B-blue">
  <img src="https://img.shields.io/badge/license-MIT-green">
  <img src="https://img.shields.io/badge/version-1.0.0-orange">
</div>

<p align="right"><i>Pyletree is a simple and fast CLI tool to generate directory tree diagrams.</i></p>

## Installation

```bash
pip install pyletree
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

- `-d`, `--dir-only` Show directories only
- `-f`, `--files-only` Show files only

### Ordering

- `-df`, `--dirs-first` List directories before files
- `-ff`, `--files-first` List files before directories

> Alphabetical order is always applied as base sorting.

### Display

- `-n`, `--no-pipes` Remove vertical pipes between branches

### Ignoring

- `-i`, `--ignore PATTERN [PATTERN ...]` Ignore files/directories
- `-gi`, `--gitignore` Respect `.gitignore` rules

### Depth

- `-dl`, `--depth-level N` Limit depth

### Output

- `-o`, `--output-file FILE` Save output to file (Markdown format)

## Examples

Basic:

```bash
pyletree
```

Directories first:

```bash
pyletree . -df
```

Files only:

```bash
pyletree . -f
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

Save to file:

```bash
pyletree . -o tree.md
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

### 1.0.0

- Initial release

## Authors

Davi Reis Furtado

**Original RP Tree Author:**
Leodanis Pozo Ramos

## License

_Pyletree_ is distributed under the MIT license. See [LICENSE](LICENSE) for more information.
