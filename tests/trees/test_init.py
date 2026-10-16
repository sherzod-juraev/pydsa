import ast
import importlib
import subprocess
import sys
from pathlib import Path

import pytest

import pydsa.trees

PUBLIC_NAMES = {"AVLTree", "BSTree", "BinaryTree", "MaxHeap", "MinHeap", "Trie"}
MODULE_VARS = vars(pydsa.trees)


def run_in_fresh_interpreter(code: str) -> str:
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def loaded_after(statement: str) -> set[str]:
    output = run_in_fresh_interpreter(
        f"import sys, pydsa.trees; {statement}; "
        "print(sorted(m for m in sys.modules if m.startswith('pydsa.trees.')))"
    )
    return set(ast.literal_eval(output))


class TestPublicApi:
    def test_all_lists_exactly_the_public_names(self) -> None:
        assert set(MODULE_VARS["__all__"]) == PUBLIC_NAMES

    def test_all_has_no_duplicates(self) -> None:
        names = MODULE_VARS["__all__"]
        assert len(names) == len(set(names))

    def test_lazy_table_matches_all(self) -> None:
        assert set(MODULE_VARS["_LAZY_IMPORTS"]) == set(MODULE_VARS["__all__"])

    @pytest.mark.parametrize("name", sorted(PUBLIC_NAMES))
    def test_every_public_name_is_a_class_with_that_name(self, name: str) -> None:
        cls = getattr(pydsa.trees, name)
        assert isinstance(cls, type)
        assert cls.__name__ == name

    def test_internal_bases_are_not_public(self) -> None:
        for name in ("BinaryTreeBase", "SearchTreeBase", "HeapBase"):
            assert name not in MODULE_VARS["__all__"]
            assert not hasattr(pydsa.trees, name)

    def test_dir_lists_the_public_names(self) -> None:
        assert set(dir(pydsa.trees)) == PUBLIC_NAMES

    def test_dunder_dir_returns_sorted_names(self) -> None:
        assert MODULE_VARS["__dir__"]() == sorted(PUBLIC_NAMES)

    def test_star_import_exposes_exactly_the_public_names(self) -> None:
        namespace: dict[str, object] = {}
        exec("from pydsa.trees import *", namespace)
        assert {name for name in namespace if not name.startswith("__")} == PUBLIC_NAMES

    def test_lazy_table_points_to_real_classes(self) -> None:
        for name, (module_name, symbol_name) in MODULE_VARS["_LAZY_IMPORTS"].items():
            module = importlib.import_module(f"pydsa.trees.{module_name}")
            assert isinstance(getattr(module, symbol_name), type), name


class TestUnknownAttribute:
    def test_raises_attribute_error(self) -> None:
        with pytest.raises(AttributeError, match="no attribute 'Missing'"):
            pydsa.trees.Missing  # type: ignore[attr-defined] # noqa: B018

    def test_message_lists_the_available_symbols(self) -> None:
        with pytest.raises(AttributeError) as info:
            pydsa.trees.Missing  # type: ignore[attr-defined] # noqa: B018
        message = str(info.value)
        assert "pydsa.trees" in message
        assert all(name in message for name in PUBLIC_NAMES)

    def test_hasattr_is_false(self) -> None:
        assert not hasattr(pydsa.trees, "Missing")


class TestLazyImport:
    def test_importing_the_package_loads_no_submodule(self) -> None:
        assert loaded_after("pass") == set()

    def test_a_heap_loads_only_the_heap_module(self) -> None:
        assert loaded_after("pydsa.trees.MinHeap") == {"pydsa.trees.heap"}
        assert loaded_after("pydsa.trees.MaxHeap") == {"pydsa.trees.heap"}

    def test_the_trie_loads_only_its_own_module(self) -> None:
        assert loaded_after("pydsa.trees.Trie") == {"pydsa.trees.trie"}

    def test_a_tree_loads_only_its_module_and_the_shared_base(self) -> None:
        assert loaded_after("pydsa.trees.BinaryTree") == {
            "pydsa.trees.base",
            "pydsa.trees.binary_tree",
        }
        assert loaded_after("pydsa.trees.AVLTree") == {"pydsa.trees.base", "pydsa.trees.avl"}


class TestStub:
    stub_tree = ast.parse(Path(str(pydsa.trees.__file__)).with_suffix(".pyi").read_text())

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
            module = importlib.import_module(f"pydsa.trees.{node.module}")
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
