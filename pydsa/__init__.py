import importlib

from .linear import *
from .trees import *
from .hash import *
from .graph import *
from .sorting import *
from .searching import *
from .algorithms import *
from .exc import PydsaException, Empty


__all__ = [
    "PydsaException", "Empty",
    "SinglyList", "DoublyList", "Queue", "Stack",
    "BinaryTree", "BSTree", "AVLTree", "MinHeap", "MaxHeap", "Trie",
    "HashTable", "Graph",
    "bubble_sort", "selection_sort", "insertion_sort",
    "merge_sort", "quick_sort", "heap_sort",
    "counting_sort", "radix_sort", "bucket_sort",
    "linear_search", "binary_search", "jump_search", "exponential_search",
    "fib_memo", "fib_tab", "knapsack_tab", "lcs_tab", "coin_change", "edit_distance",
    "activity_selection", "job_sequencing", "fractional_knapsack", "huffman_coding",
]

_submodules = {
    "linear", "trees", "hash", "graph", "sorting", "searching", "algorithms", "exc"
}

def __dir__():
    return list(__all__) + list(_submodules)

def __getattr__(name):
    if name in _submodules:
        return importlib.import_module(f".{name}", __name__)
    raise AttributeError(f"module 'pydsa' has no attribute '{name}'")