# Changelog

All notable changes to PyleTree are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.7.0] - 2025-12-15

### Added
- **Windows-style paths support** (`-bs` / `--backslash` CLI option)
  - Adds `backslashed_paths` parameter to Python API
  - Displays paths with `\` separators on Windows

### Changed
- Improved documentation on path handling

### Fixed
- Path separator handling improvements

## [2.6.4] - 2025-11-20

### Changed
- Docs website styling improvements
- Branding: "Pyletree" → "PyleTree" in docstrings

## [2.6.3] - 2025-11-10

### Changed
- Migrated manual caching to `functools.lru_cache` for better performance

## [2.6.2] - 2025-10-30

### Changed
- Internal code improvements and optimizations

## [2.6.1] - 2025-10-15

### Fixed
- Various bug fixes and minor improvements

## [2.6.0] - 2025-09-30

### Added
- `--text-only` as long-form alias for `-t` option
- Optional indentation parameter `N` to `-dt` / `--dict-tree` (default: 2, 0 for compact)

### Changed
- **Breaking CLI change**: Swapped short aliases for git and gitignore modes
  - `-git` now maps to `--git` (was `-gi`)
  - `-g` now maps to `--gitignore` (was `-gi`)
- Updated documentation to reflect new CLI aliases

## [2.5.0] - 2025-09-15

### Added
- Comprehensive docstrings across `FileTree` class and CLI entry points
- Improved type annotations throughout codebase

### Changed
- **API update**: Public method names now use snake_case (e.g., `get_tree()`, `get_dict_tree()`)
- Public attributes are now explicitly documented

## [2.4.0] - 2025-09-01

### Changed
- **Breaking API change**: `FileTree` instance attributes are now **public**
  - All user-configured parameters are accessible without `_` prefix
  - Example: `tree.root_dir`, `tree.dir_only`, `tree.depth_level`
  - Internal state remains private with `_` prefix

## [2.3.1] - 2025-08-20

### Changed
- README improvements
- Code quality enhancements

## [2.3.0] - 2025-08-10

### Changed
- **API simplification**: `-di` / `--dict-indent` merged into `-dt` / `--dict-tree`
  - Usage: `pyletree . -dt 4` (4-space indentation)
  - Usage: `pyletree . -dt 0` (compact, no indentation)

## [2.2.0] - 2025-07-25

### Added
- Enhanced dictionary output format (`-dt` / `--dict-tree`)
  - Now returns `{root: {tree...}}` structure
  - Supports configurable indentation via `-dt N`

### Changed
- Improved output format for programmatic use

## [2.1.0] - 2025-07-10

### Added
- **Include-only filter** (`-fi` / `--filter` option)
  - Display only files/directories matching gitignore-style patterns
  - Smart directory inclusion: shows parent folders even if they don't match
  - Caching optimization for large directory trees
  - Example: `pyletree . -fi *.py src/`

## [2.0.1] - 2025-06-20

### Fixed
- Stricter validation for `-g` / `--git` and `-gi` / `--gitignore` options

## [2.0.0] - 2025-06-10

### Added
- **Path tree** (`-p` / `--path-tree`): Display full paths instead of names
- **Text-only mode** (`-t [N]` / `--text-only`): Plain text output with optional indentation
- **File sizes** (`-fs` / `--file-size`): Display individual file sizes
- **Directory sizes** (`-ds` / `--dir-size`): Display cumulative folder sizes
- **Size-based sorting** (`-b` / `--big-first`, `-s` / `--small-first`)
- **Dictionary output** (`-dt` / `--dict-tree`): Tree as JSON dictionary
- **File path search** (`FileTree.get_path(pattern)`): Find files by pattern
- **Global file filter**: Exclude/include files by patterns or extensions

### Changed
- Major output format expansion
- Enhanced Python API with new methods

## [1.1.0] - 2025-05-15

### Added
- `FileTree` class for programmatic usage in Python scripts

### Removed
- `-o` / `--output-file` option (replaced by programmatic API)

## [1.0.0] - 2025-05-01

### Added
- Initial release
- Basic CLI for generating directory tree diagrams
- `.gitignore` support
- Custom ignore patterns
- Depth limiting
- Flexible sorting options
- Reverse sort order
