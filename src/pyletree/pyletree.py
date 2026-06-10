"""This module provides Pyletree main module."""

from __future__ import annotations

import sys
from collections import deque
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Deque, Iterator, KeysView, List, Literal, Optional, Set

from pathspec import PathSpec

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "
import locale


def _format_size(size_val: int | float | str) -> str:
    """Format a size value as a human-readable string.

    Accepts an integer, float, or already formatted string.
    Returns a readable unit string such as "1.2 KB" or "3 B".
    """
    if isinstance(size_val, str):
        return size_val
    size = float(size_val) if isinstance(size_val, int) else size_val
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}".replace(".0 ", " ")
        size /= 1024.0
    return f"{size:.1f} PB"


class FileTree:
    """Generate a filesystem tree representation for a root directory.

    The tree supports filtering, ignoring patterns, sorting, and
    both textual and dictionary output.
    """

    def __init__(
        self,
        root_dir: Path | str = ".",
        *,
        dir_only: bool = False,
        files_only: bool = False,
        dirs_first: bool = False,
        files_first: bool = False,
        no_pipes: bool = False,
        ignore: Optional[List[str]] = None,
        use_gitignore: bool | str | Path | list[str | Path] = False,
        depth_level: Optional[int] = None,
        path_tree: bool = False,
        text_only: bool = False,
        text_only_indent: int = 2,
        file_size: bool = False,
        dir_size: bool = False,
        sort_size: None | Literal["big", "small"] = None,
        filter: Optional[List[str]] = None,
        filter_patterns: Optional[List[str]] = None,
        reverse: bool = False,
    ) -> None:
        """Initialize a FileTree with directory traversal options.

        Parameters are the same as the CLI options and control how the
        directory tree is generated, filtered, sorted, and formatted.
        """
        if isinstance(root_dir, str):
            root_dir = Path(root_dir)

        self.root_dir = root_dir.resolve()
        self.dir_only = dir_only
        self.files_only = files_only
        self.dirs_first = dirs_first
        self.files_first = files_first
        self.no_pipes = no_pipes
        self.ignore: Set[str] = set(ignore or [])
        self.depth_level = depth_level
        self._tree_deque: Deque[str] = deque()

        self.path_tree = path_tree
        self.text_only = text_only
        self.text_only_indent = text_only_indent
        self.file_size = file_size
        self.dir_size = dir_size
        self.sort_size = sort_size
        self.reverse = reverse

        self._size_cache = {}
        self._gitignore_list = []
        self._filter_cache = {}

        self.filter = filter if filter is not None else filter_patterns

        # Initialize spec variables
        if ignore:
            self._ignore_spec = PathSpec.from_lines("gitwildmatch", ignore)
        else:
            self._ignore_spec = None

        if self.filter:
            self._filter_spec = PathSpec.from_lines("gitwildmatch", self.filter)
        else:
            self._filter_spec = None

        if use_gitignore is not False:
            try:
                # Normalize to list
                if use_gitignore is True:
                    gis = [self.root_dir]
                elif isinstance(use_gitignore, (str, Path)):
                    gis = [use_gitignore]
                else:
                    gis = use_gitignore

                for item in gis:
                    item_path = Path(item).resolve()
                    if item_path.is_file():
                        gitignore_file = item_path
                        gitignore_dir = item_path.parent
                    else:
                        gitignore_file = item_path / ".gitignore"
                        gitignore_dir = item_path

                    if gitignore_file.exists():
                        patterns = gitignore_file.read_text().splitlines()
                        spec = PathSpec.from_lines("gitwildmatch", patterns)
                        self._gitignore_list.append((gitignore_dir, spec))
            except Exception as e:
                print(
                    f"Warning: Error parsing gitignore rule: {e}",
                    file=sys.stderr,
                )

    def _get_size(self, path: Path) -> int:
        """Return the cached size for a path.

        Compute directories recursively. Files and symlinks return their
        file size. Directories return the cumulative size of their contents,
        excluding symlinked children.
        """
        if path in self._size_cache:
            return self._size_cache[path]
        try:
            if path.is_file() or path.is_symlink():
                size = path.stat().st_size
            elif path.is_dir():
                size = sum(
                    self._get_size(p)
                    for p in path.iterdir()
                    if p.exists() and not p.is_symlink()
                )
            else:
                size = 0
        except (PermissionError, FileNotFoundError, OSError):
            size = 0
        self._size_cache[path] = size
        return size

    @property
    def _tree(self) -> Deque[str]:
        """Return the cached list of tree lines, building it if needed."""
        if not hasattr(self, "_cached_tree"):
            self._cached_tree = self._build_tree()
        return self._cached_tree

    def get_tree(self) -> str:
        """Return the generated tree as a single newline-separated string."""
        return str(self)

    def get_dict_tree(self) -> dict[str, Any]:
        """Return the generated tree as a nested dictionary."""
        root_name = (
            str(self.root_dir)
            if self.path_tree
            else (self.root_dir.name or str(self.root_dir))
        )
        return {root_name: self._build_dict_tree(self.root_dir, 0)}

    def _build_dict_tree(self, directory: Path, depth: int) -> Any:
        """Build the nested dictionary or list representation of a directory tree."""
        if self.depth_level is not None and depth >= self.depth_level:
            return [] if not self.file_size else {}
        entries = self._prepare_entries(directory)
        if not self.file_size:
            result_list: list[Any] = []
            for entry in entries:
                name = str(entry) if self.path_tree else entry.name
                if entry.is_dir():
                    result_list.append({name: self._build_dict_tree(entry, depth + 1)})
                else:
                    result_list.append(name)
            return result_list

        result_dict: dict[str, Any] = {}
        for entry in entries:
            name = str(entry) if self.path_tree else entry.name
            if entry.is_dir():
                result_dict[name] = self._build_dict_tree(entry, depth + 1)
            else:
                result_dict[name] = _format_size(self._get_size(entry))
        return result_dict

    def get_path(self, pattern: str) -> List[Path]:
        """Return resolved paths matching the given pattern in the tree."""
        return self._find_paths(self.root_dir, pattern, 0)

    def _find_paths(self, directory: Path, pattern: str, depth: int) -> List[Path]:
        """Recursively search the tree for entries that match the pattern."""
        if self.depth_level is not None and depth >= self.depth_level:
            return []
        entries = self._prepare_entries(directory)
        found = []
        for entry in entries:
            rel_str = entry.relative_to(self.root_dir).as_posix()
            if (
                entry.name == pattern
                or fnmatch(rel_str, pattern)
                or entry.match(pattern)
            ):
                found.append(entry.resolve())
            if entry.is_dir():
                found.extend(self._find_paths(entry, pattern, depth + 1))
        return found

    def keys(self) -> KeysView[str]:
        """Return the keys of the dictionary tree for dict() conversion."""
        return self.get_dict_tree().keys()

    def __getitem__(self, key: str) -> Any:
        """Return a key lookup from the dictionary tree representation."""
        return self.get_dict_tree()[key]

    def __iter__(self) -> Iterator[str]:
        """Iterate over the tree as a mapping of the dict tree."""
        # Iterate over the generated tree lines so `for line in tree:`
        # yields formatted tree lines for CLI printing.
        return iter(self._tree)

    def __str__(self):
        """Return the full tree as a newline-separated string."""
        return "\n".join(self._tree)

    def _build_tree(self) -> Deque[str]:
        """Build the internal deque of tree lines for the root directory."""
        root_name = (
            str(self.root_dir)
            if self.path_tree
            else (self.root_dir.name or str(self.root_dir))
        )
        root_display = f"{root_name}/"
        if self.dir_size:
            root_display += f" ({_format_size(self._get_size(self.root_dir))})"

        self._tree_deque.append(root_display)

        if not self.no_pipes and not self.text_only:
            entries = self._prepare_entries(self.root_dir)
            if entries:
                self._tree_deque.append(PIPE)

        self._tree_body(self.root_dir, prefix="", depth=0)
        return self._tree_deque

    def _tree_body(
        self,
        directory: Path,
        prefix: str,
        depth: int,
    ) -> None:
        """Recursively append formatted tree lines below a directory."""
        if self.depth_level is not None and depth >= self.depth_level:
            return

        entries = self._prepare_entries(directory)
        if not entries:
            return

        last_index = len(entries) - 1

        for index, entry in enumerate(entries):
            is_last = index == last_index

            if self.text_only:
                connector = " " * self.text_only_indent
                full_prefix = prefix + connector
            else:
                connector = ELBOW if is_last else TEE
                full_prefix = f"{prefix}{connector} "

            entry_name = str(entry) if self.path_tree else entry.name
            display_name = f'{entry_name}{"/" if entry.is_dir() else ""}'

            if entry.is_dir() and self.dir_size:
                display_name += f" ({_format_size(self._get_size(entry))})"
            elif entry.is_file() and self.file_size:
                display_name += f" ({_format_size(self._get_size(entry))})"

            self._tree_deque.append(f"{full_prefix}{display_name}")

            if entry.is_dir():
                if self.text_only:
                    new_prefix = prefix + " " * self.text_only_indent
                else:
                    new_prefix = prefix + (SPACE_PREFIX if is_last else PIPE_PREFIX)
                self._tree_body(entry, new_prefix, depth + 1)

                if not self.no_pipes and not self.text_only and not is_last:
                    self._tree_deque.append(prefix + PIPE)

    def _prepare_entries(self, directory: Path) -> List[Path]:
        """Prepare, sort, and filter directory entries before rendering."""
        try:
            entries = sorted(
                directory.iterdir(),
                key=lambda e: e.name.lower(),
                reverse=self.reverse,
            )
        except PermissionError:
            return []

        entries = [e for e in entries if not self._is_ignored(e)]

        if self.dir_only:
            entries = [e for e in entries if e.is_dir()]
        elif self.files_only:
            entries = [e for e in entries if e.is_file()]

        if self.sort_size == "big":
            entries.sort(key=lambda e: self._get_size(e), reverse=True)
        elif self.sort_size == "small":
            entries.sort(key=lambda e: self._get_size(e), reverse=False)
        else:
            if self.dirs_first:
                entries.sort(key=lambda e: e.is_file())
            elif self.files_first:
                entries.sort(key=lambda e: e.is_dir())

        return entries

    def _is_ignored(self, entry: Path) -> bool:
        """Return True when an entry is excluded by ignore or filter rules."""
        rel = entry.relative_to(self.root_dir)
        rel_str_root = rel.as_posix()
        is_dir = entry.is_dir()

        def check_spec(spec, path_str):
            if spec.match_file(path_str):
                return True
            if is_dir and spec.match_file(path_str + "/"):
                return True
            return False

        if self._ignore_spec and check_spec(self._ignore_spec, rel_str_root):
            return True

        if self._filter_spec:
            if entry.is_file():
                if not check_spec(self._filter_spec, rel_str_root):
                    return True
            else:
                if not check_spec(
                    self._filter_spec, rel_str_root
                ) and not self._has_filtered_descendant(entry):
                    return True

        for gitignore_dir, spec in self._gitignore_list:
            try:
                rel_git = entry.relative_to(gitignore_dir)
                rel_git_str = rel_git.as_posix()

                if check_spec(spec, rel_git_str):
                    return True
            except ValueError:
                pass

        return False

    def _has_filtered_descendant(self, directory: Path) -> bool:
        """Return True if the directory contains any matching entry."""
        if directory in self._filter_cache:
            return self._filter_cache[directory]

        matched = False
        try:
            for entry in directory.iterdir():
                if self._filter_spec is None:
                    matched = True
                    break

                entry_resolved = entry.resolve()
                rel = entry_resolved.relative_to(self.root_dir).as_posix()
                if self._filter_spec.match_file(rel) or (
                    entry_resolved.is_dir() and self._filter_spec.match_file(rel + "/")
                ):
                    matched = True
                    break

                if entry_resolved.is_dir() and self._has_filtered_descendant(
                    entry_resolved
                ):
                    matched = True
                    break
        except (PermissionError, FileNotFoundError, OSError):
            matched = False

        self._filter_cache[directory] = matched
        return matched


# Adjust drawing glyphs when the current stdout encoding cannot encode
# the Unicode box-drawing characters (common on Windows cp1252 terminals).
try:
    _enc = sys.stdout.encoding or locale.getpreferredencoding(False) or "utf-8"
except Exception:
    _enc = "utf-8"


def _encodes(s: str, enc: str) -> bool:
    try:
        s.encode(enc)
        return True
    except Exception:
        return False


if not _encodes(PIPE, _enc):
    PIPE = "|"
    ELBOW = "+--"
    TEE = "|--"
    PIPE_PREFIX = "|   "
    SPACE_PREFIX = "    "
