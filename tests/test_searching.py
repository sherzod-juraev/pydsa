import math
import random

import pytest

from pydsa.searching import binary_search, exponential_search, jump_search, linear_search

SORTED_ONLY = [binary_search, jump_search, exponential_search]
ALL_SEARCHES = [linear_search, *SORTED_ONLY]


class Counted:
    """Comparable wrapper that counts every comparison in a shared counter."""

    def __init__(self, value: int, calls: list[int]) -> None:
        self.value = value
        self.calls = calls

    def __lt__(self, other: "Counted") -> bool:
        self.calls[0] += 1
        return self.value < other.value

    def __le__(self, other: "Counted") -> bool:
        self.calls[0] += 1
        return self.value <= other.value

    def __gt__(self, other: "Counted") -> bool:
        self.calls[0] += 1
        return self.value > other.value

    def __ge__(self, other: "Counted") -> bool:
        self.calls[0] += 1
        return self.value >= other.value

    def __eq__(self, other: object) -> bool:
        self.calls[0] += 1
        return isinstance(other, Counted) and self.value == other.value

    __hash__ = None  # type: ignore[assignment]


def count_comparisons(search_fn, values: list[int], target: int) -> tuple[int, int]:
    shared = [0]
    items = [Counted(v, shared) for v in values]
    result = search_fn(items, Counted(target, shared))
    return result, shared[0]


@pytest.mark.parametrize("search_fn", ALL_SEARCHES)
class TestEveryAlgorithm:
    def test_empty_sequence(self, search_fn) -> None:
        assert search_fn([], 5) == -1

    def test_single_element_found(self, search_fn) -> None:
        assert search_fn([42], 42) == 0

    def test_single_element_not_found(self, search_fn) -> None:
        assert search_fn([42], 1) == -1
        assert search_fn([42], 99) == -1

    def test_first_and_last_element(self, search_fn) -> None:
        arr = [1, 3, 5, 7, 9, 15]
        assert search_fn(arr, 1) == 0
        assert search_fn(arr, 15) == 5

    @pytest.mark.parametrize("target", [-5, 0, 2, 4, 8, 100])
    def test_absent_values_below_between_and_above(self, search_fn, target: int) -> None:
        assert search_fn([1, 3, 5, 7, 9, 15], target) == -1

    def test_two_elements(self, search_fn) -> None:
        arr = [1, 2]
        assert (search_fn(arr, 1), search_fn(arr, 2), search_fn(arr, 3), search_fn(arr, 0)) == (
            0,
            1,
            -1,
            -1,
        )

    @pytest.mark.parametrize("size", range(0, 70))
    def test_every_present_and_absent_value_for_every_small_size(
        self, search_fn, size: int
    ) -> None:
        arr = [2 * i for i in range(size)]  # evens, so odd targets are always absent
        for index, value in enumerate(arr):
            assert search_fn(arr, value) == index
        for target in range(-1, 2 * size + 2, 2):
            assert search_fn(arr, target) == -1

    def test_all_equal_elements(self, search_fn) -> None:
        arr = [7] * 9
        index = search_fn(arr, 7)
        assert 0 <= index < len(arr)
        assert search_fn(arr, 6) == -1
        assert search_fn(arr, 8) == -1

    def test_duplicates_return_an_index_holding_the_target(self, search_fn) -> None:
        arr = [1, 2, 2, 2, 3, 3, 5, 5, 5, 5]
        for target in (1, 2, 3, 5):
            assert arr[search_fn(arr, target)] == target
        assert search_fn(arr, 4) == -1

    def test_negative_numbers_and_floats(self, search_fn) -> None:
        arr = [-7.5, -2, -0.5, 0, 1.25, 3]
        assert [search_fn(arr, v) for v in arr] == list(range(len(arr)))
        assert search_fn(arr, -1) == -1

    def test_strings(self, search_fn) -> None:
        arr = ["apple", "banana", "cherry", "mango"]
        assert search_fn(arr, "cherry") == 2
        assert search_fn(arr, "zebra") == -1

    def test_tuples_as_elements(self, search_fn) -> None:
        arr = [(1, "a"), (1, "b"), (2, "a"), (3, "z")]
        assert search_fn(arr, (2, "a")) == 2
        assert search_fn(arr, (2, "b")) == -1

    def test_accepts_any_sequence(self, search_fn) -> None:
        assert search_fn((1, 3, 5, 7), 5) == 2
        assert search_fn(range(0, 100, 2), 40) == 20
        assert search_fn(range(0, 100, 2), 41) == -1

    def test_does_not_modify_the_input(self, search_fn) -> None:
        arr = [1, 3, 5, 7, 9]
        search_fn(arr, 5)
        assert arr == [1, 3, 5, 7, 9]

    def test_large_sequence(self, search_fn) -> None:
        arr = list(range(0, 200_000, 2))
        assert search_fn(arr, 199_998) == 99_999
        assert search_fn(arr, 100_001) == -1

    @pytest.mark.parametrize("seed", range(10))
    def test_random_sorted_arrays_with_duplicates(self, search_fn, seed: int) -> None:
        rng = random.Random(seed)
        arr = sorted(rng.randrange(0, 60) for _ in range(rng.randrange(0, 80)))
        for target in range(-2, 62):
            index = search_fn(arr, target)
            if target in arr:
                assert arr[index] == target
            else:
                assert index == -1


