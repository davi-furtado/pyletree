# Copilot Instructions for PyleTree

## Python Conventions

### Naming & Style
- **Module names**: Lowercase with underscores (e.g., `pyletree.py`, `__main__.py`)
- **Class names**: PascalCase (e.g., `FileTree`)
- **Function/method names**: Snake_case (e.g., `get_tree()`, `get_dict_tree()`)
- **Private attributes/methods**: Prefix with `_` (e.g., `_tree_deque`, `_size_cache`)
- **Constants**: UPPERCASE with underscores (rare in this codebase)

### Public API
- All public attributes of `FileTree` are documented (user-configurable parameters)
- Only export `FileTree` and `__version__` in `__init__.py`
- Methods should be snake_case and align with common patterns: `get_*()`, `is_*()`, `__str__()`, iteration protocol

### Docstrings
- **Format**: Google style (enforced by `mkdocstrings[python]`)
- **All public methods**: Must have docstrings
- **Public classes**: Must document purpose, parameters, and usage example
- **Private internals**: Brief docstrings sufficient; style consistency preferred

Example:
```python
def get_path(self, pattern: str) -> list[Path]:
    """Search for files or directories matching a glob pattern.
    
    Args:
        pattern: Glob pattern (e.g., '*.py', 'src/*.py').
    
    Returns:
        List of resolved Path objects matching the pattern.
    """
```

### Type Hints
- Use type hints for all function signatures (Python 3.8+)
- For optional types, use `Type | None` (Python 3.10+) or `Optional[Type]`
- Use `list[str]`, `dict[str, Any]` modern syntax (Python 3.9+)

### Error Handling
- Prefer `pathlib.Path` over string paths for robustness
- Use `pathspec` library for gitignore-pattern matching (already a dependency)
- Validate user input early (CLI args, FileTree params)
- Raise `ValueError` or `TypeError` with clear messages for invalid input

### Imports
- Standard library imports first, then third-party, then local (PEP 8)
- Avoid circular imports; use relative imports sparingly (package is small)
- `from pathlib import Path` is standard across the codebase

---

## CLI Conventions

### Argument Structure
- **Short form**: Single dash (`-n`, `-d`, `-fs`)
- **Long form**: Double dash (`--no-pipes`, `--dirs-first`, `--file-size`)
- **Positional**: `[ROOT_DIR]` (optional, defaults to `'.'`)
- **Groups**:
  - General: `-h`, `-v`
  - Modes: `-do`/`-fo` (dir/files only)
  - Ordering: `-d`/`-f`/`-r` (dirs/files first, reverse)
  - Size: `-fs`, `-ds`, `-b`, `-s`
  - Display: `-n`, `-p`, `-bs`, `-t`
  - Ignoring: `-git`, `-g`, `-i`, `-fi`
  - Depth: `-dl`
  - Output: `-dt`

### Help Text
- Keep descriptions concise (< 60 chars)
- Use lowercase for option descriptions
- Group related options in help output
- Always provide examples (see README CLI examples)

### Mutual Exclusivity
- Size sorting (`-b`/`-s`) is mutually exclusive with alpha sort (`-d`/`-f`)
- Implement with `argparse` mutually exclusive groups if needed

---

## Python API Conventions

### FileTree Class Parameters
All parameters are **public attributes** (accessible as `tree.param_name`):

- `root_dir: str | Path = '.'`
- `dir_only: bool = False`
- `files_only: bool = False`
- `dirs_first: bool = False`
- `files_first: bool = False`
- `no_pipes: bool = False`
- `ignore: list[str] | None = None`
- `filter: list[str] | None = None`
- `use_gitignore: bool | str | Path | list = False`
- `depth_level: int | None = None`
- `path_tree: bool = False`
- `backslashed_paths: bool = False` (Windows path support)
- `text_only: bool = False`
- `text_only_indent: int = 2`
- `file_size: bool = False`
- `dir_size: bool = False`
- `sort_size: str | None = None` ('big' or 'small')
- `reverse: bool = False`

### FileTree Methods
- `get_tree() -> str` — Returns tree as formatted string
- `get_dict_tree() -> dict` — Returns tree as nested dictionary
- `get_path(pattern: str) -> list[Path]` — Search for matching files
- `__str__()` → calls `get_tree()` for direct printing
- `__iter__()` — Yields one line per iteration
- `keys()` and `__getitem__()` — Support `dict()` conversion

### Output Formats
- **Dictionary format** (`-dt N`): `{root: {nested_dict}}` with `N` spaces indentation
- **Path tree** (`-p`): Absolute paths instead of relative names
- **Text-only** (`-t N`): Plain text with `N`-space indents, no special characters
- **File size units**: Bytes (B), Kilobytes (KB), Megabytes (MB)

---

## Testing Conventions

**Current Status**: No automated test suite is configured.

When tests are added:
- Use `pytest` as the test runner
- Place tests in `tests/` directory at root
- Test file naming: `test_*.py` or `*_test.py`
- Test discovery: `pytest tests/`
- Coverage: Aim for 80%+ on core logic

Typical test structure:
```python
# tests/test_pyletree.py
import pytest
from pathlib import Path
from pyletree import FileTree

def test_basic_tree_generation(tmp_path):
    """Test that FileTree generates a valid tree."""
    # Setup
    (tmp_path / "file.txt").touch()
    (tmp_path / "subdir").mkdir()
    
    # Execute
    tree = FileTree(str(tmp_path))
    output = tree.get_tree()
    
    # Assert
    assert "file.txt" in output
    assert "subdir" in output
```

