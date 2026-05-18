# pydsa

**Pure Python Data Structures & Algorithms — built from scratch.**

[![Tests](https://github.com/sherzod-juraev/pydsa/actions/workflows/tests.yml/badge.svg)](https://github.com/sherzod-juraev/pydsa/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## About

`pydsa` is a self-contained Python library implementing fundamental data structures
and algorithms entirely from scratch. Every linked list, tree, heap, graph, and sorting
routine is built node by node, without delegating to Python's built-in collections.

This is **not** a production-grade library. It is an educational project — a personal
commitment to understanding DSA not just in theory, but through the discipline of
writing, testing, and refining every component by hand.

---

## Why This Exists

Most DSA resources stop at pseudocode or fragmented code snippets. This project
goes further: each data structure and algorithm is implemented as a working module
with a clean public API, full docstrings, and comprehensive test coverage. It
answers the question: *"What does it actually take to build these things for real?"*

**What makes it different:**
- Zero external dependencies for core logic (`numpy` and `numba` are used only in
  sorting/searching modules for performance, and are entirely optional)
- Every component is written from scratch — custom `Stack`, `Queue`, `SinglyList`,
  `DoublyList`, `AVLTree`, `HashTable`, `Graph`, and more
- Iterative implementations throughout — no recursion depth limits, no hidden
  overhead, production-style clarity
- 914 passing tests covering edge cases, invariants, stability, and large inputs

---

## Installation

```bash
git clone https://github.com/sherzod-juraev/pydsa.git
cd pydsa
pip install -e .
```

## For development (includes testing tools):
```bash
pip install -e ".[dev]"
```

## Quick start
```python
import pydsa

# Linked Lists
lst = pydsa.SinglyList()
lst.insert_last(10)
lst.insert_last(20)
print(list(lst))  # [10, 20]

# Binary Search Tree
bst = pydsa.BSTree()
bst.insert(5)
bst.insert(3)
bst.insert(8)
print(list(bst.inorder()))  # [3, 5, 8] — sorted!

# AVL Tree (self-balancing)
avl = pydsa.AVLTree()
for v in [1, 2, 3, 4, 5, 6, 7]:
    avl.insert(v)
print(avl.height())  # 3 (balanced, not 7)

# Heap
heap = pydsa.MinHeap()
heap.heapify([5, 3, 8, 1, 4])
print(heap.extract_all())  # [1, 3, 4, 5, 8]

# Trie
trie = pydsa.Trie()
trie.insert("hello")
trie.insert("world")
print(list(trie.words_with_prefix("he")))  # ['hello']

# Hash Table
ht = pydsa.HashTable(capacity=16)
ht["name"] = "Sherzod"
print(ht["name"])  # Sherzod

# Graph
g = pydsa.Graph(directed=False)
g.add_edge("A", "B")
g.add_edge("B", "C")
print(g.has_path("A", "C"))  # True

# Sorting
import numpy as np
arr = np.array([5, 2, 8, 1, 4])
print(pydsa.merge_sort(arr))  # [1 2 4 5 8]

# Dynamic Programming
print(pydsa.fib_tab(50))  # 12586269025
print(pydsa.edit_distance("kitten", "sitting"))  # 3
```

## What's Inside

## What's Inside

| Module         | Components                                                      | Description                                                                                  |
|----------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| **Linear**     | `SinglyList`, `DoublyList`, `Stack`, `Queue`                    | Linked structures with full CRUD, indexing, reversals                                        |
| **Trees**      | `BinaryTree`, `BSTree`, `AVLTree`, `MinHeap`, `MaxHeap`, `Trie` | Recursive and iterative traversals, self-balancing rotations                                 |
| **Hash**       | `HashTable`                                                     | Separate chaining with `SinglyList`, auto-rehashing at 0.75 load factor                      |
| **Graph**      | `Graph`                                                         | Adjacency list, BFS, DFS, path existence, connectivity                                       |
| **Sorting**    | 9 algorithms                                                    | Bubble, Selection, Insertion, Merge, Quick, Heap, Counting, Radix, Bucket                    |
| **Searching**  | 4 algorithms                                                    | Linear, Binary, Jump, Exponential                                                            |
| **Algorithms** | DP + Greedy                                                     | Fibonacci, Knapsack 0/1, LCS, Coin Change, Edit Distance, Activity Selection, Huffman Coding |

## Testing
```bash
pytest tests/ -v
```
```text
914 passed
```
Tests cover:

- Empty and single-element cases

- Sorted, reverse-sorted, and random data

- Stability (where applicable)

- Invariant preservation (AVL, BST, Heap)

- Large inputs (1000–5000 elements)

- Edge cases: duplicates, negative values, self-loops, special float values

## Disclaimer
This library is built for learning and educational purposes. It is not intended
for production use, and updates will be infrequent. The goal is depth of understanding,
not breadth of features or performance optimization.


## Author
**Sherzod Juraev**

Student, National University of Uzbekistan (Mirzo Ulug'bek)

Faculty of Applied Mathematics and Intellectual Technologies

Artificial Intelligence, 3rd year

This project represents the intersection of disciplined self-study and practical
engineering: every structure in this library was written from a blank file, tested
to exhaustion, and revised until it was right. The value is not just in the code,
but in what the process teaches about patience, precision, and respect for fundamentals.

License
MIT — see [LICENSE](LICENSE) for details.