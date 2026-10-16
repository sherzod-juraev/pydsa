import ast
import importlib
import subprocess
import sys
from pathlib import Path

import pytest

import pydsa.linear
from pydsa.linear.doubly import DoublyList
from pydsa.linear.queue import Queue
from pydsa.linear.singly import SinglyList
from pydsa.linear.stack import Stack

PUBLIC_NAMES = {"DoublyList", "Queue", "SinglyList", "Stack"}
MODULE_VARS = vars(pydsa.linear)


def run_in_fresh_interpreter(code: str) -> str:
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


class TestPublicApi:
    def test_all_lists_the_public_names(self) -> None:
        assert set(MODULE_VARS["__all__"]) == PUBLIC_NAMES

    def test_all_has_no_duplicates(self) -> None:
        names = MODULE_VARS["__all__"]
        assert len(names) == len(set(names))

    def test_lazy_table_matches_all(self) -> None:
        assert set(MODULE_VARS["_LAZY_IMPORTS"]) == set(MODULE_VARS["__all__"])

    @pytest.mark.parametrize("name", sorted(PUBLIC_NAMES))
    def test_every_public_name_resolves_to_a_class(self, name: str) -> None:
        assert isinstance(getattr(pydsa.linear, name), type)

    @pytest.mark.parametrize(
        ("name", "expected"),
        [
            ("SinglyList", SinglyList),
            ("DoublyList", DoublyList),
            ("Stack", Stack),
            ("Queue", Queue),
        ],
    )
    def test_names_resolve_to_the_real_classes(self, name: str, expected: type) -> None:
        assert getattr(pydsa.linear, name) is expected

    def test_from_import_works(self) -> None:
        namespace: dict[str, object] = {}
        exec("from pydsa.linear import SinglyList, DoublyList, Stack, Queue", namespace)
        assert namespace["SinglyList"] is SinglyList

    def test_dir_lists_the_public_names(self) -> None:
        assert set(dir(pydsa.linear)) == PUBLIC_NAMES

    def test_dunder_dir_returns_sorted_names(self) -> None:
        assert MODULE_VARS["__dir__"]() == sorted(PUBLIC_NAMES)

    def test_star_import_exposes_exactly_the_public_names(self) -> None:
        namespace: dict[str, object] = {}
        exec("from pydsa.linear import *", namespace)
        assert {name for name in namespace if not name.startswith("__")} == PUBLIC_NAMES

    def test_lazy_table_points_to_real_symbols(self) -> None:
        for name, (module_name, symbol_name) in MODULE_VARS["_LAZY_IMPORTS"].items():
            module = importlib.import_module(f"pydsa.linear.{module_name}")
            assert hasattr(module, symbol_name), name


class TestUnknownAttribute:
    def test_raises_attribute_error(self) -> None:
        with pytest.raises(AttributeError, match="no attribute 'Missing'"):
            pydsa.linear.Missing  # type: ignore[attr-defined] # noqa: B018

    def test_message_names_the_module_and_the_available_symbols(self) -> None:
        with pytest.raises(AttributeError) as info:
            pydsa.linear.Missing  # type: ignore[attr-defined] # noqa: B018
        message = str(info.value)
        assert "pydsa.linear" in message
        assert all(name in message for name in PUBLIC_NAMES)

    def test_hasattr_is_false(self) -> None:
        assert not hasattr(pydsa.linear, "Missing")

    def test_internal_base_class_is_not_public(self) -> None:
        assert not hasattr(pydsa.linear, "LinkedListBase")


class TestLazyImport:
    def test_importing_the_package_loads_no_submodule(self) -> None:
        output = run_in_fresh_interpreter(
            "import sys, pydsa.linear; "
            "print(sorted(m for m in sys.modules if m.startswith('pydsa.linear.')))"
        )
        assert output == "[]"

    def test_accessing_a_name_loads_only_what_it_needs(self) -> None:
        output = run_in_fresh_interpreter(
            "import sys, pydsa.linear; pydsa.linear.DoublyList; "
            "print(sorted(m.removeprefix('pydsa.linear.') for m in sys.modules "
            "if m.startswith('pydsa.linear.')))"
        )
        assert output == "['base', 'doubly']"

    def test_queue_pulls_in_the_singly_list_but_not_the_doubly_list(self) -> None:
        output = run_in_fresh_interpreter(
            "import sys, pydsa.linear; pydsa.linear.Queue; "
            "print('pydsa.linear.singly' in sys.modules, 'pydsa.linear.doubly' in sys.modules)"
        )
        assert output == "True False"


class TestStub:
    stub_tree = ast.parse(Path(str(pydsa.linear.__file__)).with_suffix(".pyi").read_text())

    def test_stub_re_exports_exactly_the_public_names(self) -> None:
        exported = {
            alias.name
            for node in self.stub_tree.body
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
            if alias.asname == alias.name
        }
        assert exported == PUBLIC_NAMES

    def test_stub_imports_point_to_real_symbols(self) -> None:
        for node in self.stub_tree.body:
            assert isinstance(node, ast.ImportFrom)
            module = importlib.import_module(f"pydsa.linear.{node.module}")
            for alias in node.names:
                assert hasattr(module, alias.name)
