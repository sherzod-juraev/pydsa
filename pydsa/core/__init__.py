"""Core building blocks shared by every pydsa data structure.

Exposes :class:`BaseStructure`, the abstract base class all structures derive from,
and :class:`Comparable`, the protocol that bounds the element type of ordered
structures and algorithms. Both are imported lazily, on first access.
"""

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    "BaseStructure",
    "Comparable",
]

# Mapping: symbol → (module, name)
_LAZY_IMPORTS = {
    "BaseStructure": ("base", "BaseStructure"),
    "Comparable": ("protocols", "Comparable"),
}


def __dir__() -> list[str]:
    """Return the sorted names of the public attributes."""
    return sorted(__all__)


def __getattr__(name: str) -> Any:
    """Lazy-load public symbols on demand.

    Parameters
    ----------
    name : str
        The attribute name being accessed.

    Returns
    -------
    Any
        The requested class or protocol.

    Raises
    ------
    AttributeError
        If the attribute does not exist.
    """
    # Check for lazy symbol import (e.g., BaseStructure)
    if name in _LAZY_IMPORTS:
        module_name, symbol_name = _LAZY_IMPORTS[name]
        module = importlib.import_module(f".{module_name}", __name__)
        return getattr(module, symbol_name)

    # Attribute not found
    raise AttributeError(
        f"module '{__name__}' has no attribute '{name}'. Available: {', '.join(sorted(__all__))}"
    )
