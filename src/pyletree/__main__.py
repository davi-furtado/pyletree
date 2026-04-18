'''Entry point for Pyletree CLI.'''

import pathlib
import sys

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
        tree = FileTree(
            root_dir=root_dir,
            dir_only=args.dir_only,
            files_only=args.files_only,
            dirs_first=args.dirs_first,
            files_first=args.files_first,
            no_pipes=args.no_pipes,
            ignore=args.ignore,
            use_gitignore=args.gitignore,
            depth_level=args.depth_level,
        )

        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write('```\n')
                f.write(str(tree) + '\n')
                f.write('```\n')
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