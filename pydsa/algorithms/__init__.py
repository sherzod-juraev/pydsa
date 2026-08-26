"""Algorithms package.

Exposes dynamic-programming solutions (:mod:`pydsa.algorithms.dp`) and
greedy algorithms (:mod:`pydsa.algorithms.greedy`).
"""

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    "fib_memo",
    "fib_tab",
    "knapsack_tab",
    "lcs_tab",
    "coin_change",
    "edit_distance",
    "activity_selection",
    "job_sequencing",
    "fractional_knapsack",
    "huffman_coding",
]

# Mapping: symbol → (module, name)
_LAZY_IMPORTS = {
    "fib_memo": ("dp", "fib_memo"),
    "fib_tab": ("dp", "fib_tab"),
    "knapsack_tab": ("dp", "knapsack_tab"),
    "lcs_tab": ("dp", "lcs_tab"),
    "coin_change": ("dp", "coin_change"),
    "edit_distance": ("dp", "edit_distance"),
    "activity_selection": ("greedy", "activity_selection"),
    "job_sequencing": ("greedy", "job_sequencing"),
    "fractional_knapsack": ("greedy", "fractional_knapsack"),
    "huffman_coding": ("greedy", "huffman_coding"),
}


def __dir__():
    """Return list of public attributes and submodules."""
    return sorted(__all__)


def __getattr__(name: str) -> Any:
    """Lazy-load symbols on demand.

    Parameters
    ----------
    name : str
        The attribute name being accessed.

    Returns
    -------
    Any
        The requested class or exception.

    Raises
    ------
    AttributeError
        If the attribute does not exist.
    """
    # Check for lazy symbol import
    if name in _LAZY_IMPORTS:
        module_name, symbol_name = _LAZY_IMPORTS[name]
        module = importlib.import_module(f".{module_name}", __name__)
        return getattr(module, symbol_name)
    # Attribute not found
    raise AttributeError(
        f"module '{__name__}' has no attribute '{name}'. Available: {', '.join(sorted(__all__))}"
    )
