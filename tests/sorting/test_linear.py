import numpy as np
import pytest
from pydsa import counting_sort, radix_sort, bucket_sort


SORT_FUNCTIONS = [counting_sort, radix_sort, bucket_sort]
INT_SIZES = [0, 1, 5, 50, 200, 1000]


class TestEmptyAndSingle:
    """Empty and single-element arrays."""

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_empty_array(self, func):
        arr = np.array([], dtype=np.int64)
        result = func(arr)
        assert isinstance(result, np.ndarray)
        assert len(result) == 0

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

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_all_zeros(self, func):
        arr = np.zeros(50, dtype=np.int64)
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
        arr = rng.integers(0, size * 5, size=size).astype(np.int64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)


class TestStability:
    """Stability — all linear sorts are stable."""

    def test_counting_sort_stable(self):
        keys = np.array([2, 1, 2, 1], dtype=np.int64)
        sorted_keys = counting_sort(keys)
        assert sorted_keys[0] == 1
        assert sorted_keys[1] == 1

    def test_radix_sort_stable(self):
        keys = np.array([2, 1, 2, 1], dtype=np.int64)
        sorted_keys = radix_sort(keys)
        assert sorted_keys[0] == 1
        assert sorted_keys[1] == 1

    def test_bucket_sort_stable(self):
        keys = np.array([2, 1, 2, 1], dtype=np.int64)
        sorted_keys = bucket_sort(keys)
        assert sorted_keys[0] == 1
        assert sorted_keys[1] == 1


class TestDuplicateValues:
    """Arrays with many duplicates."""

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_duplicates_only(self, func):
        arr = np.array([5, 5, 5, 1, 5, 1, 5, 1, 5], dtype=np.int64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)

    @pytest.mark.parametrize("func", SORT_FUNCTIONS)
    def test_two_values_repeated(self, func):
        arr = np.array([3, 7, 3, 7, 3, 7, 3, 7], dtype=np.int64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)


class TestLargeValues:
    """Large value ranges."""

    @pytest.mark.parametrize("func", [counting_sort, bucket_sort])
    def test_large_max_value_counting(self, func):
        rng = np.random.default_rng(5)
        arr = rng.integers(1000, 5000, size=100).astype(np.int64)
        result = func(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)

    def test_radix_sort_large_values(self):
        rng = np.random.default_rng(5)
        arr = rng.integers(1_000_000, 10_000_000, size=200).astype(np.int64)
        result = radix_sort(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)


class TestFloatData:
    """Floating-point numbers (bucket sort only)."""

    @pytest.mark.parametrize("size", [5, 50, 200])
    def test_bucket_sort_floats(self, size):
        rng = np.random.default_rng(7)
        arr = rng.uniform(-100.0, 100.0, size=size).astype(np.float64)
        result = bucket_sort(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)

    def test_bucket_sort_uniform_floats(self):
        rng = np.random.default_rng(3)
        arr = rng.uniform(0.0, 1.0, size=200).astype(np.float64)
        result = bucket_sort(arr)
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

    def test_counting_sort_sparse(self):
        arr = np.array([100, 0, 50, 100, 0], dtype=np.int64)
        result = counting_sort(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)

    def test_radix_sort_many_digits(self):
        arr = np.array([99999, 1, 1000, 55555, 10], dtype=np.int64)
        result = radix_sort(arr)
        expected = np.sort(arr)
        np.testing.assert_array_equal(result, expected)