# pydsa

[![Tests](https://github.com/sherzod-juraev/pydsa/actions/workflows/tests.yml/badge.svg)](https://github.com/sherzod-juraev/pydsa/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12 | 3.13](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![mypy: strict](https://img.shields.io/badge/mypy-strict-blue.svg)](https://mypy.readthedocs.io/)

Pure Python implementations of fundamental data structures and algorithms.

`pydsa` is an educational package built from scratch, without relying on Python's built-in collection types for its core structures. It exists to study how these structures and algorithms work internally, and to practice typed, tested Python.

## About

`pydsa` contains implementations of:

* linear data structures;
* trees and heaps;
* a hash table;
* a graph;
* sorting algorithms;
* searching algorithms;
* dynamic programming algorithms;
* greedy algorithms.

The project favors direct, readable implementations over additional abstraction.

## Design Principles

### Implementations from scratch

Linked lists, stacks, queues, trees, heaps, a trie, a hash table, and a graph are implemented directly, without delegating storage or traversal to Python's built-in `list`, `dict`, or `set`.

### Generic type safety

The project uses Python 3.12+ generic syntax:

```python
from pydsa import SinglyList

numbers = SinglyList[int]()
names = SinglyList[str]()
```

The codebase is checked with mypy in strict mode.

### Explicit algorithm implementations

Sorting, searching, dynamic programming, and greedy algorithms are implemented as individual functions rather than wrapped in classes, keeping the relationship between code and algorithm direct.

### Lazy imports

Every package and subpackage uses `__getattr__`/`__dir__` (PEP 562) to defer imports until a symbol is actually accessed. Importing `pydsa` — or any of its subpackages — does not eagerly load every data structure and algorithm in the library.

### Testing

The test suite covers normal operation, edge cases (empty and single-element structures, duplicate values), and structural invariants where applicable (tree balance, heap order, cycle absence).

## Requirements

* Python 3.12 | 3.13

No external runtime dependencies.

## Installation

```bash
git clone https://github.com/sherzod-juraev/pydsa.git
cd pydsa
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

Development dependencies:

* pytest
* pytest-sugar
* ruff
* mypy
* interrogate

## Quick Start

### Linear Data Structures

```python
from pydsa import DoublyList, Queue, SinglyList, Stack

# Singly linked list
numbers = SinglyList[int]()
numbers.insert_last(10)
numbers.insert_last(20)

print(list(numbers))
# [10, 20]

# Doubly linked list — supports reverse iteration
names = DoublyList[str]()
names.insert_last("Alice")
names.insert_first("Bob")

print(list(names))
# ['Bob', 'Alice']
print(list(reversed(names)))
# ['Alice', 'Bob']

# Stack — LIFO
stack = Stack[int]()
stack.push(10)
stack.push(20)

print(stack.peek())
# 20

print(stack.pop())
# 20

# Queue — FIFO
queue = Queue[int]()
queue.enqueue(10)
queue.enqueue(20)

print(queue.peek())
# 10

print(queue.dequeue())
# 10
```

### Trees

```python
from pydsa import AVLTree, BinaryTree, BSTree

bst = BSTree[int]()
bst.insert(5)
bst.insert(3)
bst.insert(8)
print(list(bst.inorder()))
# [3, 5, 8]

avl = AVLTree[int]()
for value in [1, 2, 3, 4, 5, 6, 7]:
    avl.insert(value)
print(avl.height())
# 3

# General binary tree — path-based insertion
tree = BinaryTree[int]()
tree.insert(5, "")     # root
tree.insert(3, "L")
tree.insert(8, "R")
print(list(tree.preorder()))
# [5, 3, 8]
```

### Heaps

```python
from pydsa import MaxHeap, MinHeap

min_heap = MinHeap[int]()
min_heap.heapify([5, 3, 8, 1, 4])
print(min_heap.extract_all())
# [1, 3, 4, 5, 8]

max_heap = MaxHeap[int]()
max_heap.heapify([5, 3, 8, 1, 4])
print(max_heap.extract_all())
# [8, 5, 4, 3, 1]
```

### Trie

```python
from pydsa import Trie

trie = Trie()
trie.insert("hello")
trie.insert("world")
print(list(trie.words_with_prefix("he")))
# ["hello"]
```

### Hash Table

```python
from pydsa import HashTable

table = HashTable[str, str](capacity=16)
table["name"] = "Sherzod"
print(table["name"])
# Sherzod
```

### Graph

```python
from pydsa import Graph

graph = Graph(directed=False)
graph.add_edge("A", "B")
graph.add_edge("B", "C")
print(graph.has_path("A", "C"))
# True
```

### Sorting

```python
from pydsa import merge_sort

values = [5, 2, 8, 1, 4]
print(merge_sort(values))
# [1, 2, 4, 5, 8]
```

### Searching

```python
from pydsa import binary_search, linear_search

values = [1, 3, 5, 7, 9, 11]
print(binary_search(values, 7))
# 3

print(linear_search(values, 11))
# 5
```

### Dynamic Programming

```python
from pydsa import edit_distance, fib_tab

print(fib_tab(50))
# 12586269025

print(edit_distance("kitten", "sitting"))
# 3
```

### Greedy Algorithms

```python
from pydsa import activity_selection

start = [1, 3, 0, 5, 8, 5]
finish = [2, 4, 6, 7, 9, 9]
print(activity_selection(start, finish))
# [0, 1, 3, 4]
```

All public classes and functions are exposed from the top-level `pydsa` package.

## What's Included

| Module       | Components                                                                     | Purpose                                   |
| ------------ | ------------------------------------------------------------------------------ | ------------------------------------------ |
| `linear`     | `SinglyList[T]`, `DoublyList[T]`, `Stack[T]`, `Queue[T]`                       | Linear data structures                     |
| `trees`      | `BinaryTree[T]`, `BSTree[T]`, `AVLTree[T]`, `MinHeap[T]`, `MaxHeap[T]`, `Trie` | Trees, search trees, heaps, and a trie     |
| `hash`       | `HashTable[K, V]`                                                              | Hash table                                 |
| `graph`      | `Graph`                                                                        | Graph representation and operations        |
| `sorting`    | 9 algorithms                                                                   | Sorting                                    |
| `searching`  | 4 algorithms                                                                   | Searching                                  |
| `algorithms` | 10 algorithms                                                                  | Dynamic programming and greedy algorithms  |
| `exc`        | `PydsaError`, `EmptyError`                                                     | Project-specific exceptions                |

### Sorting

1. Bubble Sort
2. Selection Sort
3. Insertion Sort
4. Merge Sort
5. Quick Sort
6. Heap Sort
7. Counting Sort
8. Radix Sort
9. Bucket Sort

### Searching

1. Linear Search
2. Binary Search
3. Jump Search
4. Exponential Search

### Dynamic Programming and Greedy Algorithms

1. Fibonacci — memoization
2. Fibonacci — tabulation
3. 0/1 Knapsack
4. Longest Common Subsequence
5. Coin Change
6. Edit Distance
7. Activity Selection
8. Job Sequencing
9. Fractional Knapsack
10. Huffman Coding

## Code Quality

| Tool           | Purpose                          |
| -------------- | --------------------------------- |
| ruff           | Linting and formatting            |
| mypy           | Static type checking (strict)     |
| interrogate    | Docstring coverage (100%)         |
| pytest         | Testing                           |
| GitHub Actions | Continuous integration            |

Run the checks locally:

```bash
ruff check .
ruff format . --check
mypy pydsa
interrogate pydsa
pytest tests -v
```

The CI workflow runs these checks against Python 3.12 and Python 3.13.

## Tests

Tests are organized to mirror the package structure:

```text
tests/
├── algorithms/
├── graph/
├── hash/
├── linear/
├── searching/
├── sorting/
└── trees/
```

The suite covers normal behavior, edge cases, and structural invariants — including regression tests for bugs found during development (e.g., adjacency-list mutation during iteration in `Graph.remove_vertex`, and an empty-path edge case in `BinaryTree.insert`).

```bash
pytest tests -v
```

Docstring examples are also verified as executable tests:

```bash
pytest --doctest-modules pydsa -v
```

## Project Structure

```text
pydsa/
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── pydsa/
│   ├── _types.py
│   ├── algorithms/
│   ├── exc/
│   ├── graph/
│   ├── hash/
│   ├── linear/
│   ├── searching/
│   ├── sorting/
│   └── trees/
│
├── tests/
│   ├── algorithms/
│   ├── graph/
│   ├── hash/
│   ├── linear/
│   ├── searching/
│   ├── sorting/
│   └── trees/
│
├── pyproject.toml
├── README.md
└── LICENSE
```

## Scope & Status

`pydsa` is an educational project, not a production-ready replacement for Python's standard library or optimized DSA libraries. The implementations prioritize clarity over performance and do not carry the API stability, support, or long-term maintenance guarantees expected from production software. It is not under active development as a general-purpose library — the repository is meant for studying the implementations and their tests.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

**Sherzod Juraev**

`pydsa` is a personal educational project created to study data structures, algorithms, and software engineering practices through implementation.