---

## Code Style Notes

### Formatting
- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces (never tabs)
- **Blank lines**: 2 between top-level definitions, 1 between methods
- **Imports**: Sorted, organized by type (stdlib, third-party, local)

### Linting
No linter is currently configured. Future options:
- **Ruff**: Fast, modern (Rust-based) linter for Python
- **Black**: Opinionated code formatter
- **MyPy**: Static type checker

### When Adding Code
- Follow existing patterns in `pyletree.py` and `cli.py`
- Use `pathlib.Path` for path operations (not `os.path`)
- Use `pathspec` for pattern matching (already available)
- Test both Windows (`\`) and Unix (`/`) path separators when relevant

---

## Maintenance Matrix

This matrix documents which files must be updated when specific components change.

### When Modifying Core Logic (`src/pyletree/pyletree.py`)

| Change Type | Files to Update | Reason |
|-------------|-----------------|--------|
| Add/modify `FileTree` parameter | • `README.md` (Python API Parameters table)<br>• `docs/api.md`<br>• `src/pyletree/__init__.py` docstring | Users need to know new parameter exists |
| Add/modify method (public) | • `docs/api.md` (Methods section)<br>• `README.md` (if significant) | Public API documentation must stay in sync |
| Add/modify return type | • `docs/api.md`<br>• `README.md` (dict-tree format) | Type signature changes affect users |
| Modify output format | • `README.md` (Sample Output section)<br>• `docs/usage.md` | Examples must match actual behavior |
| Fix sorting/filtering logic | • `docs/usage.md` (if behavior changes) | Examples may need updating |

### When Modifying CLI (`src/pyletree/cli.py`)

| Change Type | Files to Update | Reason |
|-------------|-----------------|--------|
| Add/remove CLI option | • `README.md` (Options section and Examples)<br>• `docs/usage.md` (Examples)<br>• Help text in cli.py | CLI is the primary user interface |
| Rename option | • `README.md` (all references)<br>• `docs/usage.md` (all examples)<br>• `AGENTS.md` | Backward compatibility; users reference docs |
| Change default behavior | • `README.md` (General section)<br>• `README.md` (Examples)<br>• `docs/usage.md` | Breaking change requires documentation |
| Fix argument parsing | Usually no doc changes (internal fix) | Unless behavior changes visibly |

### When Modifying Dependencies

| Change Type | Files to Update | Reason |
|-------------|-----------------|--------|
| Add/remove dependency | • `pyproject.toml` (in `dependencies` group)<br>• `README.md` (if notable)<br>• Commit `uv.lock` | Lockfile tracks exact versions for reproducibility |
| Add/remove doc dependency | • `pyproject.toml` (in `docs` group)<br>• Commit `uv.lock` | Doc build reproducibility |
| Update Python version requirement | • `pyproject.toml` (`requires-python`)<br>• `README.md` (Installation section)<br>• `.github/workflows/*.yml` (test matrix) | Users need to know compatibility |

### When Adding/Updating Documentation

| File | Depends On | Update When |
|------|-----------|-------------|
| `README.md` | Core logic, CLI | Any API change, option added, example fails |
| `docs/usage.md` | CLI behavior | Option added, example no longer works |
| `docs/api.md` | `FileTree` class | Parameter added, method added/removed, return type changes |
| `docs/index.md` | Project status | Major releases, significant feature additions |
| `mkdocs.yml` | Docs structure | Adding new docs pages, changing site config |

### When Updating Release Process

| File | Depends On | Update When |
|------|-----------|-------------|
| `pyproject.toml` | Version numbers | Before every release (version bump required for CI trigger) |
| `.github/workflows/release.yml` | Build/publish process | Changing build tool, PyPI auth, or release steps |
| `.github/workflows/docs-deploy.yml` | Docs build | Changing mkdocs config, dependencies, or deployment target |

### When Adding Tests (Future)

| File | Depends On | Update When |
|------|-----------|-------------|
| `tests/test_pyletree.py` | Core logic | New feature, bug fix, refactor |
| `.github/workflows/test.yml` | Test runner config | Adding test framework, changing Python versions |
| `README.md` | Test instructions | Test setup changes (how to run locally) |

---

## Dependency Graph

**Direct Dependencies**:
- `pathspec` — Used in `src/pyletree/pyletree.py` for gitignore-pattern matching

**CLI → Core Logic Flow**:
- `cli.py` `main()` → parses args → instantiates `FileTree()` → calls `tree.get_tree()` or `tree.get_dict_tree()` → prints output

**API → Core Logic Flow**:
- User imports `FileTree` from `__init__.py` → creates instance with parameters → calls methods on instance

**Docs → Code Coupling**:
- Examples in `README.md` and `docs/usage.md` reference exact CLI syntax
- `docs/api.md` documents `FileTree` parameters and methods
- Sample outputs must match actual behavior

---

## Conventions Mined from PR History

*Note: As a new repository, there is limited PR history to mine. These conventions are established from the codebase.*

- **Backward compatibility**: Public API changes (parameter, method) are rare; prefer additive changes
- **Documentation-first**: Complex features like filtering include comprehensive README examples
- **Multi-interface support**: Features must work via both CLI and Python API
- **Cross-platform paths**: Windows (`\`) and Unix (`/`) support is expected
