import heapq
import random
from typing import Any

import pytest

from pydsa.core import BaseStructure
from pydsa.exc import EmptyError
from pydsa.trees import MaxHeap, MinHeap
from pydsa.trees.heap import HeapBase

# (class, public extract method, expected order of extract_all for a list)
HEAPS = [
    pytest.param(MinHeap, "extract_min", False, id="MinHeap"),
    pytest.param(MaxHeap, "extract_max", True, id="MaxHeap"),
]


def check_invariant(heap) -> None:
    """No element may precede its parent."""
    data = heap._data
    for child in range(1, len(data)):
        parent = (child - 1) // 2
        assert not heap._precedes(data[child], data[parent]), f"violated at index {child}"


def make(heap_cls, values):
    heap = heap_cls()
    for value in values:
        heap.insert(value)
    return heap


@pytest.mark.parametrize(("heap_cls", "extract", "descending"), HEAPS)
class TestEveryHeap:
    def test_empty_heap(self, heap_cls, extract, descending) -> None:
        heap = heap_cls()
        assert len(heap) == 0
        assert not heap
        assert 1 not in heap
        assert heap.extract_all() == []

    def test_peek_on_empty_raises(self, heap_cls, extract, descending) -> None:
        with pytest.raises(EmptyError, match=heap_cls.__name__):
            heap_cls().peek()

    def test_extract_on_empty_raises(self, heap_cls, extract, descending) -> None:
        with pytest.raises(EmptyError, match=heap_cls.__name__):
            getattr(heap_cls(), extract)()

    def test_single_element(self, heap_cls, extract, descending) -> None:
        heap = make(heap_cls, [7])
        assert (len(heap), bool(heap), heap.peek()) == (1, True, 7)
        assert getattr(heap, extract)() == 7
        assert len(heap) == 0
        assert not heap

    def test_peek_does_not_remove(self, heap_cls, extract, descending) -> None:
        heap = make(heap_cls, [4, 9, 1])
        first = heap.peek()
        assert heap.peek() == first
        assert len(heap) == 3

    def test_root_is_the_extreme_value(self, heap_cls, extract, descending) -> None:
        values = [5, 3, 9, 1, 7]
        heap = make(heap_cls, values)
        assert heap.peek() == (max(values) if descending else min(values))

    def test_extraction_order(self, heap_cls, extract, descending) -> None:
        values = [5, 3, 9, 1, 7, 3, 8, 2]
        heap = make(heap_cls, values)
        out = [getattr(heap, extract)() for _ in values]
        assert out == sorted(values, reverse=descending)
        assert len(heap) == 0

    def test_extract_all_returns_priority_order_and_empties_the_heap(
        self, heap_cls, extract, descending
    ) -> None:
        values = [5, 3, 9, 1, 7, 3]
        heap = make(heap_cls, values)
        assert heap.extract_all() == sorted(values, reverse=descending)
        assert len(heap) == 0
        assert not heap
        assert heap.extract_all() == []

    def test_insert_after_extract_all(self, heap_cls, extract, descending) -> None:
        heap = make(heap_cls, [3, 1, 2])
        heap.extract_all()
        heap.insert(5)
        assert heap.peek() == 5
        assert len(heap) == 1

    def test_duplicates(self, heap_cls, extract, descending) -> None:
        heap = make(heap_cls, [2, 2, 2, 1, 1, 3, 3])
        assert heap.extract_all() == sorted([2, 2, 2, 1, 1, 3, 3], reverse=descending)

    def test_all_equal(self, heap_cls, extract, descending) -> None:
        heap = make(heap_cls, [4] * 10)
        assert heap.extract_all() == [4] * 10

    def test_negative_numbers_and_floats(self, heap_cls, extract, descending) -> None:
        values = [3.5, -1, 0, -7.25, 2]
        assert make(heap_cls, values).extract_all() == sorted(values, reverse=descending)

    def test_strings(self, heap_cls, extract, descending) -> None:
        values = ["pear", "apple", "fig"]
        assert make(heap_cls, values).extract_all() == sorted(values, reverse=descending)

    def test_tuples(self, heap_cls, extract, descending) -> None:
        values = [(2, "b"), (1, "z"), (2, "a")]
        assert make(heap_cls, values).extract_all() == sorted(values, reverse=descending)

    def test_contains(self, heap_cls, extract, descending) -> None:
        heap = make(heap_cls, [5, 3, 9])
        assert 3 in heap
        assert 4 not in heap
        getattr(heap, extract)()
        assert (9 if descending else 3) not in heap

    def test_clear(self, heap_cls, extract, descending) -> None:
        heap = make(heap_cls, [5, 3, 9])
        heap.clear()
        assert len(heap) == 0
        assert not heap
        with pytest.raises(EmptyError):
            heap.peek()
        heap.insert(1)
        assert heap.peek() == 1

    def test_len_tracks_every_change(self, heap_cls, extract, descending) -> None:
        heap = heap_cls()
        for count in range(1, 6):
            heap.insert(count)
            assert len(heap) == count
        for count in range(4, -1, -1):
            getattr(heap, extract)()
            assert len(heap) == count

    def test_invariant_after_every_insert_and_extract(self, heap_cls, extract, descending) -> None:
        rng = random.Random(3)
        heap = heap_cls()
        for _ in range(200):
            heap.insert(rng.randrange(50))
            check_invariant(heap)
        for _ in range(200):
            getattr(heap, extract)()
            check_invariant(heap)

    def test_precedes_is_strict(self, heap_cls, extract, descending) -> None:
        heap = heap_cls()
        assert not heap._precedes(3, 3)
        assert heap._precedes(3, 2) == descending
        assert heap._precedes(2, 3) == (not descending)

    def test_large_heap(self, heap_cls, extract, descending) -> None:
        rng = random.Random(8)
        values = [rng.randrange(1000) for _ in range(20_000)]
        assert make(heap_cls, values).extract_all() == sorted(values, reverse=descending)

    @pytest.mark.parametrize("seed", range(30))
    def test_interleaved_operations_against_heapq(
        self, heap_cls, extract, descending, seed: int
    ) -> None:
        rng = random.Random(seed)
        heap = heap_cls()
        model: list[int] = []
        sign = -1 if descending else 1
        for _ in range(rng.randrange(0, 120)):
            if model and rng.random() < 0.4:
                assert getattr(heap, extract)() == sign * heapq.heappop(model)
            else:
                value = rng.randrange(30)
                heap.insert(value)
                heapq.heappush(model, sign * value)
            assert len(heap) == len(model)
            if model:
                assert heap.peek() == sign * model[0]
            check_invariant(heap)


