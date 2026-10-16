# Contributing

> [!NOTE]
> This is a personal, educational project. I am not
> actively seeking contributors at this time.

However, this project is open-source under the
[MIT License](LICENSE), and you are **welcome to**:

- **Fork** this repository.
- **Copy** the code.
- **Modify** it for your own needs.
- **Develop** your own version independently.

If you build something interesting, I would love to hear about it.

The rest of this file is also a map of the project: where things are, how to check them, and
how a new structure or a release is done.

## Quick start

```bash
git clone https://github.com/sherzod-juraev/pydsa.git
cd pydsa
pip install nox
nox
```

`nox` runs every default session (see [Nox sessions](#nox-sessions)) in isolated virtual
environments, the same way as the CI.

## Project structure

```text
pydsa/
├── .github/workflows/          # CI workflows
├── assets/branding/            # Logos
├── docs/source/                # Sphinx documentation
│   ├── getting_started/        # Installation, quickstart
│   ├── api/                    # API reference, one folder or page per submodule
│   └── design/                 # Design notes
├── pydsa/                      # Source code
│   ├── core/                   # BaseStructure, Comparable
│   ├── linear/                 # Linked lists, Stack, Queue
│   ├── trees/                  # Binary trees, BST, AVL, heaps, Trie
│   ├── sorting/                # Sorting algorithms
│   ├── exc.py                  # Exception hierarchy
│   ├── graph.py                # Graph
│   ├── searching.py            # Searching algorithms
│   └── hash.py                 # HashTable
├── tests/                      # Test suite, mirrors pydsa/
├── .readthedocs.yaml           # Read the Docs config
├── CONTRIBUTING.md             # This file
├── LICENSE                     # MIT License
├── noxfile.py                  # Nox sessions
├── pyproject.toml              # Project metadata and tool config
└── README.md                   # Project overview
```

## Development setup

### Requirements

- Python 3.12, 3.13 and 3.14. Install all three to run the whole Nox matrix, or run a single
  version, for example `nox -s tests-3.13`.

### Optional extras

The project defines the following extras in [pyproject.toml](pyproject.toml).

| Extra   |                      Purpose                      |
|---------|:-------------------------------------------------:|
| `dev`   |     mypy, ruff, pytest, interrogate (no Nox)      |
| `docs`  |           Sphinx and documentation tools          |
| `live`  |   Live documentation preview (Sphinx autobuild)   |
| `all`   |                 Everything above                  |

Nox itself is installed on its own, with `pip install nox`.

### Setup

```bash
git clone https://github.com/sherzod-juraev/pydsa.git
cd pydsa
```

Install what you need:

- Nox (recommended, runs everything in isolated environments):

```bash
pip install nox
```

- Development dependencies, to run a tool directly in your own environment:

```bash
pip install -e ".[dev]"
```

- Documentation tools:

```bash
pip install -e ".[docs]"
```

- Live documentation preview:

```bash
pip install -e ".[live]"
```

- Everything at once:

```bash
pip install -e ".[all]"
```

## Nox sessions

This project uses [Nox](https://nox.thea.codes/) to run all quality checks in isolated
environments. Nox creates a separate virtual environment for each session, installs the
required dependencies, and runs the configured commands.

| Session      |      Python      |                           What it runs                           |
|:-------------|:----------------:|:----------------------------------------------------------------:|
| `lint`       |       3.13       |                ruff check and ruff format --check                |
| `types`      |       3.13       |                mypy (strict) on `pydsa` and `tests`              |
| `docstrings` |       3.13       |     interrogate (100% coverage) and the docstring doctests       |
| `tests`      | 3.12, 3.13, 3.14 |                              pytest                              |
| `docs`       |       3.13       |          sphinx-lint, doc8, rstcheck, `sphinx-build -W`          |
| `linkcheck`  |       3.13       |        Sphinx linkcheck, validity of every link in the docs      |
| `package`    |       3.13       |  builds the wheel, checks its contents, imports an installed copy |

`nox` without arguments runs every session except `linkcheck`, which needs the network and is
slow.

```bash
nox -l                          # list all sessions
nox -s lint                     # run one session
nox -s tests-3.13               # run one session on one Python version
nox -s tests -- -k tree         # arguments after -- are passed to pytest
nox -R                          # reuse the existing virtual environments, much faster
```

## Continuous integration

Every workflow calls Nox, so a failure in the CI is reproduced locally with the same command.

| Workflow        | Runs on                     | Nox sessions                                   |
|:----------------|:----------------------------|:-----------------------------------------------|
| `pydsa.yml`     | push, pull request          | `lint`, `types`, `docstrings`, `package`       |
| `tests.yml`     | push, pull request          | `tests` on 3.12, 3.13, 3.14 (and 3.13 on Windows) |
| `docs.yml`      | push, pull request          | `docs`                                         |
| `linkcheck.yml` | weekly schedule, manual run | `linkcheck`                                    |

"Push" means a push to `main` or `dev`, and a pull request means one that targets `main`.
Read the Docs builds the documentation for the published site separately.

## Live documentation

Needs the `live` extra. To preview the documentation locally with auto-reload:

```bash
sphinx-autobuild docs/source docs/build/html/ # Linux/macOS
# or
sphinx-autobuild docs\source docs\build\html\ # Windows
```

Then open http://127.0.0.1:8000 in your browser and stop the server with `Ctrl+C`.

## Conventions

### Code

- Public imports have two levels only: `from pydsa.linear import Stack`, never
  `from pydsa import Stack`. Every package uses a lazy-loading `__init__.py` together with an
  `__init__.pyi` stub (`as` re-export style).
- Every structure derives from `BaseStructure`. It provides `len()`, truthiness and `clear()`,
  so there is no `is_empty` method. Code shared by several structures goes into a private
  family base (`LinkedListBase`, `HeapBase`, `BinaryTreeBase`, `SearchTreeBase`), and a base is
  shared only when the algorithm really is shared.
- Errors come from the hierarchy in `pydsa/exc.py`, starting at `PydsaError`. An error that
  stands in for a built-in one also derives from it (`KeyError`, `IndexError`, `ValueError`).
- Elements that must be ordered are bounded by `Comparable`.
- Everything is checked by mypy in strict mode, ruff (line length 100) and interrogate
  (100% docstring coverage, private members included).

### Docstrings

- NumPy style. The docstring explains the behavior and does not repeat the code or the
  signature.
- Every package `__init__.py` has a short module docstring in the same style: what the package
  exposes, and that everything is imported lazily.
- A class docstring holds a `Time Complexity Summary` table, and examples are doctests. They
  run in the `docstrings` session, so they must stay correct.

### Tests

- `tests/` mirrors `pydsa/`.
- Tests are grouped in classes by behavior. Randomized tests compare a structure with a
  reference model (`set`, `dict`, `heapq`), and structural invariants (BST order, AVL balance)
  are checked after every operation.
- Every package has an `__init__` test that checks the lazy loading and the exported names.
- A test file covers the behavior of its own layer and does not repeat what lower layers
  already guarantee.

### Commits and versions

- Commits follow [Conventional Commits](https://www.conventionalcommits.org/): `feat`, `fix`,
  `docs`, `test`, `build`, `refactor` and `chore`, with a body that explains what changed and
  why.
- Work happens on `dev`. `main` receives a merge only when all checks pass.
- `__version__` in `pydsa/__init__.py` is the single source of truth, `pyproject.toml` and the
  docs read it. It changes only when the public API changes: a breaking change is a MAJOR bump,
  a new structure or function is a MINOR bump, and housekeeping commits do not change it.
- Every release gets an entry in `docs/source/changelog.rst`.

## Adding a structure or an algorithm

1. Decide the algorithm and the architecture first: which base class, and whether a shared
   family base is justified.
2. Implement it in the right package under `pydsa/`, and add its name to the package's lazy
   `__init__.py` and `__init__.pyi`.
3. Write the docstrings following the conventions above.
4. Write the tests in `tests/`, including the lazy-loading `__init__` test.
5. Add the documentation: a page under `docs/source/api/`, a card on the index of its group, a
   row in the README table, and an example in the quickstart if it is a new kind of structure.
6. Run `nox` until every session passes.

## Releasing

1. Run `nox` on `dev`, and make sure the CI is green.
2. Bump `__version__` in `pydsa/__init__.py` if the public API changed, and add the entry to
   `docs/source/changelog.rst`.
3. Merge `dev` into `main` and push.
4. Create the tag `vX.Y.Z` on `main` and a GitHub release titled `vX.Y.Z`.
5. Check that the Read the Docs build is green.
