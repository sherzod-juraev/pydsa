import pytest
from pydsa import MaxHeap
from pydsa.exc import EmptyError


class TestMaxHeapInit:
    """__init__"""

    def test_EmptyError_heap_has_zero_length(self):
        heap = MaxHeap()
        assert len(heap) == 0

    def test_EmptyError_heap_is_falsy(self):
        heap = MaxHeap()
        assert not heap

    def test_EmptyError_heap_is_empty(self):
        heap = MaxHeap()
        assert heap.is_empty()


class TestMaxHeapInsert:
    """insert"""

    def test_insert_increases_length(self):
        heap = MaxHeap()
        heap.insert(10)
        assert len(heap) == 1

    def test_insert_multiple(self):
        heap = MaxHeap()
        for v in [5, 3, 8, 1, 4]:
            heap.insert(v)
        assert len(heap) == 5

    def test_peek_returns_max(self):
        heap = MaxHeap()
        heap.insert(5)
        assert heap.peek() == 5
        heap.insert(8)
        assert heap.peek() == 8
        heap.insert(3)
        assert heap.peek() == 8
        heap.insert(10)
        assert heap.peek() == 10

    def test_insert_duplicates(self):
        heap = MaxHeap()
        heap.insert(5)
        heap.insert(5)
        heap.insert(5)
        assert len(heap) == 3
        assert heap.peek() == 5


class TestMaxHeapExtract:
    """extract_max"""

    def test_extract_returns_max(self):
        heap = MaxHeap()
        for v in [5, 3, 8, 1, 4]:
            heap.insert(v)
        assert heap.extract_max() == 8
        assert heap.extract_max() == 5
        assert heap.extract_max() == 4
        assert heap.extract_max() == 3
        assert heap.extract_max() == 1

    def test_extract_decreases_length(self):
        heap = MaxHeap()
        heap.insert(10)
        heap.insert(20)
        heap.extract_max()
        assert len(heap) == 1

    def test_extract_until_EmptyError(self):
        heap = MaxHeap()
        heap.insert(10)
        heap.insert(20)
        heap.extract_max()
        heap.extract_max()
        assert heap.is_empty()

    def test_extract_on_EmptyError_raises(self):
        heap = MaxHeap()
        with pytest.raises(EmptyError):
            heap.extract_max()


class TestMaxHeapPeek:
    """peek"""

    def test_peek_does_not_remove(self):
        heap = MaxHeap()
        heap.insert(10)
        assert heap.peek() == 10
        assert len(heap) == 1

    def test_peek_on_EmptyError_raises(self):
        heap = MaxHeap()
        with pytest.raises(EmptyError):
            heap.peek()


class TestMaxHeapHeapify:
    """heapify"""

    def test_heapify_builds_valid_heap(self):
        heap = MaxHeap()
        heap.heapify([5, 3, 8, 1, 4, 7, 9, 2, 6])
        assert len(heap) == 9
        assert heap.peek() == 9

    def test_heapify_EmptyError_list(self):
        heap = MaxHeap()
        heap.heapify([])
        assert heap.is_empty()

    def test_heapify_single_element(self):
        heap = MaxHeap()
        heap.heapify([42])
        assert heap.peek() == 42

    def test_heapify_preserves_copy(self):
        original = [5, 1, 3]
        heap = MaxHeap()
        heap.heapify(original)
        assert original == [5, 1, 3]
        assert heap.peek() == 5

    def test_operations_after_heapify(self):
        heap = MaxHeap()
        heap.heapify([5, 3, 8])
        heap.insert(10)
        assert heap.peek() == 10
        assert heap.extract_max() == 10
        assert heap.extract_max() == 8


class TestMaxHeapExtractAll:
    """extract_all"""

    def test_extract_all_sorted_descending(self):
        heap = MaxHeap()
        for v in [5, 3, 8, 1, 4, 7, 9, 2, 6]:
            heap.insert(v)
        assert heap.extract_all() == [9, 8, 7, 6, 5, 4, 3, 2, 1]

    def test_extract_all_empties_heap(self):
        heap = MaxHeap()
        heap.insert(10)
        heap.insert(20)
        heap.extract_all()
        assert heap.is_empty()

    def test_extract_all_EmptyError_heap(self):
        heap = MaxHeap()
        assert heap.extract_all() == []


class TestMaxHeapContains:
    """__contains__"""

    def test_contains_existing(self):
        heap = MaxHeap()
        heap.insert(10)
        assert 10 in heap

    def test_contains_non_existing(self):
        heap = MaxHeap()
        heap.insert(10)
        assert 20 not in heap

    def test_contains_EmptyError(self):
        heap = MaxHeap()
        assert 10 not in heap


class TestMaxHeapClear:
    """clear"""

    def test_clear_empties_heap(self):
        heap = MaxHeap()
        heap.insert(10)
        heap.insert(20)
        heap.clear()
        assert heap.is_empty()
        assert len(heap) == 0

    def test_clear_EmptyError_heap(self):
        heap = MaxHeap()
        heap.clear()
        assert heap.is_empty()


class TestMaxHeapLargeData:
    """Large data"""

    def test_many_inserts_and_extracts(self):
        heap = MaxHeap()
        n = 500
        for i in range(n):
            heap.insert(i)
        for i in range(n - 1, -1, -1):
            assert heap.extract_max() == i

    def test_heapify_large(self):
        heap = MaxHeap()
        arr = list(range(500))
        heap.heapify(arr)
        for i in range(499, -1, -1):
            assert heap.extract_max() == i