"""Sorting algorithms package.

Exposes elementary sorts (bubble, selection, insertion), divide-and-conquer
sorts (merge, quick), heap sort, and non-comparison sorts (counting,
radix, bucket).
"""

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "heap.py",
    "quick_sort",
    "counting_sort",
    "radix_sort",
    "bucket_sort",
]

# Mapping: symbol → (module, name)
_LAZY_IMPORTS = {
    "bubble_sort": ("elementary", "bubble_sort"),
    "selection_sort": ("elementary", "selection_sort"),
    "insertion_sort": ("elementary", "insertion_sort"),
    "merge_sort": ("divide_conquer", "merge_sort"),
    "quick_sort": ("divide_conquer", "quick_sort"),
    "heap_sort": ("heap", "heap_sort"),
    "counting_sort": ("linear", "counting_sort"),
    "radix_sort": ("linear", "radix_sort"),
    "bucket_sort": ("linear", "bucket_sort"),
}


def __dir__() -> list[str]:
    """Return list of public attributes and submodules."""
    return sorted(__all__)


def __getattr__(name: str) -> Any:
    """Lazy-load sorting algorithms on demand.

    Parameters
    ----------
    name : str
        The name of the sorting algorithm being accessed.

    Returns
    -------
    Any
        The requested sorting function dynamically imported from the
        respective submodule.

    Raises
    ------
    AttributeError
        If the requested sorting algorithm does not exist in the public API.
    """
    if name in _LAZY_IMPORTS:
        module_name, symbol_name = _LAZY_IMPORTS[name]
        module = importlib.import_module(f".{module_name}", __name__)
        return getattr(module, symbol_name)

    # Attribute not found
    raise AttributeError(
        f"module '{__name__}' has no attribute '{name}'. Available: {', '.join(sorted(__all__))}"
    )
