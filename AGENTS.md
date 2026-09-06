# PyleTree Repository Guide

## Project Overview

**PyleTree** is a lightweight, fast Python CLI tool and library for generating directory tree diagrams. It combines a user-friendly command-line interface with a comprehensive Python API, enabling both CLI-driven workflows and programmatic integration into Python scripts.

- **Primary Language**: Python (3.8+)
- **Build System**: UV (modern, fast Python build tool)
- **Current Version**: 2.7.0
- **License**: MIT
- **Primary Use**: CLI tool + Python library
- **Target Users**: Developers, DevOps engineers, documentation creators

## Repository Structure

```
pyletree/
├── src/pyletree/           # Main package source
│   ├── __init__.py         # Public API exports
│   ├── __main__.py         # CLI entry point
│   ├── cli.py              # CLI argument parsing and handlers
│   └── pyletree.py         # Core FileTree class and logic
├── docs/                   # Documentation site (Zensical)
│   ├── index.md            # Home page
│   ├── usage.md            # CLI usage guide
│   └── api.md              # Python API reference
├── .github/
│   ├── workflows/
│   │   ├── release.yml     # PyPI release automation
│   │   └── docs.yml        # Docs deployment
│   └── agents/             # Custom Copilot agents
├── pyproject.toml          # UV project config and dependencies
├── zensical.toml           # Docs site configuration
├── uv.lock                 # Dependency lock file
└── README.md               # Main readme
```

## Tech Stack

| Component                | Technology   | Notes                                      |
| ------------------------ | ------------ | ------------------------------------------ |
| **Language**             | Python 3.8+  | Broad compatibility for widespread use     |
| **Build**                | UV           | Modern, fast Python package build tool     |
| **Dependencies**         | `pathspec`   | Gitignore-style pattern matching           |
| **Docs**                 | Zensical     | Auto-deployed on push to main              |
| **Package Distribution** | PyPI         | Automated release workflow on version bump |
| **Docs Hosting**         | GitHub Pages | Deployed from `gh-pages` branch            |

## Build & Run

### Installation

```bash
# From PyPI
pip install pyletree

# From source
git clone https://github.com/davi-furtado/pyletree.git
cd pyletree
pip install -e .
```

### Development Setup

```bash
# Install with dev dependencies
uv sync --all-groups

# Run CLI from source
python -m pyletree [options]
```

### Building the Package

```bash
# Build wheel and sdist
uv build

# Publish to PyPI (automated via GitHub Actions on version bump)
```

### Building Documentation

```bash
# Install docs dependencies
uv sync --group docs

# Serve docs locally (live reload)
uv run zensical serve

# Build static docs
uv run zensical build
```

## Testing

**Current Status**: The repository does not have an automated test suite configured. All validation occurs through:

- Manual testing during development
- Integration testing via the live CLI
- Documentation examples (implicitly tested via docs site)

**To add tests in the future**: Create a `tests/` directory with a test runner (e.g., `pytest`) and add CI automation in `.github/workflows/test.yml`.

## Key Patterns and Conventions

### CLI Design

- **Entry Point**: `src/pyletree/__main__.py` → calls `cli.main()`
- **Argument Parsing**: `src/pyletree/cli.py` — uses argparse with custom help formatting
- **Option Groups**: CLI options are organized by category (General, Modes, Ordering, Size, Display, Ignoring, Depth, Output)
- **Naming**: Short (`-n`) and long (`--no-pipes`) forms for all flags

### Python API

- **Main Class**: `FileTree` in `src/pyletree/pyletree.py`
- **Public Attributes**: All user-configurable parameters are public (e.g., `tree.root_dir`, `tree.dir_only`)
- **Internal State**: Private attributes prefixed with `_` (e.g., `_tree_deque`, `_size_cache`)
- **Methods**: `get_tree()`, `get_dict_tree()`, `get_path()`, `__str__()`, iterable protocol
- **Exported**: Only `FileTree` and `__version__` in `__init__.py`

### Output Formats

The tool supports multiple output modes:

1. **Default tree** — ASCII art with pipes and branches
2. **No-pipes** (`-n`) — Simplified ASCII without vertical lines
3. **Text-only** (`-t`) — Plain indentation, no special characters
4. **Path tree** (`-p`) — Full paths instead of names
5. **Dictionary** (`-dt`) — Structured JSON output for programmatic use

