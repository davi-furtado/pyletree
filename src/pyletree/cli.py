'''This module provides the Pyletree CLI.'''

import argparse

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
        '--filter',
        metavar='PATTERN',
        nargs='*',
        default=None,
        help='include files based on patterns or extensions',
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
        metavar='DIR_OR_FILE',
        help='ignore .git folder and use .gitignore from given paths (defaults to current directory if omitted but flag is present)',
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
        action='store_true',
        help='output the tree structure as a native Python dictionary (JSON format)',
    )

    args = parser.parse_args()

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