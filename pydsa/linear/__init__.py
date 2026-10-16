"""Linear data structures.

Exposes :class:`SinglyList` and :class:`DoublyList` (linked lists) and
:class:`Stack` and :class:`Queue` (restricted views over a singly linked list).
Everything is imported lazily, on first access.
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

# Mapping: symbol → (module, name)
_LAZY_IMPORTS = {
    "DoublyList": ("doubly", "DoublyList"),
    "Queue": ("queue", "Queue"),
    "SinglyList": ("singly", "SinglyList"),
    "Stack": ("stack", "Stack"),
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
        The requested class.

    Raises
    ------
    AttributeError
        If the attribute does not exist.
    """
    if name in _LAZY_IMPORTS:
        module_name, symbol_name = _LAZY_IMPORTS[name]
        module = importlib.import_module(f".{module_name}", __name__)
        return getattr(module, symbol_name)

    # Attribute not found
    raise AttributeError(
        f"module '{__name__}' has no attribute '{name}'. Available: {', '.join(sorted(__all__))}"
    )
