# API

Use the `FileTree` class programmatically to generate directory trees from Python.

## Example

```python
from pyletree import FileTree

tree = FileTree()
print(tree)

for line in tree:
    print(line)
```

## Parameters

- `root_dir: str | Path = '.'` Root directory path
- `dir_only: bool = False` Show directories only
- `files_only: bool = False` Show files only
- `dirs_first: bool = False` List directories before files
- `files_first: bool = False` List files before directories
- `no_pipes: bool = False` Remove vertical pipes between branches
- `ignore: list[str] | None = None` Gitignore-style patterns to ignore
- `filter: list[str] | None = None` Gitignore-style patterns to include only
- `use_gitignore: bool | str | Path | list[str | Path] = False` Respect `.gitignore` rules
- `depth_level: int | None = None` Limit tree depth
- `path_tree: bool = False` Display full paths instead of names
- `text_only: bool = False` Plain text mode
- `text_only_indent: int = 2` Indentation spaces for text-only mode
- `file_size: bool = False` Show individual file sizes
- `dir_size: bool = False` Show cumulative sizes for directories
- `sort_size: None | 'big' | 'small' = None` Sort by size
- `reverse: bool = False` Reverse alphabetical sort order

## Methods

### `get_tree() -> str`

Return the tree as a formatted string.

### `get_dict_tree() -> dict[str, Any]`

Return the tree as a nested dictionary.

### `get_path(pattern: str) -> list[Path]`

Search for files or directories matching a pattern.

### `dict(tree)`

`FileTree` supports mapping conversion via `keys()` and `__getitem__()`.

### Iteration

The class is iterable and yields one line of the tree at a time.

### String conversion

`str(tree)` returns the full tree.
