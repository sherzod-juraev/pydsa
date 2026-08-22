"""Exception types package.

Exposes the exception hierarchy used throughout pydsa:
:class:`PydsaError` (base) and :class:`EmptyError`.
"""

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    "PydsaError",
    "EmptyError",
]

# Mapping: symbol → (module, name)
_LAZY_IMPORTS = {
    "PydsaError": ("base", "PydsaError"),
    "EmptyError": ("empty", "EmptyError"),
}


def __dir__() -> list[str]:
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
