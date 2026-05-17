import numpy as np
import pytest
from pydsa import (
    linear_search,
    binary_search,
    jump_search,
    exponential_search,
)


SORTED_SEARCH_FUNCS = [binary_search, jump_search, exponential_search]
ALL_SEARCH_FUNCS = [linear_search] + SORTED_SEARCH_FUNCS


class TestEmptyArray:
    """Empty arrays."""

    @pytest.mark.parametrize("func", ALL_SEARCH_FUNCS)
    def test_empty_returns_minus_one(self, func):
        arr = np.array([], dtype=np.int64)
        assert func(arr, 5) == -1


class TestSingleElement:
    """Single element arrays."""

    @pytest.mark.parametrize("func", ALL_SEARCH_FUNCS)
    def test_found(self, func):
        arr = np.array([42], dtype=np.int64)
        assert func(arr, 42) == 0

    @pytest.mark.parametrize("func", ALL_SEARCH_FUNCS)
    def test_not_found_smaller(self, func):
        arr = np.array([42], dtype=np.int64)
        assert func(arr, 10) == -1

    @pytest.mark.parametrize("func", ALL_SEARCH_FUNCS)
    def test_not_found_larger(self, func):
        arr = np.array([42], dtype=np.int64)
        assert func(arr, 99) == -1


class TestSmallArray:
    """Small sorted arrays."""

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_first_element(self, func):
        arr = np.array([1, 2, 3, 4, 5], dtype=np.int64)
        assert func(arr, 1) == 0

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_last_element(self, func):
        arr = np.array([1, 2, 3, 4, 5], dtype=np.int64)
        assert func(arr, 5) == 4

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_middle_element(self, func):
        arr = np.array([1, 2, 3, 4, 5], dtype=np.int64)
        assert func(arr, 3) == 2

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_not_found(self, func):
        arr = np.array([1, 2, 3, 4, 5], dtype=np.int64)
        assert func(arr, 99) == -1

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_not_found_between(self, func):
        arr = np.array([1, 3, 5, 7], dtype=np.int64)
        assert func(arr, 4) == -1

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_less_than_min(self, func):
        arr = np.array([10, 20, 30], dtype=np.int64)
        assert func(arr, 5) == -1

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_greater_than_max(self, func):
        arr = np.array([10, 20, 30], dtype=np.int64)
        assert func(arr, 50) == -1


class TestLinearSearchUnsorted:
    """Linear search on unsorted data."""

    def test_found_first(self):
        arr = np.array([7, 2, 9, 1, 5], dtype=np.int64)
        assert linear_search(arr, 7) == 0

    def test_found_last(self):
        arr = np.array([7, 2, 9, 1, 5], dtype=np.int64)
        assert linear_search(arr, 5) == 4

    def test_not_found(self):
        arr = np.array([7, 2, 9, 1, 5], dtype=np.int64)
        assert linear_search(arr, 99) == -1


class TestDuplicates:
    """Arrays with duplicates."""

    @pytest.mark.parametrize("func", ALL_SEARCH_FUNCS)
    def test_first_occurrence_not_guaranteed(self, func):
        arr = np.array([1, 2, 2, 2, 3], dtype=np.int64)
        idx = func(arr, 2)
        assert idx in [1, 2, 3]  # any occurrence is valid


class TestLargeArray:
    """Large sorted arrays."""

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_found_random(self, func):
        rng = np.random.default_rng(42)
        arr = np.sort(rng.integers(0, 100_000, size=5000).astype(np.int64))
        target = arr[1234]
        assert func(arr, target) is not None
        assert arr[func(arr, target)] == target

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_not_found_large(self, func):
        rng = np.random.default_rng(42)
        arr = np.sort(rng.integers(0, 50_000, size=5000).astype(np.int64))
        # ensure value not in array
        target = np.max(arr) + 100
        assert func(arr, target) == -1


class TestEdgeCases:
    """Edge cases."""

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_two_elements(self, func):
        arr = np.array([10, 20], dtype=np.int64)
        assert func(arr, 10) == 0
        assert func(arr, 20) == 1

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_all_equal(self, func):
        arr = np.full(50, 7, dtype=np.int64)
        idx = func(arr, 7)
        assert arr[idx] == 7

    def test_exponential_search_boundary(self):
        arr = np.arange(1, 100, dtype=np.int64)
        assert exponential_search(arr, 1) == 0
        assert exponential_search(arr, 2) == 1
        assert exponential_search(arr, 3) == 2
        assert exponential_search(arr, 99) == 98


class TestNegativeNumbers:
    """Negative values."""

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_negative_target(self, func):
        arr = np.array([-10, -5, 0, 5, 10], dtype=np.int64)
        assert func(arr, -5) == 1

    @pytest.mark.parametrize("func", SORTED_SEARCH_FUNCS)
    def test_all_negative(self, func):
        arr = np.array([-50, -40, -30, -20, -10], dtype=np.int64)
        assert func(arr, -30) == 2