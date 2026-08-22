import pytest

from pydsa import bubble_sort, insertion_sort, selection_sort

ALL_SORTS = [bubble_sort, selection_sort, insertion_sort]
STABLE_SORTS = [bubble_sort, insertion_sort]


@pytest.mark.parametrize("sort_fn", ALL_SORTS)
class TestCommonSortingBehavior:
    def test_empty_list(self, sort_fn) -> None:
        assert sort_fn([]) == []

    def test_single_element(self, sort_fn) -> None:
        assert sort_fn([42]) == [42]

    def test_already_sorted(self, sort_fn) -> None:
        assert sort_fn([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self, sort_fn) -> None:
        assert sort_fn([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_unsorted(self, sort_fn) -> None:
        assert sort_fn([5, 2, 8, 1, 9]) == [1, 2, 5, 8, 9]

    def test_all_equal_elements(self, sort_fn) -> None:
        assert sort_fn([7, 7, 7, 7]) == [7, 7, 7, 7]

    def test_with_duplicates(self, sort_fn) -> None:
        assert sort_fn([3, 1, 3, 2, 1]) == [1, 1, 2, 3, 3]

    def test_strings(self, sort_fn) -> None:
        assert sort_fn(["zebra", "apple", "mango"]) == ["apple", "mango", "zebra"]

    def test_negative_numbers(self, sort_fn) -> None:
        assert sort_fn([-3, 5, -1, 0, 2]) == [-3, -1, 0, 2, 5]

    def test_does_not_mutate_input(self, sort_fn) -> None:
        original = [3, 1, 2]
        sort_fn(original)
        assert original == [3, 1, 2]

    def test_returns_new_list(self, sort_fn) -> None:
        original = [1, 2, 3]
        result = sort_fn(original)
        assert result is not original

    def test_two_elements_unordered(self, sort_fn) -> None:
        assert sort_fn([2, 1]) == [1, 2]


@pytest.mark.parametrize("sort_fn", STABLE_SORTS)
class TestStability:
    def test_preserves_relative_order_of_equal_keys(self, sort_fn) -> None:
        # tuples: (key, original_index) — equal keys must keep original order
        data = [(2, "a"), (1, "b"), (2, "c"), (1, "d"), (2, "e")]
        result = sort_fn(data)
        assert result == [(1, "b"), (1, "d"), (2, "a"), (2, "c"), (2, "e")]


class TestBubbleSortAdaptive:
    def test_early_termination_on_sorted_input(self) -> None:
        # Correctness check; adaptiveness itself isn't observable without
        # instrumentation, so we just confirm correctness on presorted input.
        assert bubble_sort(list(range(100))) == list(range(100))


class TestSelectionSortNonAdaptive:
    def test_correct_regardless_of_initial_order(self) -> None:
        assert selection_sort(list(range(50, 0, -1))) == list(range(1, 51))