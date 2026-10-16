import math
import random

import pytest

from pydsa.sorting import merge_sort, quick_sort


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


class TestMergeSort:
    @pytest.mark.parametrize("size", [1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33, 100])
    def test_sizes_around_powers_of_two(self, size: int) -> None:
        data = list(range(size, 0, -1))
        assert merge_sort(data) == sorted(data)

    def test_comparisons_are_n_log_n(self) -> None:
        n = 4096
        shared = [0]
        data = [Counted(v, shared) for v in random.Random(1).sample(range(n), n)]
        merge_sort(data)
        assert shared[0] <= n * math.ceil(math.log2(n))

    def test_does_not_hit_the_recursion_limit(self) -> None:
        data = list(range(50_000, 0, -1))
        assert merge_sort(data) == sorted(data)


class TestQuickSort:
    def test_large_random_input(self) -> None:
        rng = random.Random(3)
        data = [rng.randrange(10_000) for _ in range(20_000)]
        assert quick_sort(data) == sorted(data)

    def test_sorted_input_does_not_overflow_the_stack(self) -> None:
        data = list(range(3_000))
        assert quick_sort(data) == data

    def test_reverse_sorted_input(self) -> None:
        data = list(range(3_000, 0, -1))
        assert quick_sort(data) == sorted(data)

    def test_all_equal_input(self) -> None:
        data = [4] * 2_000
        assert quick_sort(data) == data

    def test_few_distinct_values(self) -> None:
        rng = random.Random(5)
        data = [rng.randrange(3) for _ in range(3_000)]
        assert quick_sort(data) == sorted(data)

    @pytest.mark.parametrize("seed", range(20))
    def test_random_small_arrays_with_many_duplicates(self, seed: int) -> None:
        rng = random.Random(seed)
        data = [rng.randrange(6) for _ in range(rng.randrange(0, 40))]
        assert quick_sort(data) == sorted(data)
