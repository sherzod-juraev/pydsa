"""Sorting algorithms.

Exposes the elementary sorts (:func:`bubble_sort`, :func:`selection_sort`,
:func:`insertion_sort`), the O(n log n) sorts (:func:`merge_sort`,
:func:`quick_sort`, :func:`heap_sort`) and the non-comparison sorts
(:func:`counting_sort`, :func:`radix_sort`, :func:`bucket_sort`). Everything
is imported lazily, on first access.
"""

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "heap_sort",
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
    The requested function.

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
