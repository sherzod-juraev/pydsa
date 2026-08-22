import pytest

from pydsa import EmptyError, MaxHeap


class TestBasics:
    def test_new_heap_is_empty(self) -> None:
        h = MaxHeap[int]()
        assert h.is_empty()
        assert len(h) == 0

    def test_peek_raises_when_empty(self) -> None:
        with pytest.raises(EmptyError):
            MaxHeap[int]().peek()

    def test_extract_max_raises_when_empty(self) -> None:
        with pytest.raises(EmptyError):
            MaxHeap[int]().extract_max()


class TestInsertAndPeek:
    def test_peek_returns_maximum(self) -> None:
        h = MaxHeap[int]()
        for v in [3, 9, 1, 7]:
            h.insert(v)
        assert h.peek() == 9

    def test_peek_does_not_remove(self) -> None:
        h = MaxHeap[int]()
        h.insert(5)
        h.peek()
        assert len(h) == 1

    def test_contains(self) -> None:
        h = MaxHeap[int]()
        h.insert(5)
        assert 5 in h
        assert 99 not in h


class TestExtractMax:
    def test_extract_order_is_descending(self) -> None:
        h = MaxHeap[int]()
        for v in [3, 9, 1, 7, 5]:
            h.insert(v)
        result = [h.extract_max() for _ in range(len(h))]
        assert result == [9, 7, 5, 3, 1]

    def test_single_element(self) -> None:
        h = MaxHeap[int]()
        h.insert(42)
        assert h.extract_max() == 42
        assert h.is_empty()


class TestExtractAll:
    def test_extract_all_sorted_descending(self) -> None:
        h = MaxHeap[int]()
        for v in [3, 9, 1, 7, 5]:
            h.insert(v)
        assert h.extract_all() == [9, 7, 5, 3, 1]

    def test_extract_all_empties_the_heap(self) -> None:
        h = MaxHeap[int]()
        for v in [3, 1, 2]:
            h.insert(v)
        h.extract_all()
        assert h.is_empty()

    def test_extract_all_on_empty_heap(self) -> None:
        assert MaxHeap[int]().extract_all() == []


class TestHeapify:
    def test_heapify_preserves_all_elements(self) -> None:
        h = MaxHeap[int]()
        h.heapify([5, 3, 8, 1, 9, 2])
        assert len(h) == 6
        assert h.peek() == 9

    def test_heapify_matches_extract_all_of_sorted(self) -> None:
        data = [5, 3, 8, 1, 9, 2, 7]
        h = MaxHeap[int]()
        h.heapify(data)
        assert h.extract_all() == sorted(data, reverse=True)

    def test_heapify_does_not_mutate_input(self) -> None:
        data = [5, 3, 8]
        h = MaxHeap[int]()
        h.heapify(data)
        h.insert(100)
        assert data == [5, 3, 8]  # original list untouched


class TestClear:
    def test_clear(self) -> None:
        h = MaxHeap[int]()
        h.insert(5)
        h.clear()
        assert h.is_empty()