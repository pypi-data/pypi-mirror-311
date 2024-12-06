from . import controller
from . import models
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("uspto_odp")
except PackageNotFoundError:  # pragma: no cover
    # Package is not installed
    __version__ = "unknown"

__all__ = ['controller', 'models', '__version__']
