from collections.abc import Sized

import pytest

from pydsa.core.base import BaseStructure
from pydsa.exc import EmptyError, PydsaError


class Bag(BaseStructure):
    def __init__(self) -> None:
        self.items: list[int] = []

    def __len__(self) -> int:
        return len(self.items)

    def clear(self) -> None:
        self.items.clear()


class SubBag(Bag):
    pass


class TestAbstractContract:
    def test_base_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError, match="abstract"):
            BaseStructure()  # type: ignore[abstract]

    def test_missing_len_is_rejected(self) -> None:
        class NoLen(BaseStructure):
            def clear(self) -> None: ...

        with pytest.raises(TypeError, match="__len__"):
            NoLen()  # type: ignore[abstract]

    def test_missing_clear_is_rejected(self) -> None:
        class NoClear(BaseStructure):
            def __len__(self) -> int:
                return 0

        with pytest.raises(TypeError, match="clear"):
            NoClear()  # type: ignore[abstract]

    def test_complete_subclass_can_be_instantiated(self) -> None:
        assert isinstance(Bag(), BaseStructure)


class TestSizeAndTruthiness:
    def test_len_is_reported(self) -> None:
        bag = Bag()
        bag.items.extend([1, 2, 3])
        assert len(bag) == 3

    def test_empty_structure_is_falsy(self) -> None:
        assert not Bag()

    def test_non_empty_structure_is_truthy(self) -> None:
        bag = Bag()
        bag.items.append(1)
        assert bag

    def test_clear_makes_structure_falsy(self) -> None:
        bag = Bag()
        bag.items.append(1)
        bag.clear()
        assert len(bag) == 0
        assert not bag


class TestTyping:
    def test_structure_is_sized(self) -> None:
        assert isinstance(Bag(), Sized)

    def test_sized_structural_check_does_not_leak(self) -> None:
        assert not isinstance([], BaseStructure)


class TestCheckEmpty:
    def test_raises_when_empty(self) -> None:
        with pytest.raises(EmptyError):
            Bag()._ensure_not_empty()

    def test_message_names_the_structure_type(self) -> None:
        with pytest.raises(EmptyError, match=r"^Bag is empty$"):
            Bag()._ensure_not_empty()

    def test_message_uses_the_runtime_type(self) -> None:
        with pytest.raises(EmptyError, match=r"^SubBag is empty$"):
            SubBag()._ensure_not_empty()

    def test_caught_as_pydsa_error(self) -> None:
        with pytest.raises(PydsaError):
            Bag()._ensure_not_empty()

    def test_does_not_raise_when_not_empty(self) -> None:
        bag = Bag()
        bag.items.append(1)
        bag._ensure_not_empty()

    def test_raises_again_after_clear(self) -> None:
        bag = Bag()
        bag.items.append(1)
        bag.clear()
        with pytest.raises(EmptyError):
            bag._ensure_not_empty()
