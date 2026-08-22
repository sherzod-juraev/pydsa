"""Trees package.

Exposes all tree-based data structures: :class:`BinaryTree` (general),
:class:`BSTree` (binary searching tree), :class:`AVLTree`
(self-balancing BST), :class:`MinHeap`/:class:`MaxHeap`, and
:class:`Trie` (prefix tree).
"""

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    "AVLTree",
    "BinaryTree",
    "BSTree",
    "MaxHeap",
    "MinHeap",
    "Trie",
]

# Submodules available for lazy import
_SUBMODULES = {
    "avl",
    "binary_tree",
    "bst",
    "heap",
    "trie",
}

# Mapping: symbol → (module, name)
_LAZY_IMPORTS = {
    "AVLTree": ("avl", "AVLTree"),
    "BinaryTree": ("binary_tree", "BinaryTree"),
    "BSTree": ("bst", "BSTree"),
    "MaxHeap": ("heap", "MaxHeap"),
    "MinHeap": ("heap", "MinHeap"),
    "Trie": ("trie", "Trie"),
}


def __dir__() -> list[str]:
    """Return list of public attributes and submodules."""
    return sorted(list(__all__) + list(_SUBMODULES))


def __getattr__(name: str) -> Any:
    """Lazy-load submodules and tree structures on demand.

    Parameters
    ----------
    name : str
        The name of the attribute, submodule, or tree data structure
        being accessed.

    Returns
    -------
    Any
        The requested submodule or tree class dynamically imported from
        the respective package.

    Raises
    ------
    AttributeError
        If the requested attribute does not exist in the public API or
        tree submodules.
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
