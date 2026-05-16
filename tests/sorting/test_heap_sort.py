import numpy as np
import pytest
from pydsa import heap_sort


class TestHeapSort:
    """heap_sort"""

    def test_empty_array(self):
        arr = []
        result = heap_sort(arr)
        assert result == []
        assert arr == []  # original unchanged

    def test_single_element(self):
        arr = [42]
        result = heap_sort(arr)
        assert result == [42]

    def test_original_unchanged(self):
        arr = [3, 1, 2]
        original = arr.copy()
        _ = heap_sort(arr)
        assert arr == original

    def test_already_sorted(self):
        arr = [1, 2, 3, 4, 5]
        result = heap_sort(arr)
        assert result == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        arr = [5, 4, 3, 2, 1]
        result = heap_sort(arr)
        assert result == [1, 2, 3, 4, 5]

    def test_random_list(self):
        rng = np.random.default_rng(42)
        arr = rng.integers(0, 1000, size=200).tolist()
        result = heap_sort(arr)
        assert result == sorted(arr)

    def test_all_equal(self):
        arr = [7, 7, 7, 7, 7]
        result = heap_sort(arr)
        assert result == [7, 7, 7, 7, 7]

    def test_duplicates(self):
        arr = [5, 3, 5, 1, 3, 5]
        result = heap_sort(arr)
        assert result == [1, 3, 3, 5, 5, 5]

    def test_negative_numbers(self):
        arr = [-5, -10, 0, 15, -3]
        result = heap_sort(arr)
        assert result == [-10, -5, -3, 0, 15]

    def test_floats(self):
        arr = [3.14, 1.41, 2.71, 0.0, -1.5]
        result = heap_sort(arr)
        assert result == [-1.5, 0.0, 1.41, 2.71, 3.14]

    def test_large_array(self):
        rng = np.random.default_rng(1)
        arr = rng.integers(0, 10000, size=2000).tolist()
        result = heap_sort(arr)
        assert result == sorted(arr)

    def test_two_elements(self):
        arr = [2, 1]
        result = heap_sort(arr)
        assert result == [1, 2]

    def test_two_elements_equal(self):
        arr = [5, 5]
        result = heap_sort(arr)
        assert result == [5, 5]