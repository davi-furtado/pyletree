"""Top-level package for Pyletree."""

"""Top-level Pyletree package interface."""

from importlib.metadata import version

from .pyletree import FileTree

__all__ = ["__version__", "FileTree"]

__version__ = version("pyletree")
