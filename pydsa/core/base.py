"""Common base class for every pydsa data structure.

Provides :class:`BaseStructure`, which fixes the small interface shared by all
structures and implements the emptiness check that would otherwise be repeated in
each of them.
"""

from abc import ABC, abstractmethod
from collections.abc import Sized

from ..exc import EmptyError


class BaseStructure(ABC, Sized):
    """Abstract base class for all pydsa data structures.

    Every structure reports its size with ``len()`` and can be emptied with
    ``clear()``. Subclasses must implement both, otherwise they cannot be
    instantiated.

    Notes
    -----
    - Truthiness follows ``len()``: a structure is falsy when it holds no elements,
      so ``if structure:`` replaces an explicit emptiness test. There is no
      ``is_empty`` method. Because ``bool()`` calls ``__len__``, ``__len__`` should
      run in constant time.
    - Operations that need an element, such as removing or peeking, call the
      protected ``_ensure_not_empty`` first, so every structure raises ``EmptyError``
      with the same message.

    Examples
    --------
    A minimal structure only has to provide ``__len__`` and ``clear``:

    >>> class Bag(BaseStructure):
    ...     def __init__(self) -> None:
    ...         self.items: list[int] = []
    ...
    ...     def __len__(self) -> int:
    ...         return len(self.items)
    ...
    ...     def clear(self) -> None:
    ...         self.items.clear()
    >>> bag = Bag()
    >>> bool(bag)
    False
    >>> bag.items.append(1)
    >>> len(bag), bool(bag)
    (1, True)
    >>> bag.clear()
    >>> bool(bag)
    False
    """

    @abstractmethod
    def clear(self) -> None:
        """Remove all elements from the structure.

        Afterwards ``len(self)`` is ``0``.
        """

    def _ensure_not_empty(self) -> None:
        """Raise an error if the structure holds no elements.

        The message names the concrete class, so a subclass reports its own name.

        Raises
        ------
        EmptyError
            If ``len(self) == 0``.
        """
        if len(self) == 0:
            raise EmptyError(f"{type(self).__name__} is empty")
