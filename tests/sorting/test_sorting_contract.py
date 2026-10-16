import random
from dataclasses import dataclass

import pytest

from pydsa.sorting import (
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)

COMPARISON_SORTS = [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort]
STABLE_SORTS = [bubble_sort, insertion_sort, merge_sort]


@dataclass(frozen=True)
class Record:
    """Compared by key only, so equal keys are distinguishable by tag."""

    key: int
    tag: str

    def __lt__(self, other: "Record") -> bool:
        return self.key < other.key

    def __le__(self, other: "Record") -> bool:
        return self.key <= other.key

    def __gt__(self, other: "Record") -> bool:
        return self.key > other.key

    def __ge__(self, other: "Record") -> bool:
        return self.key >= other.key


@pytest.mark.parametrize("sort_fn", COMPARISON_SORTS)
class TestEveryComparisonSort:
    def test_empty(self, sort_fn) -> None:
        assert sort_fn([]) == []

    def test_single_element(self, sort_fn) -> None:
        assert sort_fn([5]) == [5]

    def test_two_elements_both_orders(self, sort_fn) -> None:
        assert sort_fn([1, 2]) == [1, 2]
        assert sort_fn([2, 1]) == [1, 2]

    def test_already_sorted(self, sort_fn) -> None:
        assert sort_fn([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self, sort_fn) -> None:
        assert sort_fn([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_all_equal(self, sort_fn) -> None:
        assert sort_fn([7] * 12) == [7] * 12

    def test_duplicates(self, sort_fn) -> None:
        assert sort_fn([3, 1, 3, 2, 1, 2, 3]) == [1, 1, 2, 2, 3, 3, 3]

    def test_negative_numbers_and_floats(self, sort_fn) -> None:
        assert sort_fn([3.5, -1, 0, -7.25, 2]) == [-7.25, -1, 0, 2, 3.5]

    def test_strings(self, sort_fn) -> None:
        assert sort_fn(["pear", "apple", "fig"]) == ["apple", "fig", "pear"]

    def test_tuples(self, sort_fn) -> None:
        assert sort_fn([(2, "b"), (1, "z"), (2, "a")]) == [(1, "z"), (2, "a"), (2, "b")]

    def test_accepts_any_sequence(self, sort_fn) -> None:
        assert sort_fn((3, 1, 2)) == [1, 2, 3]
        assert sort_fn(range(5, 0, -1)) == [1, 2, 3, 4, 5]

    def test_returns_a_new_list_and_keeps_the_input(self, sort_fn) -> None:
        original = [3, 1, 2]
        snapshot = list(original)
        result = sort_fn(original)
        assert original == snapshot
        assert result is not original

    def test_sorted_input_returns_a_copy(self, sort_fn) -> None:
        original = [1, 2, 3]
        assert sort_fn(original) is not original

    def test_tuple_input_gives_a_list(self, sort_fn) -> None:
        assert isinstance(sort_fn((2, 1)), list)

    @pytest.mark.parametrize("size", range(0, 40))
    def test_every_permutation_class_for_small_sizes(self, sort_fn, size: int) -> None:
        rng = random.Random(size)
        data = [rng.randrange(0, 10) for _ in range(size)]
        assert sort_fn(data) == sorted(data)

    @pytest.mark.parametrize("seed", range(15))
    def test_random_against_builtin_sorted(self, sort_fn, seed: int) -> None:
        rng = random.Random(seed)
        data = [rng.randrange(-100, 100) for _ in range(rng.randrange(0, 200))]
        assert sort_fn(data) == sorted(data)

    def test_all_permutations_of_five(self, sort_fn) -> None:
        from itertools import permutations

        for perm in permutations([3, 1, 2, 2, 0]):
            assert sort_fn(list(perm)) == [0, 1, 2, 2, 3]

    def test_output_is_a_permutation_of_input(self, sort_fn) -> None:
        data = [5, 3, 5, 1, 9, 1, 1]
        assert sorted(sort_fn(data)) == sorted(data)

    def test_organ_pipe_and_sawtooth_patterns(self, sort_fn) -> None:
        pipe = list(range(30)) + list(range(30, 0, -1))
        saw = [i % 7 for i in range(60)]
        assert sort_fn(pipe) == sorted(pipe)
        assert sort_fn(saw) == sorted(saw)


@pytest.mark.parametrize("sort_fn", STABLE_SORTS)
class TestStability:
    def test_equal_keys_keep_their_original_order(self, sort_fn) -> None:
        data = [Record(2, "a"), Record(1, "b"), Record(2, "c"), Record(1, "d"), Record(2, "e")]
        result = sort_fn(data)
        assert [(r.key, r.tag) for r in result] == [
            (1, "b"),
            (1, "d"),
            (2, "a"),
            (2, "c"),
            (2, "e"),
        ]

    @pytest.mark.parametrize("seed", range(10))
    def test_random_records_match_python_stable_sort(self, sort_fn, seed: int) -> None:
        rng = random.Random(seed)
        data = [Record(rng.randrange(0, 5), str(i)) for i in range(rng.randrange(0, 60))]
        assert sort_fn(data) == sorted(data, key=lambda r: r.key)

    def test_all_equal_keys_are_untouched(self, sort_fn) -> None:
        data = [Record(1, str(i)) for i in range(10)]
        assert sort_fn(data) == data


class TestHeapAndQuickSortAreAllowedToBeUnstable:
    """Documented as unstable: only the keys are guaranteed, not the tag order."""

    @pytest.mark.parametrize("sort_fn", [selection_sort, quick_sort, heap_sort])
    def test_keys_are_sorted_even_when_tags_are_reordered(self, sort_fn) -> None:
        data = [Record(2, "a"), Record(1, "b"), Record(2, "c"), Record(1, "d")]
        assert [r.key for r in sort_fn(data)] == [1, 1, 2, 2]
