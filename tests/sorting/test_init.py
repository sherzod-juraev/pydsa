import ast
import importlib
import subprocess
import sys
from pathlib import Path

import pytest

import pydsa.sorting

PUBLIC_NAMES = {
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "heap_sort",
    "counting_sort",
    "radix_sort",
    "bucket_sort",
}
MODULE_VARS = vars(pydsa.sorting)


def run_in_fresh_interpreter(code: str) -> str:
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


class TestPublicApi:
    def test_all_lists_exactly_the_public_names(self) -> None:
        assert set(MODULE_VARS["__all__"]) == PUBLIC_NAMES

    def test_all_has_no_duplicates(self) -> None:
        names = MODULE_VARS["__all__"]
        assert len(names) == len(set(names))

    def test_all_contains_names_not_filenames(self) -> None:
        assert not [n for n in MODULE_VARS["__all__"] if n.endswith(".py")]

    def test_lazy_table_matches_all(self) -> None:
        assert set(MODULE_VARS["_LAZY_IMPORTS"]) == set(MODULE_VARS["__all__"])

    @pytest.mark.parametrize("name", sorted(PUBLIC_NAMES))
    def test_every_public_name_is_a_function_with_that_name(self, name: str) -> None:
        function = getattr(pydsa.sorting, name)
        assert callable(function)
        assert function.__name__ == name

    def test_every_name_in_all_resolves(self) -> None:
        assert [n for n in MODULE_VARS["__all__"] if not hasattr(pydsa.sorting, n)] == []

    def test_dir_lists_the_public_names(self) -> None:
        assert set(dir(pydsa.sorting)) == PUBLIC_NAMES

    def test_star_import_exposes_exactly_the_public_names(self) -> None:
        namespace: dict[str, object] = {}
        exec("from pydsa.sorting import *", namespace)
        assert {name for name in namespace if not name.startswith("__")} == PUBLIC_NAMES

    def test_lazy_table_points_to_real_functions(self) -> None:
        for name, (module_name, symbol_name) in MODULE_VARS["_LAZY_IMPORTS"].items():
            module = importlib.import_module(f"pydsa.sorting.{module_name}")
            assert callable(getattr(module, symbol_name)), name

    def test_heap_sort_is_the_function_not_the_submodule(self) -> None:
        import types

        assert not isinstance(pydsa.sorting.heap_sort, types.ModuleType)


class TestUnknownAttribute:
    def test_raises_attribute_error(self) -> None:
        with pytest.raises(AttributeError, match="no attribute 'Missing'"):
            pydsa.sorting.Missing  # type: ignore[attr-defined] # noqa: B018

    def test_message_lists_the_available_symbols(self) -> None:
        with pytest.raises(AttributeError) as info:
            pydsa.sorting.Missing  # type: ignore[attr-defined] # noqa: B018
        message = str(info.value)
        assert "pydsa.sorting" in message
        assert all(name in message for name in PUBLIC_NAMES)

    def test_hasattr_is_false(self) -> None:
        assert not hasattr(pydsa.sorting, "Missing")


class TestLazyImport:
    def test_importing_the_package_loads_no_submodule(self) -> None:
        output = run_in_fresh_interpreter(
            "import sys, pydsa.sorting; "
            "print(sorted(m for m in sys.modules if m.startswith('pydsa.sorting.')))"
        )
        assert output == "[]"

    def test_accessing_a_name_loads_only_its_module(self) -> None:
        output = run_in_fresh_interpreter(
            "import sys, pydsa.sorting; pydsa.sorting.bubble_sort; "
            "print(sorted(m for m in sys.modules if m.startswith('pydsa.sorting.')))"
        )
        assert output == "['pydsa.sorting.elementary']"


class TestStub:
    stub_tree = ast.parse(Path(str(pydsa.sorting.__file__)).with_suffix(".pyi").read_text())

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
            module = importlib.import_module(f"pydsa.sorting.{node.module}")
            for alias in node.names:
                assert hasattr(module, alias.name)

    def test_stub_agrees_with_the_lazy_table(self) -> None:
        pairs = {
            alias.name: node.module
            for node in self.stub_tree.body
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        }
        table = {name: module for name, (module, _) in MODULE_VARS["_LAZY_IMPORTS"].items()}
        assert pairs == table
