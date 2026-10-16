"""Pure Python data structures and algorithms.

Exposes the submodules :mod:`pydsa.core`, :mod:`pydsa.exc`, :mod:`pydsa.linear`,
:mod:`pydsa.trees`, :mod:`pydsa.hash`, :mod:`pydsa.graph`, :mod:`pydsa.sorting` and
:mod:`pydsa.searching`. Everything is imported lazily, on first access.
"""

__version__ = "2.0.0"

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    "linear",
    "core",
    "trees",
    "hash",
    "graph",
    "sorting",
    "searching",
    "exc",
]


def __dir__() -> list[str]:
    """Return list of public attributes and submodules."""
    return sorted(__all__)


def __getattr__(name: str) -> Any:
    """Lazy-load symbols and submodules on demand.

    Parameters
    ----------
    name : str
        The attribute name being accessed.

    Returns
    -------
    Any
        The requested module, class, or function.

    Raises
    ------
    AttributeError
        If the attribute does not exist.
    """
    if name in __all__:
        return importlib.import_module(f".{name}", __name__)

    # Attribute not found
    raise AttributeError(
        f"module '{__name__}' has no attribute '{name}'. Available: {', '.join(sorted(__all__))}"
    )