@pytest.mark.parametrize(("heap_cls", "extract", "descending"), HEAPS)
class TestHeapify:
    def test_builds_a_valid_heap(self, heap_cls, extract, descending) -> None:
        values = [9, 4, 7, 1, 8, 2, 6, 3, 5, 0]
        heap = heap_cls()
        heap.heapify(values)
        check_invariant(heap)
        assert len(heap) == len(values)
        assert heap.extract_all() == sorted(values, reverse=descending)

    def test_empty_and_single_lists(self, heap_cls, extract, descending) -> None:
        heap = heap_cls()
        heap.heapify([])
        assert len(heap) == 0
        heap.heapify([5])
        assert heap.peek() == 5

    def test_the_given_list_is_not_modified(self, heap_cls, extract, descending) -> None:
        values = [9, 4, 7, 1, 8]
        heap = heap_cls()
        heap.heapify(values)
        heap.insert(100)
        getattr(heap, extract)()
        assert values == [9, 4, 7, 1, 8]

    def test_changing_the_list_afterwards_does_not_affect_the_heap(
        self, heap_cls, extract, descending
    ) -> None:
        values = [3, 1, 2]
        heap = heap_cls()
        heap.heapify(values)
        values.append(99)
        values[0] = -99
        assert heap.extract_all() == sorted([3, 1, 2], reverse=descending)

    def test_replaces_previous_contents(self, heap_cls, extract, descending) -> None:
        heap = make(heap_cls, [100, 200, 300])
        heap.heapify([1, 2])
        assert len(heap) == 2
        assert 100 not in heap
        assert heap.extract_all() == sorted([1, 2], reverse=descending)

    def test_heap_stays_usable_after_heapify(self, heap_cls, extract, descending) -> None:
        heap = heap_cls()
        heap.heapify([5, 3, 8])
        heap.insert(0)
        heap.insert(10)
        check_invariant(heap)
        assert heap.extract_all() == sorted([5, 3, 8, 0, 10], reverse=descending)

    @pytest.mark.parametrize("seed", range(25))
    def test_random_lists(self, heap_cls, extract, descending, seed: int) -> None:
        rng = random.Random(seed)
        values = [rng.randrange(20) for _ in range(rng.randrange(0, 80))]
        heap = heap_cls()
        heap.heapify(values)
        check_invariant(heap)
        assert heap.extract_all() == sorted(values, reverse=descending)


class TestVariants:
    def test_each_heap_has_only_its_own_extract_method(self) -> None:
        assert hasattr(MinHeap, "extract_min") and not hasattr(MinHeap, "extract_max")
        assert hasattr(MaxHeap, "extract_max") and not hasattr(MaxHeap, "extract_min")

    def test_the_same_values_give_opposite_orders(self) -> None:
        values = [4, 1, 3, 2]
        assert make(MinHeap, values).extract_all() == [1, 2, 3, 4]
        assert make(MaxHeap, values).extract_all() == [4, 3, 2, 1]

    def test_heap_base_is_abstract(self) -> None:
        with pytest.raises(TypeError):
            HeapBase()  # type: ignore[abstract]

    def test_both_heaps_share_the_base(self) -> None:
        assert issubclass(MinHeap, HeapBase) and issubclass(MaxHeap, HeapBase)
        assert issubclass(HeapBase, BaseStructure)

    def test_heapify_is_linear_in_comparisons(self) -> None:
        class Counted:
            calls = 0

            def __init__(self, value: int) -> None:
                self.value = value

            def __lt__(self, other: "Counted") -> bool:
                Counted.calls += 1
                return self.value < other.value

        n = 4096
        data = [Counted(v) for v in random.Random(2).sample(range(n), n)]
        heap: MinHeap[Any] = MinHeap()
        heap.heapify(data)
        assert Counted.calls <= 4 * n  # Floyd needs about 2n; inserting one by one needs ~n log n