### Filtering & Ignoring

- **Pattern Matching**: Uses `pathspec` library for gitignore-compatible patterns
- **Include Filters** (`-fi`/`--filter`) — Show only matching files (with parent dirs)
- **Exclude Patterns** (`-i`/`--ignore`) — Hide matching files/dirs
- **Gitignore Support** (`-g`/`--gitignore`) — Respect `.gitignore` rules

### Sorting & Sizing

- **Default Sort**: Alphabetical (case-sensitive)
- **Size-Based Sort**: `-b` (biggest first) or `-s` (smallest first)
- **Reverse**: `-r` inverts sort order
- **Mutually Exclusive**: Size sorting and alpha sort are mutually exclusive flags

## CI/CD

### Release Workflow (`.github/workflows/release.yml`)

- **Trigger**: Push to `main` that modifies `pyproject.toml` (version bump)
- **Steps**:
  1. Extract old and new version from `pyproject.toml`
  2. Check if version changed
  3. Create Git tag (`v<version>`)
  4. Build Python wheel and source dist
  5. Publish to PyPI via `gh-action-pypi-publish`
- **Permissions**: Requires `contents: write` for tagging

### Docs Deployment (`.github/workflows/docs.yml`)

- **Trigger**: Push to `main`
- **Steps**: Builds the Zensical site and deploys it to GitHub Pages
- **Result**: Accessible at https://davi-furtado.github.io/pyletree

### No PR/Test CI

- ⚠️ Currently no CI for PRs or branch pushes
- Consider adding: `test.yml` for unit tests, `lint.yml` for code quality

## Adding a New Feature

### Example: Add a New CLI Output Format

1. **Define the Feature**
   - Add a new parameter to `FileTree.__init__()` (e.g., `custom_format: bool = False`)
   - Document the expected output in `docs/usage.md`

2. **Implement Core Logic**
   - Modify `src/pyletree/pyletree.py` to handle the new format
   - Add a method (e.g., `get_custom_format()`) if output format differs significantly
   - Ensure the feature is optional and doesn't break existing behavior

3. **Expose via CLI**
   - Add argument to `src/pyletree/cli.py` with short (`-cf`) and long (`--custom-format`) forms
   - Pass the argument to `FileTree()` instantiation
   - Add help text in the appropriate CLI options group

4. **Update Exports**
   - If adding new public methods, document them in `__all__` exports
   - If adding new parameters to `FileTree`, list them in README.md Python API table

5. **Test Manually**
   - Run `python -m pyletree . -cf` to verify CLI works
   - Run Python API: `tree = FileTree(custom_format=True)` to verify programmatically
   - Update examples in `docs/usage.md` and `docs/api.md`

6. **Documentation**
   - Add CLI example to usage guide
   - Add Python API example to API reference
   - Update README if significant feature

7. **Version Bump & Release**
   - Update `version` in `pyproject.toml` (semver)
   - Commit and push to `main`
   - GitHub Actions automatically tags, builds, and publishes to PyPI

## Common Pitfalls

### When Adding Features

- **Don't break defaults**: New features should be optional and off by default
- **Test both CLI and API**: Changes must work via both interfaces
- **Update docs alongside code**: README, usage, and API docs drift quickly
- **Gitignore patterns**: Use `pathspec` for pattern matching; test with real `.gitignore` files

### When Fixing Bugs

- **Preserve public API**: `FileTree` parameters should not change without a major version bump
- **Size caching**: The `_size_cache` is used for performance; invalidate on parameter changes
- **Path handling**: Windows and Unix paths are handled differently; test both `/` and `\` separators

### When Releasing

- **Version must change**: CI only triggers on `pyproject.toml` changes to version
- **Lock file**: Commit `uv.lock` after dependency changes
- **PyPI token**: Requires `PYPI_API_TOKEN` secret configured in GitHub repo settings

## Documentation

The project uses **Zensical** for API documentation and usage guides. The site is built and deployed automatically to GitHub Pages on every push to `main`.

**Key Docs Files**:

- `docs/index.md` — Home/overview
- `docs/usage.md` — CLI usage and examples
- `docs/api.md` — Python API reference

To review/update docs:

1. Edit `.md` files in `docs/`
2. Run `uv run zensical serve` to preview locally
3. Commit and push to `main` — GitHub Actions auto-deploys
