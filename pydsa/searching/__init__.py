"""Searching algorithms package.

Exposes classic search algorithms: linear, binary, jump, and
exponential search.
"""

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    "linear_search",
    "binary_search",
    "jump_search",
    "exponential_search",
]

# Mapping: symbol → (module, name)
_LAZY_IMPORTS = {
    "linear_search": ("search", "linear_search"),
    "binary_search": ("search", "binary_search"),
    "jump_search": ("search", "jump_search"),
    "exponential_search": ("search", "exponential_search"),
}


def __dir__() -> list[str]:
    """Return list of public attributes and submodules."""
    return sorted(__all__)


def __getattr__(name: str) -> Any:
    """Lazy-load searching algorithms on demand.

    Parameters
    ----------
    name : str
        The name of the attribute or searching algorithm being accessed.

    Returns
    -------
    Any
        The requested searching function dynamically imported from the
        search module.

    Raises
    ------
    AttributeError
        If the requested attribute does not exist in the public API mapping.
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
