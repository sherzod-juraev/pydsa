<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/branding/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/branding/logo.svg">
    <img alt="pydsa" src="assets/branding/logo.svg" width="300">
  </picture>
</p>

[![Release](https://img.shields.io/github/v/release/sherzod-juraev/pydsa)](https://github.com/sherzod-juraev/pydsa/releases)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Pydsa](https://github.com/sherzod-juraev/pydsa/actions/workflows/pydsa.yml/badge.svg)](https://github.com/sherzod-juraev/pydsa/actions/workflows/pydsa.yml)
[![Tests](https://github.com/sherzod-juraev/pydsa/actions/workflows/tests.yml/badge.svg)](https://github.com/sherzod-juraev/pydsa/actions/workflows/tests.yml)
[![Docs](https://github.com/sherzod-juraev/pydsa/actions/workflows/docs.yml/badge.svg)](https://github.com/sherzod-juraev/pydsa/actions/workflows/docs.yml)
[![Ruff](https://img.shields.io/badge/Ruff-enabled-brightgreen)](https://docs.astral.sh/ruff/)
[![mypy: strict](https://img.shields.io/badge/mypy-strict-blue.svg)](https://mypy.readthedocs.io/)
[![Interrogate](https://img.shields.io/badge/Interrogate-100%25-brightgreen)](https://interrogate.readthedocs.io/)
[![Nox](https://img.shields.io/badge/nox-sessions-blue)](https://nox.thea.codes/)

Classic data structures and algorithms in pure Python, built from scratch, fully typed, with no
runtime dependencies. The project exists to study how they work inside, not to replace what
Python already provides.

- **Documentation**: https://pydsa-edu.readthedocs.io
- **Source code**: https://github.com/sherzod-juraev/pydsa

## What this is, and what it is not

pydsa is a personal, educational project. Every implementation favors being readable and
correct over being fast.

- It is **not** a replacement for `list`, `dict`, `set`, `heapq`, `bisect` or `sorted`. They are
  faster, and you should use them in real code.
- It is **not** published on PyPI, and it makes no stability promise beyond its own tests.
- "From scratch" has a limit. Linked lists, trees and the `Stack` and `Queue` built on them
  manage their own nodes. Heaps, `Graph`, `Trie` and `HashTable` use a Python `list` or `dict`
  as their underlying array or mapping, because that is how those structures are built.

The reasoning behind these choices is in the
[Design Notes](https://pydsa-edu.readthedocs.io/en/latest/design/index.html).

## Quick example

Imports have two levels: a structure comes from its submodule, for example
`from pydsa.linear import Stack`, never from `pydsa` itself.

```python
from pydsa.exc import EmptyError
from pydsa.linear import Stack
from pydsa.searching import binary_search
from pydsa.sorting import merge_sort
from pydsa.trees import AVLTree

tree = AVLTree[int]()
for value in (5, 3, 8, 1, 4):
    tree.insert(value)
print(list(tree.inorder()))            # [1, 3, 4, 5, 8]
print(4 in tree)                       # True

ordered = merge_sort([5, 3, 8, 1, 4])
print(binary_search(ordered, 8))       # 4, the index of the target (-1 if it is absent)

stack = Stack[str]()
try:
    stack.pop()
except EmptyError as error:
    print(error)                       # Stack is empty
```

## Installation

pydsa requires Python 3.12 or newer and is installed directly from GitHub:

```bash
pip install git+https://github.com/sherzod-juraev/pydsa.git
```

To install a fixed release, add its tag after `@`, replacing `vX.Y.Z` with a tag from the
[Releases](https://github.com/sherzod-juraev/pydsa/releases) page:

```bash
pip install git+https://github.com/sherzod-juraev/pydsa.git@vX.Y.Z
```

## What's inside

| Submodule         |                              Contents                               |
|:------------------|:-------------------------------------------------------------------:|
| `pydsa.linear`    |             SinglyList, DoublyList, Stack, Queue                    |
| `pydsa.trees`     |      BinaryTree, BSTree, AVLTree, MinHeap, MaxHeap, Trie            |
| `pydsa.hash`      |                           HashTable                                 |
| `pydsa.graph`     |                             Graph                                   |
| `pydsa.sorting`   | Bubble, selection, insertion, merge, quick, heap, counting, radix, bucket |
| `pydsa.searching` |           Linear, binary, jump and exponential search               |
| `pydsa.core`      |                BaseStructure, Comparable                            |
| `pydsa.exc`       |                  The `PydsaError` hierarchy                         |

## Upgrading from 1.x

Version 2.0 is a breaking release: the flat imports (`from pydsa import Stack`) and
`is_empty()` are gone, and some errors changed. The
[Changelog](https://pydsa-edu.readthedocs.io/en/latest/changelog.html) has a migration table.

## Documentation

- [Installation](https://pydsa-edu.readthedocs.io/en/latest/getting_started/installation.html)
- [Quickstart](https://pydsa-edu.readthedocs.io/en/latest/getting_started/quickstart.html)
- [API Reference](https://pydsa-edu.readthedocs.io/en/latest/api/index.html)
- [Design Notes](https://pydsa-edu.readthedocs.io/en/latest/design/index.html)
- [Changelog](https://pydsa-edu.readthedocs.io/en/latest/changelog.html)

## Development

The development setup, the Nox sessions, the CI and the project conventions are described in
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License. See [LICENSE](LICENSE) for details.
