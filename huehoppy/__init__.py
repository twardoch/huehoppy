"""
huehoppy: Advanced Color Transfer Tool

A unified and extensible color transfer library that consolidates the best features
of existing color transfer libraries while offering enhanced modularity, consistent API,
and sophisticated processing pipelines.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("huehoppy")
except PackageNotFoundError:
    # Package is not installed, try to get version from git tags
    try:
        from setuptools_scm import get_version
        __version__ = get_version(root="..", relative_to=__file__)
    except Exception:
        __version__ = "unknown"

__author__ = "Terragon Labs"
__email__ = "contact@terragonlabs.com"
__license__ = "MIT"

# Public API
from .core import ColorTransferAlgorithm, HueHoppyManager
from .cli import main as cli_main

__all__ = [
    "__version__",
    "ColorTransferAlgorithm", 
    "HueHoppyManager",
    "cli_main",
]