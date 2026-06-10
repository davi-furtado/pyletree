"""Top-level package for Pyletree."""

"""Top-level Pyletree package interface."""

from importlib.metadata import version, PackageNotFoundError

from .pyletree import FileTree

__all__ = ["__version__", "FileTree"]

try:
    __version__ = version("pyletree")
except PackageNotFoundError:
    __version__ = "0.0.0"