class TestLinearSearch:
    def test_works_on_unsorted_input(self) -> None:
        assert linear_search([15, 3, 9, 1, 7], 9) == 2
        assert linear_search([15, 3, 9, 1, 7], 100) == -1

    def test_returns_the_first_occurrence(self) -> None:
        assert linear_search([5, 3, 5, 5], 5) == 0
        assert linear_search([1, 2, 1, 2], 2) == 1

    def test_none_is_an_ordinary_target(self) -> None:
        assert linear_search([1, None, 3], None) == 1  # type: ignore[type-var]

    def test_stops_at_the_first_match(self) -> None:
        index, comparisons = count_comparisons(linear_search, [4, 4, 4, 4, 4], 4)
        assert (index, comparisons) == (0, 1)


class TestJumpSearch:
    @pytest.mark.parametrize("size", [1, 2, 3, 4, 5, 9, 10, 15, 16, 17, 24, 25, 26, 99, 100, 101])
    def test_lengths_around_perfect_squares(self, size: int) -> None:
        arr = list(range(size))
        assert [jump_search(arr, v) for v in arr] == arr
        assert jump_search(arr, size) == -1
        assert jump_search(arr, -1) == -1

    def test_target_exactly_at_a_jump_boundary(self) -> None:
        arr = list(range(0, 100))  # step = 10, boundaries at 10, 20, ...
        for boundary in range(10, 100, 10):
            assert jump_search(arr, boundary) == boundary
            assert jump_search(arr, boundary - 1) == boundary - 1
            assert jump_search(arr, boundary + 1) == boundary + 1

    def test_target_between_the_last_jump_and_the_end(self) -> None:
        arr = list(range(0, 50))
        assert jump_search(arr, 49) == 49
        assert jump_search(arr, 48) == 48

    def test_makes_about_square_root_comparisons(self) -> None:
        n = 10_000
        _, comparisons = count_comparisons(jump_search, list(range(n)), n - 1)
        assert comparisons <= 3 * math.isqrt(n)


class TestBinarySearch:
    def test_makes_logarithmic_comparisons(self) -> None:
        n = 100_000
        for target in (0, n // 3, n - 1, n + 5):
            _, comparisons = count_comparisons(binary_search, list(range(n)), target)
            assert comparisons <= 2 * (math.ceil(math.log2(n)) + 1)

    def test_finds_every_position_in_an_odd_length_array(self) -> None:
        arr = [1, 4, 9, 16, 25, 36, 49]
        assert [binary_search(arr, v) for v in arr] == list(range(7))


class TestExponentialSearch:
    @pytest.mark.parametrize("size", [1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33, 64, 65])
    def test_lengths_around_powers_of_two(self, size: int) -> None:
        arr = list(range(size))
        assert [exponential_search(arr, v) for v in arr] == arr
        assert exponential_search(arr, size) == -1

    def test_target_at_power_of_two_positions(self) -> None:
        arr = list(range(100))
        for position in (1, 2, 4, 8, 16, 32, 64):
            assert exponential_search(arr, position) == position

    def test_target_near_the_start_is_cheap(self) -> None:
        _, near = count_comparisons(exponential_search, list(range(100_000)), 3)
        _, far = count_comparisons(exponential_search, list(range(100_000)), 99_999)
        assert near < far
        assert near <= 12

    def test_makes_logarithmic_comparisons(self) -> None:
        n = 100_000
        _, comparisons = count_comparisons(exponential_search, list(range(n)), n - 1)
        assert comparisons <= 6 * math.ceil(math.log2(n)) + 10
