'''This module provides Pyletree main module.'''

from __future__ import annotations

import pathlib
import sys
from collections import deque
from fnmatch import fnmatch
from typing import Deque, List, Optional, Set, Any

import pathspec

PIPE = '│'
ELBOW = '└──'
TEE = '├──'
PIPE_PREFIX = '│   '
SPACE_PREFIX = '    '


def _format_size(size_val: Any) -> str:
    if isinstance(size_val, str):
        return size_val
    size = float(size_val)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            if unit == 'B':
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}".replace('.0 ', ' ')
        size /= 1024.0
    return f"{size:.1f} PB"


class FileTree:
    def __init__(
        self,
        root_dir: pathlib.Path | str = '.',
        *,
        dir_only: bool = False,
        files_only: bool = False,
        dirs_first: bool = False,
        files_first: bool = False,
        no_pipes: bool = False,
        ignore: Optional[List[str]] = None,
        use_gitignore: Any = False,
        depth_level: Optional[int] = None,
        path_tree: bool = False,
        text_only: bool = False,
        text_only_indent: int = 2,
        file_size: bool = False,
        dir_size: bool = False,
        sort_size: Optional[str] = None,
        filter: Optional[List[str]] = None,
        reverse: bool = False,
    ) -> None:
        if isinstance(root_dir, str):
            root_dir = pathlib.Path(root_dir)
            
        self._root_dir = root_dir.resolve()
        self._dir_only = dir_only
        self._files_only = files_only
        self._dirs_first = dirs_first
        self._files_first = files_first
        self._no_pipes = no_pipes
        self._ignore: Set[str] = set(ignore or [])
        self._depth_level = depth_level
        self._tree_deque: Deque[str] = deque()

        self._path_tree = path_tree
        self._text_only = text_only
        self._text_only_indent = text_only_indent
        self._file_size = file_size
        self._dir_size = dir_size
        self._sort_size = sort_size
        self._reverse = reverse

        self._size_cache = {}
        self._gitignore_list = []
        self._filter_cache = {}
        
        # Initialize spec variables
        if ignore:
            self._ignore_spec = pathspec.PathSpec.from_lines('gitwildmatch', ignore)
        else:
            self._ignore_spec = None
            
        if filter:
            self._filter_spec = pathspec.PathSpec.from_lines('gitwildmatch', filter)
        else:
            self._filter_spec = None

        if use_gitignore is not False:
            try:
                # Normalize to list
                if use_gitignore is True:
                    gis = [self._root_dir]
                elif isinstance(use_gitignore, (str, pathlib.Path)):
                    gis = [use_gitignore]
                else:
                    gis = use_gitignore

                for item in gis:
                    item_path = pathlib.Path(item).resolve()
                    if item_path.is_file():
                        gitignore_file = item_path
                        gitignore_dir = item_path.parent
                    else:
                        gitignore_file = item_path / '.gitignore'
                        gitignore_dir = item_path

                    if gitignore_file.exists():
                        patterns = gitignore_file.read_text().splitlines()
                        spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
                        self._gitignore_list.append((gitignore_dir, spec))
            except Exception as e:
                print(f'Warning: Error parsing gitignore rule: {e}', file=sys.stderr)

    def _get_size(self, path: pathlib.Path) -> int:
        if path in self._size_cache:
            return self._size_cache[path]
        try:
            if path.is_file() or path.is_symlink():
                size = path.stat().st_size
            elif path.is_dir():
                size = sum(self._get_size(p) for p in path.iterdir() if p.exists() and not p.is_symlink())
            else:
                size = 0
        except (PermissionError, FileNotFoundError, OSError):
            size = 0
        self._size_cache[path] = size
        return size

    @property
    def _tree(self) -> Deque[str]:
        if not hasattr(self, '_cached_tree'):
            self._cached_tree = self._build_tree()
        return self._cached_tree

    def getTree(self) -> str:
        return str(self)

    def getDictTree(self) -> dict:
        root_name = str(self._root_dir) if self._path_tree else (self._root_dir.name or str(self._root_dir))
        return {root_name: self._build_dict_tree(self._root_dir, 0)}
        
    def _build_dict_tree(self, directory: pathlib.Path, depth: int) -> dict:
        if self._depth_level is not None and depth >= self._depth_level:
             return {}
        entries = self._prepare_entries(directory)
        result = {}
        for entry in entries:
            name = str(entry) if self._path_tree else entry.name
            if entry.is_dir():
                result[name] = self._build_dict_tree(entry, depth + 1)
            else:
                result[name] = None
                if self._file_size:
                     result[name] = _format_size(self._get_size(entry))
        return result

    def getPath(self, pattern: str) -> List[pathlib.Path]:
        return self._find_paths(self._root_dir, pattern, 0)

    def _find_paths(self, directory: pathlib.Path, pattern: str, depth: int) -> List[pathlib.Path]:
        if self._depth_level is not None and depth >= self._depth_level:
             return []
        entries = self._prepare_entries(directory)
        found = []
        for entry in entries:
            rel_str = entry.relative_to(self._root_dir).as_posix()
            if entry.name == pattern or fnmatch(rel_str, pattern) or entry.match(pattern):
                 found.append(entry.resolve())
            if entry.is_dir():
                 found.extend(self._find_paths(entry, pattern, depth + 1))
        return found

    def keys(self):
        return self.getDictTree().keys()

    def __getitem__(self, key):
        return self.getDictTree()[key]

    def __iter__(self):
        return iter(self._tree)

    def __str__(self):
        return "\n".join(self._tree)

    def _build_tree(self) -> Deque[str]:
        root_name = str(self._root_dir) if self._path_tree else (self._root_dir.name or str(self._root_dir))
        root_display = f'{root_name}/'
        if self._dir_size:
             root_display += f" ({_format_size(self._get_size(self._root_dir))})"

        self._tree_deque.append(root_display)

        if not self._no_pipes and not self._text_only:
            entries = self._prepare_entries(self._root_dir)
            if entries:
                self._tree_deque.append(PIPE)

        self._tree_body(self._root_dir, prefix='', depth=0)
        return self._tree_deque

    def _tree_body(
        self,
        directory: pathlib.Path,
        prefix: str,
        depth: int,
    ) -> None:
        if self._depth_level is not None and depth >= self._depth_level:
            return

        entries = self._prepare_entries(directory)
        if not entries:
            return

        last_index = len(entries) - 1

        for index, entry in enumerate(entries):
            is_last = index == last_index
            
            if self._text_only:
                connector = " " * self._text_only_indent
                full_prefix = prefix + connector
            else:
                connector = ELBOW if is_last else TEE
                full_prefix = f'{prefix}{connector} '
            
            entry_name = str(entry) if self._path_tree else entry.name
            display_name = f'{entry_name}{"/" if entry.is_dir() else ""}'
            
            if entry.is_dir() and self._dir_size:
                 display_name += f" ({_format_size(self._get_size(entry))})"
            elif entry.is_file() and self._file_size:
                 display_name += f" ({_format_size(self._get_size(entry))})"

            self._tree_deque.append(f'{full_prefix}{display_name}')

            if entry.is_dir():
                if self._text_only:
                    new_prefix = prefix + " " * self._text_only_indent
                else:
                    new_prefix = prefix + (SPACE_PREFIX if is_last else PIPE_PREFIX)
                self._tree_body(entry, new_prefix, depth + 1)

                if not self._no_pipes and not self._text_only and not is_last:
                    self._tree_deque.append(prefix + PIPE)

    def _prepare_entries(self, directory: pathlib.Path) -> List[pathlib.Path]:
        try:
            entries = sorted(directory.iterdir(), key=lambda e: e.name.lower(), reverse=self._reverse)
        except PermissionError:
            return []

        entries = [e for e in entries if not self._is_ignored(e)]

        if self._dir_only:
            entries = [e for e in entries if e.is_dir()]
        elif self._files_only:
            entries = [e for e in entries if e.is_file()]

        if self._sort_size == 'big':
             entries.sort(key=lambda e: self._get_size(e), reverse=True)
        elif self._sort_size == 'small':
             entries.sort(key=lambda e: self._get_size(e), reverse=False)
        else:
             if self._dirs_first:
                 entries.sort(key=lambda e: e.is_file())
             elif self._files_first:
                 entries.sort(key=lambda e: e.is_dir())

        return entries

    def _is_ignored(self, entry: pathlib.Path) -> bool:
        rel = entry.relative_to(self._root_dir)
        rel_str_root = rel.as_posix()
        is_dir = entry.is_dir()

        def check_spec(spec, path_str):
            if spec.match_file(path_str):
                return True
            if is_dir and spec.match_file(path_str + '/'):
                return True
            return False

        if self._ignore_spec and check_spec(self._ignore_spec, rel_str_root):
            return True

        if self._filter_spec:
            if entry.is_file():
                if not check_spec(self._filter_spec, rel_str_root):
                    return True
            else:
                if not check_spec(self._filter_spec, rel_str_root) and not self._has_filtered_descendant(entry):
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

    def _has_filtered_descendant(self, directory: pathlib.Path) -> bool:
        if directory in self._filter_cache:
            return self._filter_cache[directory]

        matched = False
        try:
            for entry in directory.iterdir():
                if self._filter_spec is None:
                    matched = True
                    break

                entry_resolved = entry.resolve()
                rel = entry_resolved.relative_to(self._root_dir).as_posix()
                if self._filter_spec.match_file(rel) or (entry_resolved.is_dir() and self._filter_spec.match_file(rel + '/')):
                    matched = True
                    break

                if entry_resolved.is_dir() and self._has_filtered_descendant(entry_resolved):
                    matched = True
                    break
        except (PermissionError, FileNotFoundError, OSError):
            matched = False

        self._filter_cache[directory] = matched
        return matched

        return False