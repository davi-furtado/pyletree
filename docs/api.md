# Python API

Use `FileTree` to generate directory trees programmatically.

## Example

```python
from pyletree import FileTree

tree = FileTree()
print(tree)

for line in tree:
    print(line)
```

## Constructor

```python
FileTree(
    root_dir=".",
    *,
    dir_only=False,
    files_only=False,
    dirs_first=False,
    files_first=False,
    no_pipes=False,
    ignore=None,
    use_gitignore=False,
    depth_level=None,
    path_tree=False,
    backslashed_paths=False,
    text_only=False,
    text_only_indent=2,
    file_size=False,
    dir_size=False,
    sort_size=None,
    filter=None,
    reverse=False,
)
```

### Main parameters

| Parameter | Description |
| --- | --- |
| `root_dir` | Directory to scan. Defaults to the current directory. |
| `dir_only` / `files_only` | Restrict output to directories or files. |
| `dirs_first` / `files_first` | Put one entry type before the other. |
| `ignore` | Gitignore-style patterns to exclude. |
| `filter` | Gitignore-style patterns to include. |
| `use_gitignore` | Read `.gitignore` rules from the root or supplied paths. |
| `depth_level` | Maximum depth to traverse. |
| `path_tree` | Display full paths instead of entry names. |
| `backslashed_paths` | Use Windows-style path separators. |
| `text_only` | Use plain indentation instead of tree characters. |
| `file_size` / `dir_size` | Display file or cumulative directory sizes. |
| `sort_size` | Sort by size using `"big"` or `"small"`. |
| `reverse` | Reverse the alphabetical or size-based order. |

## Methods

- `get_tree() -> str`: Return the formatted tree.
- `get_dict_tree() -> dict`: Return the tree as nested dictionaries.
- `get_path(pattern: str) -> list[Path]`: Find matching files and directories.
- `__str__() -> str`: Return the same output as `get_tree()`.
- Iteration yields one formatted tree line at a time.
