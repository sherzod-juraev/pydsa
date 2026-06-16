import pytest
from pydsa import SinglyList
from pydsa.exc import EmptyError


class TestSinglyListInit:
    """__init__"""

    def test_EmptyError_list_has_zero_length(self):
        lst = SinglyList()
        assert len(lst) == 0

    def test_EmptyError_list_is_falsy(self):
        lst = SinglyList()
        assert not lst

    def test_EmptyError_list_is_EmptyError(self):
        lst = SinglyList()
        assert lst.is_empty()


class TestSinglyListInsertFirst:
    """insert_first"""

    def test_insert_into_EmptyError_list(self):
        lst = SinglyList()
        lst.insert_first(10)
        assert len(lst) == 1
        assert lst.get_first() == 10
        assert lst.get_last() == 10

    def test_insert_multiple(self):
        lst = SinglyList()
        lst.insert_first(30)
        lst.insert_first(20)
        lst.insert_first(10)
        assert len(lst) == 3
        assert lst.get_first() == 10
        assert lst.get_last() == 30

    def test_head_and_tail_same_for_single_element(self):
        lst = SinglyList()
        lst.insert_first(42)
        assert lst.get_first() == lst.get_last()

    def test_list_is_truthy_after_insert(self):
        lst = SinglyList()
        lst.insert_first(1)
        assert bool(lst)


class TestSinglyListInsertLast:
    """insert_last"""

    def test_insert_into_EmptyError_list(self):
        lst = SinglyList()
        lst.insert_last(10)
        assert len(lst) == 1
        assert lst.get_first() == 10
        assert lst.get_last() == 10

    def test_insert_multiple(self):
        lst = SinglyList()
        lst.insert_last(10)
        lst.insert_last(20)
        lst.insert_last(30)
        assert len(lst) == 3
        assert lst.get_first() == 10
        assert lst.get_last() == 30

    def test_mixed_with_insert_first(self):
        lst = SinglyList()
        lst.insert_first(20)
        lst.insert_first(10)
        lst.insert_last(30)
        assert list(lst) == [10, 20, 30]


class TestSinglyListInsertAt:
    """insert_at"""

    def test_insert_at_head(self):
        lst = SinglyList()
        lst.insert_last(20)
        lst.insert_at(0, 10)
        assert list(lst) == [10, 20]

    def test_insert_at_tail(self):
        lst = SinglyList()
        lst.insert_last(10)
        lst.insert_at(1, 20)
        assert list(lst) == [10, 20]

    def test_insert_at_length_appends(self):
        lst = SinglyList()
        lst.insert_last(10)
        lst.insert_at(1, 20)
        assert lst.get_last() == 20

    def test_insert_in_middle(self):
        lst = SinglyList()
        for v in [10, 30]:
            lst.insert_last(v)
        lst.insert_at(1, 20)
        assert list(lst) == [10, 20, 30]

    def test_insert_into_EmptyError_list_at_zero(self):
        lst = SinglyList()
        lst.insert_at(0, 42)
        assert len(lst) == 1
        assert lst.get_first() == 42

    def test_insert_at_negative_index(self):
        lst = SinglyList()
        for v in [10, 20]:
            lst.insert_last(v)
        lst.insert_at(-1, 15)
        assert list(lst) == [10, 15, 20]

    def test_insert_at_negative_index_head(self):
        lst = SinglyList()
        lst.insert_last(10)
        lst.insert_at(-1, 5)
        assert list(lst) == [5, 10]

    def test_insert_at_invalid_index_raises(self):
        lst = SinglyList()
        with pytest.raises(IndexError):
            lst.insert_at(1, 99)

    def test_insert_at_negative_out_of_bounds_raises(self):
        lst = SinglyList()
        lst.insert_last(10)
        with pytest.raises(IndexError):
            lst.insert_at(-3, 99)


