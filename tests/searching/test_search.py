import pytest

from pydsa import binary_search, exponential_search, jump_search, linear_search

ALGORITHMS_UNSORTED_OK = [linear_search]
ALGORITHMS_SORTED_ONLY = [binary_search, jump_search, exponential_search]
ALL_ALGORITHMS = ALGORITHMS_UNSORTED_OK + ALGORITHMS_SORTED_ONLY


class TestLinearSearchUnsorted:
    def test_finds_in_unsorted(self) -> None:
        assert linear_search([15, 3, 9, 1, 7], 9) == 2

    def test_not_found_returns_minus_one(self) -> None:
        assert linear_search([15, 3, 9, 1, 7], 100) == -1

    def test_returns_first_occurrence(self) -> None:
        assert linear_search([5, 3, 5, 5], 5) == 0


@pytest.mark.parametrize("search_fn", ALL_ALGORITHMS)
class TestCommonBehavior:
    def test_empty_array_returns_minus_one(self, search_fn) -> None:
        assert search_fn([], 5) == -1

    def test_single_element_found(self, search_fn) -> None:
        assert search_fn([42], 42) == 0

    def test_single_element_not_found(self, search_fn) -> None:
        assert search_fn([42], 1) == -1

    def test_target_is_first_element(self, search_fn) -> None:
        arr = [1, 3, 5, 7, 9, 15]
        assert search_fn(arr, 1) == 0

    def test_target_is_last_element(self, search_fn) -> None:
        arr = [1, 3, 5, 7, 9, 15]
        assert search_fn(arr, 15) == 5


@pytest.mark.parametrize("search_fn", ALGORITHMS_SORTED_ONLY)
class TestSortedOnlyAlgorithms:
    def test_finds_middle_element(self, search_fn) -> None:
        arr = [1, 3, 7, 9, 15]
        assert search_fn(arr, 7) == 2

    def test_not_found_below_range(self, search_fn) -> None:
        arr = [1, 3, 7, 9, 15]
        assert search_fn(arr, -5) == -1

    def test_not_found_above_range(self, search_fn) -> None:
        arr = [1, 3, 7, 9, 15]
        assert search_fn(arr, 999) == -1

    def test_not_found_between_elements(self, search_fn) -> None:
        arr = [1, 3, 7, 9, 15]
        assert search_fn(arr, 5) == -1

    def test_large_sorted_array(self, search_fn) -> None:
        arr = list(range(0, 10_000, 2))
        assert search_fn(arr, 4998) == 2499

    def test_all_equal_elements_found(self, search_fn) -> None:
        arr = [7, 7, 7, 7, 7]
        assert search_fn(arr, 7) != -1
        assert arr[search_fn(arr, 7)] == 7

    def test_two_elements(self, search_fn) -> None:
        arr = [1, 2]
        assert search_fn(arr, 1) == 0
        assert search_fn(arr, 2) == 1
        assert search_fn(arr, 3) == -1


class TestJumpSearchBoundary:
    def test_target_at_step_boundary(self) -> None:
        arr = [1, 3, 7, 9, 15, 20, 25, 30]
        assert jump_search(arr, 20) == 5

    def test_odd_length_array(self) -> None:
        arr = [1, 4, 9, 16, 25, 36, 49]
        for i, v in enumerate(arr):
            assert jump_search(arr, v) == i


class TestExponentialSearchBoundary:
    def test_target_near_start(self) -> None:
        arr = list(range(1, 1000))
        assert exponential_search(arr, 2) == 1

    def test_target_at_power_of_two_boundary(self) -> None:
        arr = list(range(20))
        assert exponential_search(arr, 8) == 8

    def test_target_beyond_first_double(self) -> None:
        arr = [1, 3, 5, 7, 9, 15, 20, 30, 50]
        assert exponential_search(arr, 50) == 8