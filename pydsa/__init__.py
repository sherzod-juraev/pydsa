"""pydsa — Pure Python Data Structures & Algorithms.

A comprehensive, educational library implementing fundamental data structures
and algorithms from scratch in pure Python with full type safety.

Core Components
===============

**Linear Data Structures**
    :class:`SinglyList`, :class:`DoublyList`, :class:`Stack`, :class:`Queue`

**Trees**
    :class:`BinaryTree`, :class:`BSTree`, :class:`AVLTree`,
    :class:`MinHeap`, :class:`MaxHeap`, :class:`Trie`

**Hash-based**
    :class:`HashTable`

**Graph**
    :class:`Graph`

**Sorting Algorithms** (O(n²) to O(n log n))
    :func:`bubble_sort`, :func:`selection_sort`, :func:`insertion_sort`,
    :func:`merge_sort`, :func:`quick_sort`, :func:`heap_sort`,
    :func:`counting_sort`, :func:`radix_sort`, :func:`bucket_sort`

**Searching Algorithms** (O(n) to O(log n))
    :func:`linear_search`, :func:`binary_search`,
    :func:`jump_search`, :func:`exponential_search`

**Dynamic Programming**
    :func:`fib_memo`, :func:`fib_tab`, :func:`knapsack_tab`, :func:`lcs_tab`,
    :func:`coin_change`, :func:`edit_distance`

**Greedy Algorithms**
    :func:`activity_selection`, :func:`job_sequencing`,
    :func:`fractional_knapsack`, :func:`huffman_coding`

**Exceptions**
    :exc:`PydsaError`, :exc:`EmptyError`

Quick Start
===========

Linear Structures
-----------------
>>> from pydsa import SinglyList, Stack, Queue
>>>
>>> lst = SinglyList[int]()
>>> lst.insert_last(1)
>>> lst.insert_last(2)
>>> list(lst)
[1, 2]
>>>
>>> stack = Stack[int]()
>>> stack.push(42)
>>> stack.pop()
42

Trees
-----
>>> from pydsa import BSTree, MinHeap
>>>
>>> bst = BSTree[int]()
>>> bst.insert(5)
>>> bst.insert(3)
>>> bst.insert(7)
>>> bst.search(3)
True

Sorting
-------
>>> from pydsa import merge_sort, bubble_sort
>>>
>>> merge_sort([3, 1, 4, 1, 5, 9, 2, 6])
[1, 1, 2, 3, 4, 5, 6, 9]

Searching
---------
>>> from pydsa import binary_search
>>>
>>> binary_search([1, 3, 5, 7, 9], 5)
2

Dynamic Programming
-------------------
>>> from pydsa import fib_memo, fib_tab
>>>
>>> fib_memo(10)
55
>>> fib_tab(10)
55

Design Philosophy
=================

**Pure Python**: No external dependencies (educational focus)
**Type Safe**: Full generic type hints, zero mypy errors
**Readable**: Clear implementations, not optimized for production speed
**Educational**: Focused on learning DSA concepts, not performance tricks
**Comprehensive**: All classic algorithms and data structures
**Well-Tested**: 506 passing tests with invariant preservation

Module Structure
================

.. toctree::
   :hidden:

   pydsa.linear
   pydsa.trees
   pydsa.hash
   pydsa.graph
   pydsa.sorting
   pydsa.searching
   pydsa.algorithms
   pydsa.exc


License
=======

MIT License. See LICENSE file for details.

Author
======

Sherzod Juraev

See Also
--------
- GitHub: https://github.com/sherzod-juraev/pydsa
- Tests: See tests/ directory for usage examples
"""

__version__ = "1.1.0"

import importlib
from typing import Any

