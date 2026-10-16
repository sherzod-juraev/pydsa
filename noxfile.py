"""Nox sessions: the quality checks that run locally and in the CI.

Run ``nox -l`` to list the sessions and ``nox`` to run the default ones.
"""

import shutil
import zipfile
from pathlib import Path

import nox

PYTHON_VERSIONS = ["3.12", "3.13", "3.14"]
DEFAULT_VERSION = "3.13"

_SOURCE_PATHS = ["pydsa", "tests", "noxfile.py"]
_DOCS_SOURCE = "docs/source"
_DOCS_HTML = "docs/build/html"
_DOCS_LINKCHECK = "docs/build/linkcheck"

_WHEEL_REQUIRED = [
    "pydsa/py.typed",
    "pydsa/__init__.py",
    "pydsa/__init__.pyi",
    *(f"pydsa/{package}/__init__.pyi" for package in ("core", "linear", "trees", "sorting")),
]
_WHEEL_FORBIDDEN_PREFIXES = ("tests/", "docs/")

# Runs inside the session, from a folder outside the repository, against the installed wheel.
_SMOKE_TEST = """
from pathlib import Path

import pydsa
from pydsa.linear import Stack

location = Path(pydsa.__file__).resolve()
assert "site-packages" in location.parts, f"pydsa was not imported from site-packages: {location}"
assert isinstance(pydsa.__version__, str)

stack = Stack[int]()
stack.push(1)
assert stack.pop() == 1
print("pydsa", pydsa.__version__, "imported from", location.parent)
"""


nox.options.sessions = ["lint", "types", "docstrings", "tests", "docs", "package"]
nox.options.error_on_external_run = True


def _check_wheel_contents(session: nox.Session, wheel: Path) -> None:
    """Fail the session if the wheel lacks files users need or ships files they do not.

    Parameters
    ----------
    session : nox.Session
        Session that reports the error.
    wheel : Path
        Wheel file to inspect.
    """
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()

    problems = [f"missing {name}" for name in _WHEEL_REQUIRED if name not in names]
    if not any(name.endswith(".dist-info/licenses/LICENSE") for name in names):
        problems.append("missing the LICENSE file in the metadata")
    problems += [
        f"unexpected {name}" for name in names if name.startswith(_WHEEL_FORBIDDEN_PREFIXES)
    ]

    if problems:
        session.error(f"{wheel.name}: " + "; ".join(problems))


@nox.session(python=DEFAULT_VERSION)
def lint(session: nox.Session) -> None:
    """Check the code style and the formatting with ruff."""
    session.install(".[dev]")
    session.run("ruff", "check", *_SOURCE_PATHS)
    session.run("ruff", "format", "--check", *_SOURCE_PATHS)


@nox.session(python=DEFAULT_VERSION)
def types(session: nox.Session) -> None:
    """Check the types with mypy in strict mode."""
    session.install(".[dev]")
    session.run("mypy", "pydsa")
    session.run("mypy", "tests")


@nox.session(python=DEFAULT_VERSION)
def docstrings(session: nox.Session) -> None:
    """Check that the docstring coverage of the package is 100%."""
    session.install(".[dev]")
    session.run("interrogate", "pydsa")
    session.run("pytest", "--doctest-modules", "pydsa")


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite on every supported Python version.

    Arguments after ``--`` are passed to pytest, for example ``nox -s tests -- -k tree``.
    """
    session.install(".[dev]")
    session.run("pytest", *session.posargs)


@nox.session(python=DEFAULT_VERSION)
def docs(session: nox.Session) -> None:
    """Check the style of the documentation and build it with warnings as errors."""
    session.install(".[docs]")
    session.run("sphinx-lint", _DOCS_SOURCE)
    session.run("doc8", _DOCS_SOURCE)
    session.run("rstcheck", "--recursive", _DOCS_SOURCE)
    session.run("sphinx-build", "-b", "html", "-W", "--keep-going", "-E", _DOCS_SOURCE, _DOCS_HTML)


@nox.session(python=DEFAULT_VERSION)
def linkcheck(session: nox.Session) -> None:
    """Check that every link in the documentation resolves.

    It needs the network and is slow, so it is not one of the default sessions.
    """
    session.install(".[docs]")
    session.run("sphinx-build", "-b", "linkcheck", "-E", _DOCS_SOURCE, _DOCS_LINKCHECK)


@nox.session(python=DEFAULT_VERSION)
def package(session: nox.Session) -> None:
    """Build the wheel, check its contents and import an installed copy of it."""
    session.install("build")
    dist = Path(session.create_tmp()) / "dist"
    # Leftovers of an earlier build would be packed into the new wheel as they are.
    for leftover in (dist, Path("build"), *Path().glob("*.egg-info")):
        shutil.rmtree(leftover, ignore_errors=True)
    session.run("python", "-m", "build", "--wheel", "--outdir", str(dist))

    wheels = list(dist.glob("*.whl"))
    if len(wheels) != 1:
        session.error(f"expected exactly one wheel, found {len(wheels)}")
    _check_wheel_contents(session, wheels[0])

    session.install(str(wheels[0]))
    session.chdir(session.create_tmp())
    session.run("python", "-c", _SMOKE_TEST)
