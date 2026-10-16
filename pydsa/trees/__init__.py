"""Tree data structures.

Exposes the binary trees :class:`BinaryTree`, :class:`BSTree` and :class:`AVLTree`,
the binary heaps :class:`MinHeap` and :class:`MaxHeap`, and the prefix tree
:class:`Trie`. Everything is imported lazily, on first access.
"""

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    "AVLTree",
    "BSTree",
    "BinaryTree",
    "MaxHeap",
    "MinHeap",
    "Trie",
]

# Mapping: symbol → (module, name)
_LAZY_IMPORTS = {
    "AVLTree": ("avl", "AVLTree"),
    "BSTree": ("bst", "BSTree"),
    "BinaryTree": ("binary_tree", "BinaryTree"),
    "MaxHeap": ("heap", "MaxHeap"),
    "MinHeap": ("heap", "MinHeap"),
    "Trie": ("trie", "Trie"),
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
