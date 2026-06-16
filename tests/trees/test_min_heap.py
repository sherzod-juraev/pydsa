import pytest
from pydsa import MinHeap
from pydsa.exc import EmptyError


class TestMinHeapInit:
    """__init__"""

    def test_EmptyError_heap_has_zero_length(self):
        heap = MinHeap()
        assert len(heap) == 0

    def test_EmptyError_heap_is_falsy(self):
        heap = MinHeap()
        assert not heap

    def test_EmptyError_heap_is_empty(self):
        heap = MinHeap()
        assert heap.is_empty()


class TestMinHeapInsert:
    """insert"""

    def test_insert_increases_length(self):
        heap = MinHeap()
        heap.insert(10)
        assert len(heap) == 1

    def test_insert_multiple(self):
        heap = MinHeap()
        for v in [5, 3, 8, 1, 4]:
            heap.insert(v)
        assert len(heap) == 5

    def test_peek_returns_min(self):
        heap = MinHeap()
        heap.insert(5)
        assert heap.peek() == 5
        heap.insert(3)
        assert heap.peek() == 3
        heap.insert(8)
        assert heap.peek() == 3
        heap.insert(1)
        assert heap.peek() == 1

    def test_insert_duplicates(self):
        heap = MinHeap()
        heap.insert(5)
        heap.insert(5)
        heap.insert(5)
        assert len(heap) == 3
        assert heap.peek() == 5


class TestMinHeapExtract:
    """extract_min"""

    def test_extract_returns_min(self):
        heap = MinHeap()
        for v in [5, 3, 8, 1, 4]:
            heap.insert(v)
        assert heap.extract_min() == 1
        assert heap.extract_min() == 3
        assert heap.extract_min() == 4
        assert heap.extract_min() == 5
        assert heap.extract_min() == 8

    def test_extract_decreases_length(self):
        heap = MinHeap()
        heap.insert(10)
        heap.insert(20)
        heap.extract_min()
        assert len(heap) == 1

    def test_extract_until_EmptyError(self):
        heap = MinHeap()
        heap.insert(10)
        heap.insert(20)
        heap.extract_min()
        heap.extract_min()
        assert heap.is_empty()

    def test_extract_on_EmptyError_raises(self):
        heap = MinHeap()
        with pytest.raises(EmptyError):
            heap.extract_min()


class TestMinHeapPeek:
    """peek"""

    def test_peek_does_not_remove(self):
        heap = MinHeap()
        heap.insert(10)
        assert heap.peek() == 10
        assert len(heap) == 1

    def test_peek_on_EmptyError_raises(self):
        heap = MinHeap()
        with pytest.raises(EmptyError):
            heap.peek()


class TestMinHeapHeapify:
    """heapify"""

    def test_heapify_builds_valid_heap(self):
        heap = MinHeap()
        heap.heapify([5, 3, 8, 1, 4, 7, 9, 2, 6])
        assert len(heap) == 9
        assert heap.peek() == 1

    def test_heapify_EmptyError_list(self):
        heap = MinHeap()
        heap.heapify([])
        assert heap.is_empty()

    def test_heapify_single_element(self):
        heap = MinHeap()
        heap.heapify([42])
        assert heap.peek() == 42

    def test_heapify_preserves_copy(self):
        original = [5, 1, 3]
        heap = MinHeap()
        heap.heapify(original)
        assert original == [5, 1, 3]  # unchanged
        assert heap.peek() == 1

    def test_operations_after_heapify(self):
        heap = MinHeap()
        heap.heapify([5, 3, 8])
        heap.insert(1)
        assert heap.peek() == 1
        assert heap.extract_min() == 1
        assert heap.extract_min() == 3


class TestMinHeapExtractAll:
    """extract_all"""

    def test_extract_all_sorted(self):
        heap = MinHeap()
        for v in [5, 3, 8, 1, 4, 7, 9, 2, 6]:
            heap.insert(v)
        assert heap.extract_all() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_extract_all_empties_heap(self):
        heap = MinHeap()
        heap.insert(10)
        heap.insert(20)
        heap.extract_all()
        assert heap.is_empty()

    def test_extract_all_EmptyError_heap(self):
        heap = MinHeap()
        assert heap.extract_all() == []


class TestMinHeapContains:
    """__contains__"""

    def test_contains_existing(self):
        heap = MinHeap()
        heap.insert(10)
        assert 10 in heap

    def test_contains_non_existing(self):
        heap = MinHeap()
        heap.insert(10)
        assert 20 not in heap

    def test_contains_EmptyError(self):
        heap = MinHeap()
        assert 10 not in heap


class TestMinHeapClear:
    """clear"""

    def test_clear_empties_heap(self):
        heap = MinHeap()
        heap.insert(10)
        heap.insert(20)
        heap.clear()
        assert heap.is_empty()
        assert len(heap) == 0

    def test_clear_EmptyError_heap(self):
        heap = MinHeap()
        heap.clear()
        assert heap.is_empty()


class TestMinHeapLargeData:
    """Large data"""

    def test_many_inserts_and_extracts(self):
        heap = MinHeap()
        n = 500
        for i in range(n, 0, -1):
            heap.insert(i)
        for i in range(1, n + 1):
            assert heap.extract_min() == i

    def test_heapify_large(self):
        heap = MinHeap()
        arr = list(range(500, 0, -1))
        heap.heapify(arr)
        for i in range(1, 501):
            assert heap.extract_min() == i