# -*- coding: utf-8 -*-

__all__ = [
    "__version__",
    "solve",
    "kepler",
]

from .kepler import solve
from .core import kepler
from .kepler_version import __version__

__uri__ = "https://github.com/dfm/kepler.py"
__author__ = "Daniel Foreman-Mackey"
__email__ = "foreman.mackey@gmail.com"
__license__ = "MIT"
__description__ = "Fast and stable Kepler solver"