class TestSinglyListGetFirst:
    """get_first"""

    def test_returns_first(self):
        lst = SinglyList()
        lst.insert_first(10)
        assert lst.get_first() == 10

    def test_raises_on_EmptyError(self):
        lst = SinglyList()
        with pytest.raises(EmptyError):
            lst.get_first()


class TestSinglyListGetLast:
    """get_last"""

    def test_returns_last(self):
        lst = SinglyList()
        lst.insert_last(10)
        lst.insert_last(20)
        assert lst.get_last() == 20

    def test_single_element_returns_same(self):
        lst = SinglyList()
        lst.insert_first(5)
        assert lst.get_last() == 5

    def test_raises_on_EmptyError(self):
        lst = SinglyList()
        with pytest.raises(EmptyError):
            lst.get_last()


class TestSinglyListGetAt:
    """get_at"""

    def test_returns_correct(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert lst.get_at(1) == 20

    def test_negative_index(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert lst.get_at(-1) == 30

    def test_raises_on_invalid_index(self):
        lst = SinglyList()
        lst.insert_last(10)
        with pytest.raises(IndexError):
            lst.get_at(5)

    def test_raises_on_EmptyError_list(self):
        lst = SinglyList()
        with pytest.raises(IndexError):
            lst.get_at(0)


class TestSinglyListRemoveFirst:
    """remove_first"""

    def test_removes_and_returns(self):
        lst = SinglyList()
        lst.insert_last(10)
        val = lst.remove_first()
        assert val == 10
        assert lst.is_empty()

    def test_updates_head_and_tail(self):
        lst = SinglyList()
        lst.insert_last(10)
        lst.insert_last(20)
        lst.remove_first()
        assert lst.get_first() == 20
        assert lst.get_last() == 20
        assert len(lst) == 1

    def test_raises_on_EmptyError(self):
        lst = SinglyList()
        with pytest.raises(EmptyError):
            lst.remove_first()


class TestSinglyListRemoveLast:
    """remove_last"""

    def test_removes_and_returns(self):
        lst = SinglyList()
        lst.insert_last(10)
        val = lst.remove_last()
        assert val == 10
        assert lst.is_empty()

    def test_updates_tail(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        val = lst.remove_last()
        assert val == 30
        assert lst.get_last() == 20
        assert len(lst) == 2

    def test_single_element_clears_list(self):
        lst = SinglyList()
        lst.insert_first(1)
        lst.remove_last()
        assert lst.is_empty()

    def test_raises_on_EmptyError(self):
        lst = SinglyList()
        with pytest.raises(EmptyError):
            lst.remove_last()


class TestSinglyListRemoveAt:
    """remove_at"""

    def test_remove_head(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        val = lst.remove_at(0)
        assert val == 10
        assert lst.get_first() == 20

    def test_remove_tail(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        val = lst.remove_at(2)
        assert val == 30
        assert lst.get_last() == 20

    def test_remove_middle(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        val = lst.remove_at(1)
        assert val == 20
        assert list(lst) == [10, 30]

    def test_negative_index(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert lst.remove_at(-1) == 30

    def test_remove_single_element(self):
        lst = SinglyList()
        lst.insert_last(42)
        val = lst.remove_at(0)
        assert val == 42
        assert lst.is_empty()

    def test_raises_on_invalid_index_EmptyError(self):
        lst = SinglyList()
        with pytest.raises(IndexError):
            lst.remove_at(0)

    def test_raises_on_invalid_index_nonEmptyError(self):
        lst = SinglyList()
        lst.insert_last(10)
        with pytest.raises(IndexError):
            lst.remove_at(5)


class TestSinglyListRemove:
    """remove"""

    def test_removes_head(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert lst.remove(10) is True
        assert list(lst) == [20, 30]

    def test_removes_tail(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert lst.remove(30) is True
        assert list(lst) == [10, 20]

    def test_removes_middle(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert lst.remove(20) is True
        assert list(lst) == [10, 30]

    def test_removes_only_first_occurrence(self):
        lst = SinglyList()
        for v in [10, 20, 10, 30]:
            lst.insert_last(v)
        assert lst.remove(10) is True
        assert list(lst) == [20, 10, 30]

    def test_returns_false_if_not_found(self):
        lst = SinglyList()
        lst.insert_last(10)
        assert lst.remove(99) is False

    def test_single_element_becomes_EmptyError(self):
        lst = SinglyList()
        lst.insert_first(1)
        lst.remove(1)
        assert lst.is_empty()

    def test_raises_on_EmptyError(self):
        lst = SinglyList()
        with pytest.raises(EmptyError):
            lst.remove(10)


class TestSinglyListIndex:
    """index_of"""

    def test_returns_index(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert lst.index_of(20) == 1

    def test_returns_first_occurrence(self):
        lst = SinglyList()
        for v in [10, 20, 10]:
            lst.insert_last(v)
        assert lst.index_of(10) == 0

    def test_returns_negative_one_if_not_found(self):
        lst = SinglyList()
        lst.insert_last(10)
        assert lst.index_of(99) == -1

    def test_EmptyError_list_returns_negative_one(self):
        lst = SinglyList()
        assert lst.index_of(10) == -1


class TestSinglyListCount:
    """count"""

    def test_counts_occurrences(self):
        lst = SinglyList()
        for v in [10, 20, 10, 10, 30]:
            lst.insert_last(v)
        assert lst.count(10) == 3

    def test_returns_zero_if_not_found(self):
        lst = SinglyList()
        lst.insert_last(10)
        assert lst.count(99) == 0

    def test_EmptyError_list_returns_zero(self):
        lst = SinglyList()
        assert lst.count(10) == 0


class TestSinglyListContains:
    """__contains__"""

    def test_contains_returns_true(self):
        lst = SinglyList()
        lst.insert_last(10)
        assert 10 in lst

    def test_contains_returns_false(self):
        lst = SinglyList()
        lst.insert_last(10)
        assert 20 not in lst

    def test_EmptyError_list_returns_false(self):
        lst = SinglyList()
        assert 10 not in lst


class TestSinglyListGetItem:
    """__getitem__"""

    def test_positive_index(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert lst[1] == 20

    def test_negative_index(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert lst[-1] == 30

    def test_raises_on_invalid_index(self):
        lst = SinglyList()
        with pytest.raises(IndexError):
            _ = lst[0]

    def test_raises_on_negative_out_of_bounds(self):
        lst = SinglyList()
        lst.insert_last(10)
        with pytest.raises(IndexError):
            _ = lst[-2]


class TestSinglyListIter:
    """__iter__"""

    def test_iterates_in_order(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert list(lst) == [10, 20, 30]

    def test_EmptyError_list_yields_nothing(self):
        lst = SinglyList()
        assert list(lst) == []


class TestSinglyListReverse:
    """reverse"""

    def test_reverses_multiple_elements(self):
        lst = SinglyList()
        for v in [1, 2, 3, 4, 5]:
            lst.insert_last(v)
        lst.reverse()
        assert list(lst) == [5, 4, 3, 2, 1]

    def test_reverses_two_elements(self):
        lst = SinglyList()
        lst.insert_last(10)
        lst.insert_last(20)
        lst.reverse()
        assert list(lst) == [20, 10]

    def test_reverses_single_element(self):
        lst = SinglyList()
        lst.insert_last(42)
        lst.reverse()
        assert list(lst) == [42]

    def test_head_and_tail_swapped_after_reverse(self):
        lst = SinglyList()
        for v in [1, 2, 3]:
            lst.insert_last(v)
        lst.reverse()
        assert lst.get_first() == 3
        assert lst.get_last() == 1

    def test_reverse_twice_restores_original(self):
        lst = SinglyList()
        for v in [1, 2, 3]:
            lst.insert_last(v)
        lst.reverse()
        lst.reverse()
        assert list(lst) == [1, 2, 3]

    def test_EmptyError_list_no_error(self):
        lst = SinglyList()
        lst.reverse()
        assert lst.is_empty()


class TestSinglyListCopy:
    """copy"""

    def test_copy_has_same_elements(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        cpy = lst.copy()
        assert list(cpy) == [10, 20, 30]

    def test_copy_is_independent(self):
        lst = SinglyList()
        lst.insert_last(10)
        cpy = lst.copy()
        lst.insert_last(20)
        assert len(cpy) == 1
        assert cpy.get_last() == 10

    def test_copy_EmptyError_list(self):
        lst = SinglyList()
        cpy = lst.copy()
        assert cpy.is_empty()
        assert isinstance(cpy, SinglyList)


class TestSinglyListClear:
    """clear"""

    def test_clears_all_elements(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        lst.clear()
        assert lst.is_empty()
        assert len(lst) == 0

    def test_clear_EmptyError_list_no_error(self):
        lst = SinglyList()
        lst.clear()
        assert lst.is_empty()
        assert not lst


class TestSinglyListHasCycle:
    """has_cycle"""

    def test_no_cycle_in_normal_list(self):
        lst = SinglyList()
        for v in [10, 20, 30]:
            lst.insert_last(v)
        assert lst.has_cycle() is False

    def test_no_cycle_in_EmptyError_list(self):
        lst = SinglyList()
        assert lst.has_cycle() is False

    def test_no_cycle_single_element(self):
        lst = SinglyList()
        lst.insert_first(1)
        assert lst.has_cycle() is False


class TestSinglyListMiddle:
    """middle"""

    def test_middle_odd_length(self):
        lst = SinglyList()
        for v in [1, 2, 3, 4, 5]:
            lst.insert_last(v)
        assert lst.middle() == 3

    def test_middle_even_length_returns_tuple(self):
        lst = SinglyList()
        for v in [1, 2, 3, 4]:
            lst.insert_last(v)
        assert lst.middle() == (2, 3)

    def test_middle_single_element(self):
        lst = SinglyList()
        lst.insert_last(42)
        assert lst.middle() == 42

    def test_middle_two_elements(self):
        lst = SinglyList()
        lst.insert_last(10)
        lst.insert_last(20)
        assert lst.middle() == (10, 20)

    def test_raises_on_EmptyError(self):
        lst = SinglyList()
        with pytest.raises(EmptyError):
            lst.middle()


class TestSinglyListBool:
    """__bool__"""

    def test_non_EmptyError_is_truthy(self):
        lst = SinglyList()
        lst.insert_first(1)
        assert bool(lst)

    def test_EmptyError_is_falsy(self):
        lst = SinglyList()
        assert not lst


class TestSinglyListLen:
    """__len__"""

    def test_length_updates_after_insert(self):
        lst = SinglyList()
        lst.insert_first(1)
        assert len(lst) == 1
        lst.insert_last(2)
        assert len(lst) == 2

    def test_length_updates_after_remove(self):
        lst = SinglyList()
        lst.insert_last(10)
        lst.insert_last(20)
        lst.remove_first()
        assert len(lst) == 1


class TestSinglyListWithCustomObjects:
    """Custom object types"""

    def test_works_with_strings(self):
        lst = SinglyList()
        lst.insert_last("hello")
        assert lst.get_first() == "hello"

    def test_works_with_none(self):
        lst = SinglyList()
        lst.insert_last(None)
        assert lst.get_first() is None

    def test_works_with_nested_lists(self):
        lst = SinglyList()
        inner = [1, 2, 3]
        lst.insert_last(inner)
        assert lst.get_first() is inner


class TestSinglyListLargeData:
    """Large data"""

    def test_many_elements(self):
        lst = SinglyList()
        n = 1000
        for i in range(n):
            lst.insert_last(i)
        assert len(lst) == n
        assert lst.get_first() == 0
        assert lst.get_last() == n - 1

    def test_many_removals(self):
        lst = SinglyList()
        n = 500
        for i in range(n):
            lst.insert_last(i)
        for _ in range(n):
            lst.remove_first()
        assert lst.is_empty()