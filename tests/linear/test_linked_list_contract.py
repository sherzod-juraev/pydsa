"""Behaviour every linked list must share, run against each concrete class."""

import random
from collections.abc import Iterable
from typing import Any

import pytest

from pydsa.core import BaseStructure
from pydsa.exc import EmptyError, IndexOutOfRangeError, PydsaError
from pydsa.linear.base import LinkedListBase
from pydsa.linear.doubly import DoublyList
from pydsa.linear.singly import SinglyList

type AnyList = LinkedListBase[Any, Any]
type ListType = type[AnyList]


@pytest.fixture(params=[SinglyList, DoublyList], ids=lambda cls: cls.__name__)
def list_type(request: pytest.FixtureRequest) -> ListType:
    return request.param  # type: ignore[no-any-return]


def make(list_type: ListType, values: Iterable[Any] = ()) -> AnyList:
    items = list_type()
    for value in values:
        items.insert_last(value)
    return items


def check_invariants(items: AnyList) -> None:
    """Walk the nodes and verify head, tail, length and (for doubly) prev links."""
    nodes = []
    node = items._head
    while node is not None:
        nodes.append(node)
        assert len(nodes) <= len(items), "chain is longer than the recorded length"
        node = node.next
    assert len(nodes) == len(items)
    assert items._tail is (nodes[-1] if nodes else None)
    if isinstance(items, DoublyList):
        if nodes:
            assert nodes[0].prev is None
        assert all(nodes[i].prev is nodes[i - 1] for i in range(1, len(nodes)))
        assert list(reversed(items)) == [n.value for n in reversed(nodes)]


class TestConstruction:
    def test_new_list_is_empty(self, list_type: ListType) -> None:
        items = list_type()
        assert len(items) == 0
        assert not items
        assert list(items) == []
        check_invariants(items)

    def test_is_a_base_structure_and_a_linked_list(self, list_type: ListType) -> None:
        items = list_type()
        assert isinstance(items, BaseStructure)
        assert isinstance(items, LinkedListBase)

    def test_non_empty_list_is_truthy(self, list_type: ListType) -> None:
        assert make(list_type, [1])

    def test_base_class_is_abstract(self) -> None:
        with pytest.raises(TypeError):
            LinkedListBase()  # type: ignore[abstract]


class TestInsertion:
    def test_insert_first_puts_values_at_the_front(self, list_type: ListType) -> None:
        items = list_type()
        for value in (1, 2, 3):
            items.insert_first(value)
        assert list(items) == [3, 2, 1]
        check_invariants(items)

    def test_insert_last_appends_in_order(self, list_type: ListType) -> None:
        items = list_type()
        for value in (1, 2, 3):
            items.insert_last(value)
        assert list(items) == [1, 2, 3]
        check_invariants(items)

    def test_insert_first_and_last_can_be_mixed(self, list_type: ListType) -> None:
        items = list_type()
        items.insert_last(2)
        items.insert_first(1)
        items.insert_last(3)
        items.insert_first(0)
        assert list(items) == [0, 1, 2, 3]
        check_invariants(items)

    def test_first_insertion_sets_both_ends(self, list_type: ListType) -> None:
        for insert in ("insert_first", "insert_last"):
            items = list_type()
            getattr(items, insert)(7)
            assert items.get_first() == items.get_last() == 7
            check_invariants(items)

    @pytest.mark.parametrize("index", range(-4, 5))
    def test_insert_at_matches_list_insert(self, list_type: ListType, index: int) -> None:
        items = make(list_type, [10, 20, 30, 40])
        model = [10, 20, 30, 40]
        items.insert_at(index, 99)
        model.insert(index, 99)
        assert list(items) == model
        assert len(items) == 5
        check_invariants(items)

    def test_insert_at_the_end_moves_the_tail(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2])
        items.insert_at(2, 3)
        assert items.get_last() == 3

    def test_insert_at_zero_moves_the_head(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2])
        items.insert_at(0, 0)
        assert items.get_first() == 0

    def test_insert_at_zero_into_empty_list(self, list_type: ListType) -> None:
        items = list_type()
        items.insert_at(0, 5)
        assert list(items) == [5]
        check_invariants(items)

    @pytest.mark.parametrize("index", [5, 6, 100, -5, -100])
    def test_insert_at_out_of_range_raises_and_changes_nothing(
        self, list_type: ListType, index: int
    ) -> None:
        items = make(list_type, [1, 2, 3, 4])
        with pytest.raises(IndexOutOfRangeError):
            items.insert_at(index, 99)
        assert list(items) == [1, 2, 3, 4]
        check_invariants(items)

    def test_insert_at_one_into_empty_list_raises(self, list_type: ListType) -> None:
        with pytest.raises(IndexOutOfRangeError):
            list_type().insert_at(1, 5)


