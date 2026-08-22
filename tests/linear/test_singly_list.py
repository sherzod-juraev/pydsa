import pytest

from pydsa import SinglyList, EmptyError


@pytest.fixture
def empty_list() -> SinglyList[int]:
    return SinglyList[int]()


@pytest.fixture
def filled_list() -> SinglyList[int]:
    lst = SinglyList[int]()
    for v in [1, 2, 3, 4, 5]:
        lst.insert_last(v)
    return lst


class TestConstruction:
    def test_new_list_is_empty(self, empty_list: SinglyList[int]) -> None:
        assert empty_list.is_empty()
        assert len(empty_list) == 0
        assert bool(empty_list) is False

    def test_new_list_iterates_to_nothing(self, empty_list: SinglyList[int]) -> None:
        assert list(empty_list) == []


class TestInsertFirst:
    def test_into_empty(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_first(1)
        assert list(empty_list) == [1]
        assert len(empty_list) == 1
        assert empty_list.get_first() == 1
        assert empty_list.get_last() == 1

    def test_multiple_prepends_reverse_order(self, empty_list: SinglyList[int]) -> None:
        for v in [1, 2, 3]:
            empty_list.insert_first(v)
        assert list(empty_list) == [3, 2, 1]

    def test_updates_tail_only_when_was_empty(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_first(1)
        empty_list.insert_first(2)
        assert empty_list.get_last() == 1


class TestInsertLast:
    def test_into_empty(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_last(1)
        assert list(empty_list) == [1]
        assert empty_list.get_first() == 1
        assert empty_list.get_last() == 1

    def test_multiple_appends_preserve_order(self, empty_list: SinglyList[int]) -> None:
        for v in [1, 2, 3]:
            empty_list.insert_last(v)
        assert list(empty_list) == [1, 2, 3]

    def test_on_filled_list(self, filled_list: SinglyList[int]) -> None:
        filled_list.insert_last(6)
        assert list(filled_list) == [1, 2, 3, 4, 5, 6]
        assert filled_list.get_last() == 6


class TestInsertAt:
    def test_at_zero_equals_insert_first(self, filled_list: SinglyList[int]) -> None:
        filled_list.insert_at(0, 0)
        assert list(filled_list) == [0, 1, 2, 3, 4, 5]

    def test_at_length_equals_insert_last(self, filled_list: SinglyList[int]) -> None:
        filled_list.insert_at(len(filled_list), 6)
        assert list(filled_list) == [1, 2, 3, 4, 5, 6]

    def test_at_middle(self, filled_list: SinglyList[int]) -> None:
        filled_list.insert_at(2, 99)
        assert list(filled_list) == [1, 2, 99, 3, 4, 5]

    def test_negative_index(self, filled_list: SinglyList[int]) -> None:
        filled_list.insert_at(-1, 99)
        assert list(filled_list) == [1, 2, 3, 4, 99, 5]

    def test_updates_length(self, filled_list: SinglyList[int]) -> None:
        filled_list.insert_at(2, 99)
        assert len(filled_list) == 6

    @pytest.mark.parametrize("index", [6, -6])
    def test_out_of_range_raises(self, filled_list: SinglyList[int], index: int) -> None:
        with pytest.raises(IndexError):
            filled_list.insert_at(index, 99)

    def test_into_empty_at_zero(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_at(0, 1)
        assert list(empty_list) == [1]


class TestRemoveFirst:
    def test_raises_on_empty(self, empty_list: SinglyList[int]) -> None:
        with pytest.raises(EmptyError):
            empty_list.remove_first()

    def test_removes_and_returns_head(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.remove_first() == 1
        assert list(filled_list) == [2, 3, 4, 5]
        assert len(filled_list) == 4

    def test_down_to_single_element_clears_tail(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_last(1)
        empty_list.remove_first()
        assert empty_list.is_empty()
        with pytest.raises(EmptyError):
            empty_list.get_last()

    def test_insert_after_draining_to_empty(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_last(1)
        empty_list.remove_first()
        empty_list.insert_last(2)
        assert list(empty_list) == [2]
        assert empty_list.get_last() == 2


class TestRemoveLast:
    def test_raises_on_empty(self, empty_list: SinglyList[int]) -> None:
        with pytest.raises(EmptyError):
            empty_list.remove_last()

    def test_removes_and_returns_tail(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.remove_last() == 5
        assert list(filled_list) == [1, 2, 3, 4]
        assert filled_list.get_last() == 4

    def test_single_element_delegates_to_remove_first(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_last(1)
        assert empty_list.remove_last() == 1
        assert empty_list.is_empty()

    def test_tail_pointer_consistent_after_removal(self, filled_list: SinglyList[int]) -> None:
        filled_list.remove_last()
        filled_list.insert_last(99)
        assert list(filled_list) == [1, 2, 3, 4, 99]


class TestRemoveAt:
    def test_raises_on_out_of_range(self, filled_list: SinglyList[int]) -> None:
        with pytest.raises(IndexError):
            filled_list.remove_at(10)

    def test_at_zero_delegates_to_remove_first(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.remove_at(0) == 1
        assert list(filled_list) == [2, 3, 4, 5]

    def test_at_last_index_delegates_to_remove_last(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.remove_at(4) == 5
        assert list(filled_list) == [1, 2, 3, 4]

    def test_at_middle(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.remove_at(2) == 3
        assert list(filled_list) == [1, 2, 4, 5]

    def test_negative_index(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.remove_at(-2) == 4
        assert list(filled_list) == [1, 2, 3, 5]


class TestRemove:
    def test_raises_on_empty(self, empty_list: SinglyList[int]) -> None:
        with pytest.raises(EmptyError):
            empty_list.remove(1)

    def test_value_at_head(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.remove(1) is True
        assert list(filled_list) == [2, 3, 4, 5]

    def test_value_at_tail(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.remove(5) is True
        assert list(filled_list) == [1, 2, 3, 4]

    def test_value_in_middle(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.remove(3) is True
        assert list(filled_list) == [1, 2, 4, 5]

    def test_value_not_found_returns_false(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.remove(999) is False
        assert list(filled_list) == [1, 2, 3, 4, 5]

    def test_removes_only_first_occurrence(self, empty_list: SinglyList[int]) -> None:
        for v in [1, 2, 1, 3]:
            empty_list.insert_last(v)
        empty_list.remove(1)
        assert list(empty_list) == [2, 1, 3]

    def test_single_element_matching(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_last(1)
        assert empty_list.remove(1) is True
        assert empty_list.is_empty()


class TestGetters:
    def test_get_first_raises_on_empty(self, empty_list: SinglyList[int]) -> None:
        with pytest.raises(EmptyError):
            empty_list.get_first()

    def test_get_last_raises_on_empty(self, empty_list: SinglyList[int]) -> None:
        with pytest.raises(EmptyError):
            empty_list.get_last()

    def test_get_at_valid_index(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.get_at(2) == 3

    def test_get_at_negative_index(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.get_at(-1) == 5

    def test_get_at_out_of_range_raises(self, filled_list: SinglyList[int]) -> None:
        with pytest.raises(IndexError):
            filled_list.get_at(100)

    def test_getitem_matches_get_at(self, filled_list: SinglyList[int]) -> None:
        assert filled_list[3] == filled_list.get_at(3)


class TestIndexOfAndCount:
    def test_index_of_found(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.index_of(3) == 2

    def test_index_of_not_found(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.index_of(999) == -1

    def test_index_of_returns_first_match(self, empty_list: SinglyList[int]) -> None:
        for v in [1, 2, 1]:
            empty_list.insert_last(v)
        assert empty_list.index_of(1) == 0

    def test_count_multiple_occurrences(self, empty_list: SinglyList[int]) -> None:
        for v in [1, 2, 1, 1, 3]:
            empty_list.insert_last(v)
        assert empty_list.count(1) == 3

    def test_count_zero_when_absent(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.count(999) == 0


class TestContains:
    def test_true_when_present(self, filled_list: SinglyList[int]) -> None:
        assert 3 in filled_list

    def test_false_when_absent(self, filled_list: SinglyList[int]) -> None:
        assert 999 not in filled_list

    def test_false_on_empty(self, empty_list: SinglyList[int]) -> None:
        assert 1 not in empty_list


class TestReverse:
    def test_reverses_order(self, filled_list: SinglyList[int]) -> None:
        filled_list.reverse()
        assert list(filled_list) == [5, 4, 3, 2, 1]

    def test_head_and_tail_swap(self, filled_list: SinglyList[int]) -> None:
        filled_list.reverse()
        assert filled_list.get_first() == 5
        assert filled_list.get_last() == 1

    def test_empty_list_noop(self, empty_list: SinglyList[int]) -> None:
        empty_list.reverse()
        assert list(empty_list) == []

    def test_single_element_noop(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_last(1)
        empty_list.reverse()
        assert list(empty_list) == [1]

    def test_list_still_usable_after_reverse(self, filled_list: SinglyList[int]) -> None:
        filled_list.reverse()
        filled_list.insert_last(0)
        assert list(filled_list) == [5, 4, 3, 2, 1, 0]


class TestCopy:
    def test_copy_has_same_elements(self, filled_list: SinglyList[int]) -> None:
        copy = filled_list.copy()
        assert list(copy) == list(filled_list)
        assert copy is not filled_list

    def test_copy_of_empty_list(self, empty_list: SinglyList[int]) -> None:
        copy = empty_list.copy()
        assert copy.is_empty()

    def test_mutating_copy_does_not_affect_original(self, filled_list: SinglyList[int]) -> None:
        copy = filled_list.copy()
        copy.insert_last(99)
        assert 99 not in filled_list
        assert list(filled_list) == [1, 2, 3, 4, 5]


class TestClear:
    def test_clears_filled_list(self, filled_list: SinglyList[int]) -> None:
        filled_list.clear()
        assert filled_list.is_empty()
        assert len(filled_list) == 0

    def test_usable_after_clear(self, filled_list: SinglyList[int]) -> None:
        filled_list.clear()
        filled_list.insert_last(42)
        assert list(filled_list) == [42]


class TestHasCycle:
    def test_false_for_acyclic_list(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.has_cycle() is False

    def test_false_for_empty_list(self, empty_list: SinglyList[int]) -> None:
        assert empty_list.has_cycle() is False

    def test_false_for_single_element(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_last(1)
        assert empty_list.has_cycle() is False


class TestMiddle:
    def test_raises_on_empty(self, empty_list: SinglyList[int]) -> None:
        with pytest.raises(EmptyError):
            empty_list.middle()

    def test_odd_length_returns_single_value(self, filled_list: SinglyList[int]) -> None:
        assert filled_list.middle() == 3

    def test_even_length_returns_tuple(self, empty_list: SinglyList[int]) -> None:
        for v in [1, 2, 3, 4]:
            empty_list.insert_last(v)
        assert empty_list.middle() == (2, 3)

    def test_single_element(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_last(1)
        assert empty_list.middle() == 1

    def test_two_elements(self, empty_list: SinglyList[int]) -> None:
        empty_list.insert_last(1)
        empty_list.insert_last(2)
        assert empty_list.middle() == (1, 2)