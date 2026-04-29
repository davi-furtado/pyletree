'''Entry point for Pyletree CLI.'''

import pathlib
import sys
import json

from .cli import parse_cmd_line_arguments
from .pyletree import FileTree


def main() -> None:
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir).resolve()

    if not root_dir.exists():
        print(f'Error: directory not found: {root_dir}', file=sys.stderr)
        sys.exit(1)

    if not root_dir.is_dir():
        print(f'Error: path is not a directory: {root_dir}', file=sys.stderr)
        sys.exit(1)

    try:
        sort_size = 'big' if args.big_first else ('small' if args.small_first else None)
        text_only = args.o is not None
        text_only_indent = args.o if args.o is not None else 2
        
        git_mode = args.git
        use_gitignore = args.gitignore
        ignore_patterns = args.ignore
        
        if git_mode is not False:
            use_gitignore = git_mode if git_mode else ['.']
            if ignore_patterns is None:
                ignore_patterns = ['.git']
            elif '.git' not in ignore_patterns:
                ignore_patterns.append('.git')
        elif use_gitignore is not False:
            use_gitignore = use_gitignore if use_gitignore else ['.']

        tree = FileTree(
            root_dir=root_dir,
            dir_only=args.dir_only,
            files_only=args.files_only,
            dirs_first=args.dirs_first,
            files_first=args.files_first,
            no_pipes=args.no_pipes,
            ignore=ignore_patterns,
            use_gitignore=use_gitignore,
            depth_level=args.depth_level,
            path_tree=args.path_tree,
            text_only=text_only,
            text_only_indent=text_only_indent,
            file_size=args.file_size,
            dir_size=args.dir_size,
            sort_size=sort_size,
            filter=args.filter,
            reverse=args.reverse,
        )

        if args.dict_tree is not None:
            indent = args.dict_tree if args.dict_tree > 0 else None
            print(json.dumps(tree.getDictTree(), indent=indent))
        else:
            for line in tree:
                print(line)

    except KeyboardInterrupt:
        print('\nOperation cancelled.', file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()