# Lazy-load all public API
__all__ = [
    # Exceptions
    "PydsaError",
    "EmptyError",
    # Linear Data Structures
    "SinglyList",
    "DoublyList",
    "Queue",
    "Stack",
    # Trees
    "BinaryTree",
    "BSTree",
    "AVLTree",
    "MinHeap",
    "MaxHeap",
    "Trie",
    # Hash & Graph
    "HashTable",
    "Graph",
    # Sorting
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "heap_sort",
    "counting_sort",
    "radix_sort",
    "bucket_sort",
    # Searching
    "linear_search",
    "binary_search",
    "jump_search",
    "exponential_search",
    # Dynamic Programming
    "fib_memo",
    "fib_tab",
    "knapsack_tab",
    "lcs_tab",
    "coin_change",
    "edit_distance",
    # Greedy
    "activity_selection",
    "job_sequencing",
    "fractional_knapsack",
    "huffman_coding",
]

# Submodules available for lazy import
_SUBMODULES = {
    "linear",
    "trees",
    "hash",
    "graph",
    "sorting",
    "searching",
    "algorithms",
    "exc",
}

# Mapping: symbol → (module, name)
_LAZY_IMPORTS = {
    "PydsaError": ("exc", "PydsaError"),
    "EmptyError": ("exc", "EmptyError"),
    "SinglyList": ("linear", "SinglyList"),
    "DoublyList": ("linear", "DoublyList"),
    "Queue": ("linear", "Queue"),
    "Stack": ("linear", "Stack"),
    "BinaryTree": ("trees", "BinaryTree"),
    "BSTree": ("trees", "BSTree"),
    "AVLTree": ("trees", "AVLTree"),
    "MinHeap": ("trees", "MinHeap"),
    "MaxHeap": ("trees", "MaxHeap"),
    "Trie": ("trees", "Trie"),
    "HashTable": ("hash", "HashTable"),
    "Graph": ("graph", "Graph"),
    "bubble_sort": ("sorting", "bubble_sort"),
    "selection_sort": ("sorting", "selection_sort"),
    "insertion_sort": ("sorting", "insertion_sort"),
    "merge_sort": ("sorting", "merge_sort"),
    "quick_sort": ("sorting", "quick_sort"),
    "heap_sort": ("sorting", "heap_sort"),
    "counting_sort": ("sorting", "counting_sort"),
    "radix_sort": ("sorting", "radix_sort"),
    "bucket_sort": ("sorting", "bucket_sort"),
    "linear_search": ("searching", "linear_search"),
    "binary_search": ("searching", "binary_search"),
    "jump_search": ("searching", "jump_search"),
    "exponential_search": ("searching", "exponential_search"),
    "fib_memo": ("algorithms", "fib_memo"),
    "fib_tab": ("algorithms", "fib_tab"),
    "knapsack_tab": ("algorithms", "knapsack_tab"),
    "lcs_tab": ("algorithms", "lcs_tab"),
    "coin_change": ("algorithms", "coin_change"),
    "edit_distance": ("algorithms", "edit_distance"),
    "activity_selection": ("algorithms", "activity_selection"),
    "job_sequencing": ("algorithms", "job_sequencing"),
    "fractional_knapsack": ("algorithms", "fractional_knapsack"),
    "huffman_coding": ("algorithms", "huffman_coding"),
}


def __dir__() -> list[str]:
    """Return list of public attributes and submodules."""
    return sorted(list(__all__) + list(_SUBMODULES))


def __getattr__(name: str) -> Any:
    """Lazy-load symbols and submodules on demand.

    Parameters
    ----------
    name : str
        The attribute name being accessed.

    Returns
    -------
    Any
        The requested module, class, or function.

    Raises
    ------
    AttributeError
        If the attribute does not exist.
    """
    # Check for submodule access (e.g., pydsa.linear)
    if name in _SUBMODULES:
        return importlib.import_module(f".{name}", __name__)

    # Check for lazy symbol import (e.g., pydsa.SinglyList)
    if name in _LAZY_IMPORTS:
        module_name, symbol_name = _LAZY_IMPORTS[name]
        module = importlib.import_module(f".{module_name}", __name__)
        return getattr(module, symbol_name)

    # Attribute not found
    raise AttributeError(
        f"module '{__name__}' has no attribute '{name}'. Available: {', '.join(sorted(__all__))}"
    )
