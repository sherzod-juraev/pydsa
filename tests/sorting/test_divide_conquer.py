import pytest

from pydsa import merge_sort, quick_sort

ALL_SORTS = [merge_sort, quick_sort]


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
        assert sort_fn([38, 27, 43, 3, 9, 82, 10]) == [3, 9, 10, 27, 38, 43, 82]

    def test_all_equal_elements(self, sort_fn) -> None:
        assert sort_fn([7, 7, 7, 7]) == [7, 7, 7, 7]

    def test_with_duplicates(self, sort_fn) -> None:
        assert sort_fn([3, 1, 3, 2, 1]) == [1, 1, 2, 3, 3]

    def test_strings(self, sort_fn) -> None:
        assert sort_fn(["dog", "cat", "elephant", "ant"]) == ["ant", "cat", "dog", "elephant"]

    def test_negative_numbers(self, sort_fn) -> None:
        assert sort_fn([-3, 5, -1, 0, 2]) == [-3, -1, 0, 2, 5]

    def test_two_elements_unordered(self, sort_fn) -> None:
        assert sort_fn([2, 1]) == [1, 2]

    def test_large_random_like_input(self, sort_fn) -> None:
        arr = [(i * 37) % 101 for i in range(200)]
        assert sort_fn(arr) == sorted(arr)

    def test_odd_length_input(self, sort_fn) -> None:
        assert sort_fn([9, 1, 5, 3, 7]) == [1, 3, 5, 7, 9]


class TestMergeSortStability:
    def test_preserves_relative_order_of_equal_keys(self) -> None:
        data = [(2, "a"), (1, "b"), (2, "c"), (1, "d"), (2, "e")]
        result = merge_sort(data)
        assert result == [(1, "b"), (1, "d"), (2, "a"), (2, "c"), (2, "e")]


class TestQuickSortEdgeCases:
    def test_worst_case_already_sorted_still_correct(self) -> None:
        assert quick_sort(list(range(100))) == list(range(100))

    def test_worst_case_reverse_sorted_still_correct(self) -> None:
        assert quick_sort(list(range(100, 0, -1))) == list(range(1, 101))

    def test_many_duplicate_pivots(self) -> None:
        arr = [5] * 50 + [1, 9, 3]
        assert quick_sort(arr) == sorted(arr)