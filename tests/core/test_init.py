import ast
import importlib
import subprocess
import sys
from pathlib import Path

import pytest

import pydsa.core
from pydsa.core.base import BaseStructure
from pydsa.core.protocols import Comparable

PUBLIC_NAMES = {"BaseStructure", "Comparable"}
MODULE_VARS = vars(pydsa.core)


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
    def test_every_public_name_resolves(self, name: str) -> None:
        assert getattr(pydsa.core, name) is not None

    def test_base_structure_is_the_real_class(self) -> None:
        assert pydsa.core.BaseStructure is BaseStructure

    def test_comparable_is_the_real_protocol(self) -> None:
        assert pydsa.core.Comparable is Comparable

    def test_dir_lists_the_public_names(self) -> None:
        assert set(dir(pydsa.core)) == PUBLIC_NAMES

    def test_dunder_dir_returns_sorted_names(self) -> None:
        assert MODULE_VARS["__dir__"]() == sorted(PUBLIC_NAMES)

    def test_star_import_exposes_exactly_the_public_names(self) -> None:
        namespace: dict[str, object] = {}
        exec("from pydsa.core import *", namespace)
        assert {name for name in namespace if not name.startswith("__")} == PUBLIC_NAMES


class TestUnknownAttribute:
    def test_raises_attribute_error(self) -> None:
        with pytest.raises(AttributeError, match="no attribute 'Missing'"):
            pydsa.core.Missing  # type: ignore[attr-defined]  # noqa: B018

    def test_message_names_the_module_and_the_available_symbols(self) -> None:
        with pytest.raises(AttributeError) as info:
            pydsa.core.Missing  # type: ignore[attr-defined]  # noqa: B018
        message = str(info.value)
        assert "pydsa.core" in message
        assert all(name in message for name in PUBLIC_NAMES)

    def test_hasattr_is_false(self) -> None:
        assert not hasattr(pydsa.core, "Missing")


class TestLazyImport:
    def test_importing_the_package_loads_no_submodule(self) -> None:
        output = run_in_fresh_interpreter(
            "import sys, pydsa.core; "
            "print('pydsa.core.base' in sys.modules, 'pydsa.core.protocols' in sys.modules)"
        )
        assert output == "False False"

    def test_accessing_a_name_loads_only_its_module(self) -> None:
        output = run_in_fresh_interpreter(
            "import sys, pydsa.core; pydsa.core.Comparable; "
            "print('pydsa.core.base' in sys.modules, 'pydsa.core.protocols' in sys.modules)"
        )
        assert output == "False True"


class TestStub:
    stub_tree = ast.parse(Path(str(pydsa.core.__file__)).with_suffix(".pyi").read_text())

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
            module = importlib.import_module(f"pydsa.core.{node.module}")
            for alias in node.names:
                assert hasattr(module, alias.name)
