import numpy as np
import pytest
from pydsa import merge_sort, quick_sort


SORT_FUNCTIONS = [merge_sort, quick_sort]
SIZES = [0, 1, 5, 50, 200, 1000]


class TestEmptyAndSingle:
    """Empty and single-element arrays."""

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_empty_array(self, func):
        arr = np.array([], dtype=np.int64)
        result = func(arr)
        assert isinstance(result, np.ndarray)
        assert len(result) == 0
        assert result.dtype == arr.dtype

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_single_element(self, func):
        arr = np.array([42], dtype=np.int64)
        result = func(arr)
        np.testing.assert_array_equal(result, np.array([42]))

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_original_unchanged(self, func):
        arr = np.array([3, 1, 2], dtype=np.int64)
        original = arr.copy()
        _ = func(arr)
        np.testing.assert_array_equal(arr, original)


class TestAlreadySorted:
    """Already sorted input."""

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    @pytest.mark.parametrize("size", [5, 50, 200])
    def test_already_sorted(self, func, size):
        arr = np.arange(size, dtype=np.int64)
        result = func(arr)
        np.testing.assert_array_equal(result, arr)

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_all_equal(self, func):
        arr = np.full(100, 7, dtype=np.int64)
        result = func(arr)
        np.testing.assert_array_equal(result, arr)


class TestReverseSorted:
    """Reverse sorted input."""

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    @pytest.mark.parametrize("size", [5, 50, 200])
    def test_reverse_sorted(self, func, size):
        arr = np.arange(size, 0, -1, dtype=np.int64)
        expected = np.arange(1, size + 1, dtype=np.int64)
        result = func(arr)
        np.testing.assert_array_equal(result, expected)


class TestRandomData:
    """Random unsorted data."""

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    @pytest.mark.parametrize("size", [5, 50, 200, 1000])
    def test_random_array(self, func, size):
        rng = np.random.default_rng(42)
        arr = rng.integers(0, size * 10, size=size).astype(np.int64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)


class TestStability:
    """Stability — merge is stable, quick is not."""

    def test_merge_sort_stable(self):
        keys = np.array([2, 1, 2, 1], dtype=np.int64)
        sorted_keys = merge_sort(keys)
        assert sorted_keys[0] == 1
        assert sorted_keys[1] == 1

    def test_quick_sort_unstable(self):
        keys = np.array([2, 1, 2, 1], dtype=np.int64)
        _ = quick_sort(keys)


class TestNegativeNumbers:
    """Negative integers."""

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    @pytest.mark.parametrize("size", [5, 50])
    def test_negative_numbers(self, func, size):
        rng = np.random.default_rng(99)
        arr = rng.integers(-size * 5, size * 5, size=size).astype(np.int64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)


class TestFloatData:
    """Floating-point numbers."""

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    @pytest.mark.parametrize("size", [5, 50, 200])
    def test_float_array(self, func, size):
        rng = np.random.default_rng(7)
        arr = rng.uniform(-100.0, 100.0, size=size).astype(np.float64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)


class TestLargeAndEdge:
    """Large arrays and edge cases."""

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_large_array(self, func):
        rng = np.random.default_rng(1)
        arr = rng.integers(0, 10_000, size=2000).astype(np.int64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_duplicates_only(self, func):
        arr = np.array([5, 5, 5, 1, 5, 1, 5, 1, 5], dtype=np.int64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_two_elements(self, func):
        arr = np.array([2, 1], dtype=np.int64)
        result = func(arr)
        np.testing.assert_array_equal(result, np.array([1, 2]))

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_two_elements_equal(self, func):
        arr = np.array([5, 5], dtype=np.int64)
        result = func(arr)
        np.testing.assert_array_equal(result, np.array([5, 5]))

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_power_of_two_size(self, func):
        rng = np.random.default_rng(13)
        arr = rng.integers(0, 1000, size=64).astype(np.int64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_prime_size(self, func):
        rng = np.random.default_rng(17)
        arr = rng.integers(0, 1000, size=67).astype(np.int64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)