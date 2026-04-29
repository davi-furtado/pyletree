'''This module provides the Pyletree CLI.'''

import argparse
import pathlib

from . import __version__


def parse_cmd_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='pyletree',
        description='Generate a directory tree',
        epilog='Thanks for using Pyletree!',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'Pyletree v{__version__}',
    )

    parser.add_argument(
        'root_dir',
        metavar='ROOT_DIR',
        nargs='?',
        default='.',
        help='root directory to generate the tree from',
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        '-do',
        '--dir-only',
        action='store_true',
        help='show directories only',
    )
    mode.add_argument(
        '-fo',
        '--files-only',
        action='store_true',
        help='show files only',
    )
    
    parser.add_argument(
        '-p',
        '--path-tree',
        action='store_true',
        help='generates a view focused exclusively on paths',
    )

    parser.add_argument(
        '-o',
        metavar='N',
        nargs='?',
        type=int,
        const=2,
        help='Text-Only Mode: tree in plain text. N spaces indent (default 2)',
    )

    parser.add_argument(
        '-fs',
        '--file-size',
        action='store_true',
        help='toggle visibility of individual file sizes',
    )

    parser.add_argument(
        '-ds',
        '--dir-size',
        action='store_true',
        help='display cumulative sizes for folders',
    )

    ordering = parser.add_mutually_exclusive_group()
    ordering.add_argument(
        '-d',
        '--dirs-first',
        action='store_true',
        help='list directories before files',
    )
    ordering.add_argument(
        '-f',
        '--files-first',
        action='store_true',
        help='list files before directories',
    )
    
    size_sorting = parser.add_mutually_exclusive_group()
    size_sorting.add_argument(
        '-b',
        '--big-first',
        action='store_true',
        help='order tree entries by size (descending)',
    )
    size_sorting.add_argument(
        '-s',
        '--small-first',
        action='store_true',
        help='order tree entries by size (ascending)',
    )

    parser.add_argument(
        '-n',
        '--no-pipes',
        action='store_true',
        help='remove vertical pipes between branches',
    )

    parser.add_argument(
        '-r',
        '--reverse',
        action='store_true',
        help='reverse alphabet sort order',
    )

    parser.add_argument(
        '-i',
        '--ignore',
        metavar='PATTERN',
        nargs='*',
        default=None,
        help='ignore files or directories (e.g. *.py __pycache__)',
    )

    parser.add_argument(
        '-fi',
        '--filter',
        metavar='PATTERN',
        nargs='*',
        default=None,
        help='include only files or directories matching gitignore-style patterns',
    )

    parser.add_argument(
        '-gi',
        '--gitignore',
        nargs='*',
        default=False,
        metavar='DIR_OR_FILE',
        help='respect .gitignore rules from given paths (defaults to current directory if omitted but flag is present)',
    )

    parser.add_argument(
        '-g',
        '--git',
        nargs='*',
        default=False,
        metavar='DIR',
        help='ignore .git folder and use .gitignore from given directories or directories containing .git (defaults to current directory if omitted but flag is present)',
    )

    parser.add_argument(
        '-dl',
        '--depth-level',
        metavar='N',
        type=int,
        help='limit tree depth (>= 0)',
    )

    parser.add_argument(
        '-dt',
        '--dict-tree',
        metavar='N',
        nargs='?',
        type=int,
        const=2,
        help='output the tree structure as a native Python dictionary (JSON format). N spaces indent (default 2)',
    )

    args = parser.parse_args()

    # Validate -g/--git option: must be directories only
    if args.git is not False:
        if args.git:  # If specific paths provided
            for path_str in args.git:
                path = pathlib.Path(path_str).resolve()
                if not path.exists():
                    parser.error(f'--git path does not exist: {path_str}')
                if not path.is_dir():
                    parser.error(f'--git option only accepts directories: {path_str}')
                
                # Check if it's a .git directory or contains .git
                git_dir = path if path.name == '.git' else path / '.git'
                if not git_dir.exists() or not git_dir.is_dir():
                    parser.error(f'--git path must be a .git directory or contain a .git directory: {path_str}')

    # Validate -gi/--gitignore option: can be files or directories
    if args.gitignore is not False:
        if args.gitignore:  # If specific paths provided
            for path_str in args.gitignore:
                path = pathlib.Path(path_str).resolve()
                if not path.exists():
                    parser.error(f'--gitignore path does not exist: {path_str}')
                
                # If it's a file, must be named .gitignore
                if path.is_file() and path.name != '.gitignore':
                    parser.error(f'--gitignore file must be named .gitignore: {path_str}')
                
                # If it's a directory, must contain .gitignore
                if path.is_dir():
                    gitignore_file = path / '.gitignore'
                    if not gitignore_file.exists():
                        parser.error(f'--gitignore directory must contain a .gitignore file: {path_str}')

    if (args.dir_only or args.files_only) and (
        args.dirs_first or args.files_first
    ):
        parser.error('ordering options cannot be used with --dir-only or --files-only')

    if args.depth_level is not None and args.depth_level < 0:
        parser.error('--depth-level must be >= 0')
        
    if args.o is not None and args.no_pipes:
        parser.error('-o (Text-Only Mode) cannot be used with -n/--no-pipes')

    if args.o is not None and args.o < 0:
        parser.error('-o indent must be >= 0')

    return args