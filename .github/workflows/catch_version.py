'''
Compare pyproject.toml version with the latest git tag.
Useful for determining if a new release tag should be created.
'''

import sys
import tomllib
import subprocess
from pathlib import Path


def get_pyproject_version():
    '''Get version from pyproject.toml.'''
    with open('pyproject.toml', 'rb') as f:
        data = tomllib.load(f)
    return data['project']['version']


def get_latest_tag_version():
    '''Get version from the latest git tag.'''
    try:
        result = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        return result.lstrip('v')
    except subprocess.CalledProcessError:
        return None


def main():
    pyproject_version = get_pyproject_version()
    latest_tag_version = get_latest_tag_version()

    print(f'pyproject.toml version: {pyproject_version}')
    print(f'Latest tag version: {latest_tag_version}')

    if latest_tag_version is None:
        print('✓ No tags found. Ready to create first tag.')
        print(f'::set-output name=old::{latest_tag_version or ''}')
        print(f'::set-output name=new::{pyproject_version}')
        return 0

    if pyproject_version != latest_tag_version:
        print(f'✓ Version changed! Ready to create tag v{pyproject_version}')
        print(f'::set-output name=old::{latest_tag_version}')
        print(f'::set-output name=new::{pyproject_version}')
        return 0
    else:
        print(f'✗ Version not changed ({pyproject_version})')
        print(f'::set-output name=old::{latest_tag_version}')
        print(f'::set-output name=new::{pyproject_version}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
