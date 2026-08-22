"""Linear data structures package.

Exposes the linear data structures implemented in this package:
:class:`SinglyList` and :class:`DoublyList` (linked lists), and
:class:`Stack` and :class:`Queue` (adapters built on top of them).
"""

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    "DoublyList",
    "Queue",
    "SinglyList",
    "Stack",
]

# Submodules available for lazy import
_SUBMODULES = {
    "doubly",
    "singly",
}

# Mapping: symbol → (module, name)
_LAZY_IMPORTS = {
    "DoublyList": ("doubly", "DoublyList"),
    "Queue": ("queue", "Queue"),
    "SinglyList": ("singly", "SinglyList"),
    "Stack": ("stack", "Stack"),
}


def __dir__() -> list[str]:
    """Return list of public attributes and submodules."""
    return sorted(list(__all__) + list(_SUBMODULES))


def __getattr__(name: str) -> Any:
    """Lazy-load submodules and symbols on demand.

    Parameters
    ----------
    name : str
        The name of the attribute, submodule, or data structure being accessed.

    Returns
    -------
    Any
        The requested module or class dynamically imported from the
        respective submodule.

    Raises
    ------
    AttributeError
        If the requested attribute does not exist in the public API or
        submodules.
    """
    # Check for submodule access
    if name in _SUBMODULES:
        return importlib.import_module(f".{name}", __name__)

    # Check for lazy symbol import
    if name in _LAZY_IMPORTS:
        module_name, symbol_name = _LAZY_IMPORTS[name]
        module = importlib.import_module(f".{module_name}", __name__)
        return getattr(module, symbol_name)

    # Attribute not found
    raise AttributeError(
        f"module '{__name__}' has no attribute '{name}'. Available: {', '.join(sorted(__all__))}"
    )
