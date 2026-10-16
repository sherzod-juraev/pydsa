import pytest

from pydsa.sorting import bubble_sort, insertion_sort, selection_sort


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


def comparisons(sort_fn, values: list[int]) -> int:
    shared = [0]
    sort_fn([Counted(v, shared) for v in values])
    return shared[0]


class TestBubbleSort:
    def test_sorted_input_takes_a_single_pass(self) -> None:
        n = 200
        assert comparisons(bubble_sort, list(range(n))) <= n

    def test_reverse_input_is_quadratic(self) -> None:
        n = 60
        assert comparisons(bubble_sort, list(range(n, 0, -1))) >= n * (n - 1) // 4

    def test_largest_element_moves_to_the_end_first(self) -> None:
        assert bubble_sort([9, 1, 2, 3]) == [1, 2, 3, 9]


class TestSelectionSort:
    def test_comparisons_do_not_depend_on_input_order(self) -> None:
        n = 40
        expected = n * (n - 1) // 2
        assert comparisons(selection_sort, list(range(n))) == expected
        assert comparisons(selection_sort, list(range(n, 0, -1))) == expected

    def test_minimum_at_the_end(self) -> None:
        assert selection_sort([5, 4, 3, 0]) == [0, 3, 4, 5]


class TestInsertionSort:
    def test_sorted_input_is_linear(self) -> None:
        n = 300
        assert comparisons(insertion_sort, list(range(n))) <= 2 * n

    def test_nearly_sorted_input_is_cheaper_than_reversed(self) -> None:
        n = 100
        nearly = list(range(n))
        nearly[10], nearly[11] = nearly[11], nearly[10]
        assert (
            comparisons(insertion_sort, nearly)
            < comparisons(insertion_sort, list(range(n, 0, -1))) // 10
        )

    @pytest.mark.parametrize("data", [[2, 1], [1, 3, 2], [3, 2, 1], [2, 3, 1]])
    def test_small_cases(self, data: list[int]) -> None:
        assert insertion_sort(data) == sorted(data)
