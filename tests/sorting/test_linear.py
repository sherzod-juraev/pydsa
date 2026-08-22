import pytest

from pydsa import bucket_sort, counting_sort, radix_sort

NON_NEGATIVE_ONLY = [counting_sort, radix_sort]


@pytest.mark.parametrize("sort_fn", NON_NEGATIVE_ONLY)
class TestNonNegativeIntSorts:
    def test_empty_list(self, sort_fn) -> None:
        assert sort_fn([]) == []

    def test_single_element(self, sort_fn) -> None:
        assert sort_fn([42]) == [42]

    def test_already_sorted(self, sort_fn) -> None:
        assert sort_fn([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self, sort_fn) -> None:
        assert sort_fn([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_unsorted(self, sort_fn) -> None:
        assert sort_fn([4, 2, 2, 8, 3, 3, 1]) == [1, 2, 2, 3, 3, 4, 8]

    def test_all_equal_elements(self, sort_fn) -> None:
        assert sort_fn([7, 7, 7, 7]) == [7, 7, 7, 7]

    def test_zero_included(self, sort_fn) -> None:
        assert sort_fn([0, 3, 0, 1]) == [0, 0, 1, 3]

    def test_negative_raises(self, sort_fn) -> None:
        with pytest.raises(ValueError):
            sort_fn([1, -2, 3])

    def test_two_elements(self, sort_fn) -> None:
        assert sort_fn([2, 1]) == [1, 2]


class TestCountingSort:
    def test_stability(self) -> None:
        assert counting_sort([2, 1, 2, 1]) == [1, 1, 2, 2]

    def test_large_range_sparse_values(self) -> None:
        assert counting_sort([100, 50, 75, 25, 100]) == [25, 50, 75, 100, 100]


class TestRadixSort:
    def test_multi_digit_numbers(self) -> None:
        assert radix_sort([170, 45, 75, 90, 2, 802, 24, 2, 66]) == [2, 2, 24, 45, 66, 75, 90, 170, 802,]

    def test_varying_digit_counts(self) -> None:
        assert radix_sort([121, 432, 564, 23, 1]) == [1, 23, 121, 432, 564]

    def test_all_zero(self) -> None:
        assert radix_sort([0, 0, 0]) == [0, 0, 0]


class TestBucketSort:
    def test_empty_list(self) -> None:
        assert bucket_sort([]) == []

    def test_single_element(self) -> None:
        assert bucket_sort([42]) == [42]

    def test_floats_unit_range(self) -> None:
        assert bucket_sort([0.4, 0.1, 0.7, 0.3, 0.9]) == [0.1, 0.3, 0.4, 0.7, 0.9]

    def test_integers(self) -> None:
        assert bucket_sort([5, 2, 8, 1, 9, 3]) == [1, 2, 3, 5, 8, 9]

    def test_all_equal_elements_returns_input_unchanged(self) -> None:
        assert bucket_sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    def test_negative_and_positive_floats(self) -> None:
        assert bucket_sort([-2.5, 3.1, 0.0, -1.0, 2.2]) == [-2.5, -1.0, 0.0, 2.2, 3.1]

    def test_two_elements(self) -> None:
        assert bucket_sort([2.0, 1.0]) == [1.0, 2.0]

    def test_larger_distribution(self) -> None:
        arr = [float(i % 37) for i in range(150)]
        assert bucket_sort(arr) == sorted(arr)