class TestIndexing:
    def test_getitem_matches_list_for_every_valid_index(self, list_type: ListType) -> None:
        values = [5, 6, 7, 8, 9]
        items = make(list_type, values)
        for index in range(-5, 5):
            assert items[index] == values[index]

    @pytest.mark.parametrize("index", [5, 6, 100, -6, -100])
    def test_getitem_out_of_range_raises(self, list_type: ListType, index: int) -> None:
        with pytest.raises(IndexOutOfRangeError):
            make(list_type, [1, 2, 3, 4, 5])[index]

    def test_getitem_on_empty_list_raises(self, list_type: ListType) -> None:
        for index in (0, -1):
            with pytest.raises(IndexOutOfRangeError):
                list_type()[index]

    def test_out_of_range_error_is_an_index_error_and_a_pydsa_error(
        self, list_type: ListType
    ) -> None:
        items = make(list_type, [1])
        with pytest.raises(IndexError):
            items[1]
        with pytest.raises(PydsaError):
            items[1]

    def test_out_of_range_message_names_type_index_and_length(self, list_type: ListType) -> None:
        with pytest.raises(IndexOutOfRangeError) as info:
            make(list_type, [1, 2])[5]
        assert str(info.value) == f"{list_type.__name__} index 5 out of range for length 2"

    def test_get_at_is_the_same_as_getitem(self, list_type: ListType) -> None:
        items = make(list_type, [4, 5, 6])
        assert [items.get_at(i) for i in (-3, -1, 0, 2)] == [4, 6, 4, 6]
        with pytest.raises(IndexOutOfRangeError):
            items.get_at(3)

    def test_get_first_and_get_last_do_not_remove(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        assert (items.get_first(), items.get_last()) == (1, 3)
        assert len(items) == 3

    def test_get_first_and_get_last_on_single_element(self, list_type: ListType) -> None:
        items = make(list_type, [9])
        assert items.get_first() == items.get_last() == 9

    @pytest.mark.parametrize("getter", ["get_first", "get_last"])
    def test_getters_on_empty_list_raise_empty_error(
        self, list_type: ListType, getter: str
    ) -> None:
        with pytest.raises(EmptyError, match=f"{list_type.__name__} is empty"):
            getattr(list_type(), getter)()

    def test_get_last_follows_the_tail_after_changes(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        items.insert_last(4)
        assert items.get_last() == 4
        items.remove_last()
        assert items.get_last() == 3
        items.insert_first(0)
        assert items.get_last() == 3

    def test_get_last_reads_the_tail_without_walking(
        self, list_type: ListType, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        items = make(list_type, range(50))

        def forbidden(self: AnyList, index: int, /) -> Any:
            raise AssertionError("get_last must not walk the chain")

        monkeypatch.setattr(list_type, "_node_at", forbidden)
        assert items.get_last() == 49


class TestRemoveFirstAndLast:
    def test_remove_first_returns_values_front_to_back(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        assert [items.remove_first() for _ in range(3)] == [1, 2, 3]
        assert len(items) == 0
        check_invariants(items)

    def test_remove_last_returns_values_back_to_front(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        assert [items.remove_last() for _ in range(3)] == [3, 2, 1]
        assert len(items) == 0
        check_invariants(items)

    def test_remove_first_leaves_the_rest_in_order(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        items.remove_first()
        assert list(items) == [2, 3]
        assert items.get_first() == 2
        check_invariants(items)

    def test_remove_last_leaves_the_rest_in_order(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        items.remove_last()
        assert list(items) == [1, 2]
        assert items.get_last() == 2
        check_invariants(items)

    def test_list_is_reusable_after_its_last_element_is_removed(self, list_type: ListType) -> None:
        for remove in ("remove_first", "remove_last"):
            items = make(list_type, [1])
            getattr(items, remove)()
            check_invariants(items)
            items.insert_last(2)
            items.insert_first(1)
            assert list(items) == [1, 2]
            assert items.get_last() == 2
            check_invariants(items)

    def test_appending_after_remove_last_attaches_to_the_new_tail(
        self, list_type: ListType
    ) -> None:
        items = make(list_type, [1, 2, 3])
        items.remove_last()
        items.insert_last(9)
        assert list(items) == [1, 2, 9]
        check_invariants(items)

    @pytest.mark.parametrize("remove", ["remove_first", "remove_last"])
    def test_removing_from_an_empty_list_raises_empty_error(
        self, list_type: ListType, remove: str
    ) -> None:
        with pytest.raises(EmptyError, match=f"{list_type.__name__} is empty"):
            getattr(list_type(), remove)()

    def test_empty_error_is_a_pydsa_error(self, list_type: ListType) -> None:
        with pytest.raises(PydsaError):
            list_type().remove_first()


class TestRemoveAt:
    @pytest.mark.parametrize("index", range(-4, 4))
    def test_matches_list_pop(self, list_type: ListType, index: int) -> None:
        items = make(list_type, [10, 20, 30, 40])
        model = [10, 20, 30, 40]
        assert items.remove_at(index) == model.pop(index)
        assert list(items) == model
        check_invariants(items)

    def test_removing_the_ends_updates_head_and_tail(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3, 4])
        items.remove_at(0)
        items.remove_at(-1)
        assert (items.get_first(), items.get_last()) == (2, 3)
        check_invariants(items)

    def test_removing_every_element_one_by_one(self, list_type: ListType) -> None:
        items = make(list_type, range(6))
        while items:
            items.remove_at(len(items) // 2)
            check_invariants(items)
        assert len(items) == 0

    @pytest.mark.parametrize("index", [4, 5, 100, -5, -100])
    def test_out_of_range_raises_and_changes_nothing(self, list_type: ListType, index: int) -> None:
        items = make(list_type, [1, 2, 3, 4])
        with pytest.raises(IndexOutOfRangeError):
            items.remove_at(index)
        assert list(items) == [1, 2, 3, 4]

    def test_empty_list_raises_index_error_not_empty_error(self, list_type: ListType) -> None:
        with pytest.raises(IndexOutOfRangeError):
            list_type().remove_at(0)


class TestRemoveValue:
    def test_removes_only_the_first_occurrence(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 1, 3, 1])
        assert items.remove(1) is True
        assert list(items) == [2, 1, 3, 1]
        check_invariants(items)

    def test_missing_value_returns_false_and_changes_nothing(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        assert items.remove(9) is False
        assert list(items) == [1, 2, 3]

    def test_empty_list_returns_false(self, list_type: ListType) -> None:
        assert list_type().remove(1) is False

    @pytest.mark.parametrize("value", [1, 2, 3, 4])
    def test_head_middle_and_tail_values(self, list_type: ListType, value: int) -> None:
        items = make(list_type, [1, 2, 3, 4])
        assert items.remove(value) is True
        assert list(items) == [v for v in (1, 2, 3, 4) if v != value]
        check_invariants(items)
        assert items.get_first() == (2 if value == 1 else 1)
        assert items.get_last() == (3 if value == 4 else 4)

    def test_removing_the_only_element(self, list_type: ListType) -> None:
        items = make(list_type, [1])
        assert items.remove(1) is True
        assert len(items) == 0
        check_invariants(items)

    def test_repeated_removal_drains_duplicates(self, list_type: ListType) -> None:
        items = make(list_type, [7, 7, 7])
        assert [items.remove(7) for _ in range(4)] == [True, True, True, False]

    def test_equal_but_distinct_objects_match(self, list_type: ListType) -> None:
        items = make(list_type, [(1, 2), (3, 4)])
        assert items.remove((3, 4)) is True
        assert list(items) == [(1, 2)]

    def test_appending_after_removing_the_tail_value_works(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        items.remove(3)
        items.insert_last(4)
        assert list(items) == [1, 2, 4]
        check_invariants(items)


class TestSearch:
    def test_contains(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        assert 2 in items
        assert 9 not in items
        assert 1 not in list_type()

    def test_index_of_returns_the_first_match(self, list_type: ListType) -> None:
        items = make(list_type, [5, 6, 5, 7])
        assert items.index_of(5) == 0
        assert items.index_of(7) == 3

    def test_index_of_missing_value_is_minus_one(self, list_type: ListType) -> None:
        assert make(list_type, [1, 2]).index_of(9) == -1
        assert list_type().index_of(1) == -1

    def test_count(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 1, 1])
        assert items.count(1) == 3
        assert items.count(2) == 1
        assert items.count(9) == 0
        assert list_type().count(1) == 0

    def test_none_is_an_ordinary_value(self, list_type: ListType) -> None:
        items = make(list_type, [1, None, 2])
        assert None in items
        assert items.index_of(None) == 1
        assert items.count(None) == 1


class TestIteration:
    def test_yields_values_in_order(self, list_type: ListType) -> None:
        assert list(make(list_type, [3, 1, 2])) == [3, 1, 2]

    def test_can_be_iterated_repeatedly(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        assert list(items) == list(items) == [1, 2, 3]

    def test_iterators_are_independent(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        first, second = iter(items), iter(items)
        assert next(first) == 1
        assert next(first) == 2
        assert next(second) == 1

    def test_empty_list_yields_nothing(self, list_type: ListType) -> None:
        assert list(list_type()) == []


class TestReverse:
    @pytest.mark.parametrize("size", range(7))
    def test_matches_list_reverse(self, list_type: ListType, size: int) -> None:
        items = make(list_type, range(size))
        items.reverse()
        assert list(items) == list(reversed(range(size)))
        check_invariants(items)

    def test_reversing_twice_restores_the_order(self, list_type: ListType) -> None:
        items = make(list_type, range(5))
        items.reverse()
        items.reverse()
        assert list(items) == [0, 1, 2, 3, 4]
        check_invariants(items)

    def test_head_and_tail_swap(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        items.reverse()
        assert (items.get_first(), items.get_last()) == (3, 1)

    def test_list_stays_fully_usable_after_reversing(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        items.reverse()
        items.insert_last(0)
        items.insert_first(9)
        assert list(items) == [9, 3, 2, 1, 0]
        assert items.remove_last() == 0
        assert items.remove_first() == 9
        assert list(items) == [3, 2, 1]
        check_invariants(items)


class TestCopy:
    def test_copy_has_equal_contents_and_same_type(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        clone = items.copy()
        assert type(clone) is list_type
        assert list(clone) == [1, 2, 3]
        assert clone is not items
        check_invariants(clone)

    def test_copy_of_an_empty_list_is_empty(self, list_type: ListType) -> None:
        clone = list_type().copy()
        assert len(clone) == 0
        check_invariants(clone)

    def test_changing_the_copy_leaves_the_original_alone(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        clone = items.copy()
        clone.insert_last(4)
        clone.remove_first()
        assert list(items) == [1, 2, 3]

    def test_changing_the_original_leaves_the_copy_alone(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        clone = items.copy()
        items.clear()
        assert list(clone) == [1, 2, 3]

    def test_copy_is_shallow(self, list_type: ListType) -> None:
        shared = [1, 2]
        items = make(list_type, [shared])
        assert items.copy().get_first() is shared


class TestClear:
    def test_clear_empties_the_list(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        items.clear()
        assert len(items) == 0
        assert not items
        assert list(items) == []
        check_invariants(items)

    def test_cleared_list_is_empty_for_getters(self, list_type: ListType) -> None:
        items = make(list_type, [1])
        items.clear()
        with pytest.raises(EmptyError):
            items.get_first()
        with pytest.raises(EmptyError):
            items.remove_last()

    def test_list_is_reusable_after_clear(self, list_type: ListType) -> None:
        items = make(list_type, [1, 2, 3])
        items.clear()
        items.insert_last(7)
        items.insert_first(6)
        assert list(items) == [6, 7]
        check_invariants(items)

    def test_clear_is_idempotent(self, list_type: ListType) -> None:
        items = list_type()
        items.clear()
        items.clear()
        assert len(items) == 0


class TestMiddle:
    @pytest.mark.parametrize("size", range(1, 9))
    def test_middle_of_every_size(self, list_type: ListType, size: int) -> None:
        items = make(list_type, range(size))
        expected: Any = size // 2 if size % 2 else (size // 2 - 1, size // 2)
        assert items.middle() == expected

    def test_middle_of_empty_list_raises(self, list_type: ListType) -> None:
        with pytest.raises(EmptyError):
            list_type().middle()

    def test_middle_does_not_modify_the_list(self, list_type: ListType) -> None:
        items = make(list_type, range(4))
        items.middle()
        assert list(items) == [0, 1, 2, 3]


class TestHasCycle:
    @pytest.mark.parametrize("size", [0, 1, 2, 5])
    def test_ordinary_lists_have_no_cycle(self, list_type: ListType, size: int) -> None:
        assert make(list_type, range(size)).has_cycle() is False

    @pytest.mark.parametrize("target", ["head", "middle"])
    def test_a_looped_chain_is_detected(self, list_type: ListType, target: str) -> None:
        items = make(list_type, range(6))
        tail = items._tail
        assert tail is not None
        tail.next = items._head if target == "head" else items._node_at(2)
        assert items.has_cycle() is True

    def test_a_single_node_pointing_at_itself_is_detected(self, list_type: ListType) -> None:
        items = make(list_type, [1])
        node = items._head
        assert node is not None
        node.next = node
        assert items.has_cycle() is True


class TestAgainstPythonList:
    OPERATIONS = (
        "insert_first",
        "insert_last",
        "insert_at",
        "remove_first",
        "remove_last",
        "remove_at",
        "remove",
        "reverse",
    )

    @pytest.mark.parametrize("seed", range(15))
    def test_random_operations_match_a_python_list(self, list_type: ListType, seed: int) -> None:
        rng = random.Random(seed)
        items = list_type()
        model: list[int] = []
        for _ in range(300):
            operation = rng.choice(self.OPERATIONS)
            size = len(model)
            value = rng.randrange(20)
            if operation == "insert_first":
                items.insert_first(value)
                model.insert(0, value)
            elif operation == "insert_last":
                items.insert_last(value)
                model.append(value)
            elif operation == "insert_at":
                index = rng.randint(-size, size)
                items.insert_at(index, value)
                model.insert(index, value)
            elif operation == "remove_first":
                if model:
                    assert items.remove_first() == model.pop(0)
                else:
                    with pytest.raises(EmptyError):
                        items.remove_first()
            elif operation == "remove_last":
                if model:
                    assert items.remove_last() == model.pop()
                else:
                    with pytest.raises(EmptyError):
                        items.remove_last()
            elif operation == "remove_at":
                if model:
                    index = rng.randint(-size, size - 1)
                    assert items.remove_at(index) == model.pop(index)
                else:
                    with pytest.raises(IndexOutOfRangeError):
                        items.remove_at(0)
            elif operation == "remove":
                assert items.remove(value) is (value in model)
                if value in model:
                    model.remove(value)
            else:
                items.reverse()
                model.reverse()

            assert list(items) == model
            assert len(items) == len(model)
            probe = rng.randrange(20)
            assert items.index_of(probe) == (model.index(probe) if probe in model else -1)
            assert items.count(probe) == model.count(probe)
            if model:
                assert items.get_first() == model[0]
                assert items.get_last() == model[-1]
            check_invariants(items)
