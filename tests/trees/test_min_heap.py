import pytest

from pydsa import EmptyError, MinHeap


class TestBasics:
    def test_new_heap_is_empty(self) -> None:
        h = MinHeap[int]()
        assert h.is_empty()
        assert len(h) == 0

    def test_peek_raises_when_empty(self) -> None:
        with pytest.raises(EmptyError):
            MinHeap[int]().peek()

    def test_extract_min_raises_when_empty(self) -> None:
        with pytest.raises(EmptyError):
            MinHeap[int]().extract_min()


class TestInsertAndPeek:
    def test_peek_returns_minimum(self) -> None:
        h = MinHeap[int]()
        for v in [3, 9, 1, 7]:
            h.insert(v)
        assert h.peek() == 1

    def test_contains(self) -> None:
        h = MinHeap[int]()
        h.insert(5)
        assert 5 in h
        assert 99 not in h


class TestExtractMin:
    def test_extract_order_is_ascending(self) -> None:
        h = MinHeap[int]()
        for v in [3, 9, 1, 7, 5]:
            h.insert(v)
        result = [h.extract_min() for _ in range(len(h))]
        assert result == [1, 3, 5, 7, 9]

    def test_single_element(self) -> None:
        h = MinHeap[int]()
        h.insert(42)
        assert h.extract_min() == 42
        assert h.is_empty()


class TestExtractAll:
    def test_extract_all_sorted_ascending(self) -> None:
        h = MinHeap[int]()
        for v in [3, 9, 1, 7, 5]:
            h.insert(v)
        assert h.extract_all() == [1, 3, 5, 7, 9]

    def test_extract_all_empties_the_heap(self) -> None:
        h = MinHeap[int]()
        for v in [3, 1, 2]:
            h.insert(v)
        h.extract_all()
        assert h.is_empty()

    def test_extract_all_on_empty_heap(self) -> None:
        assert MinHeap[int]().extract_all() == []


class TestHeapify:
    def test_heapify_preserves_all_elements(self) -> None:
        h = MinHeap[int]()
        h.heapify([5, 3, 8, 1, 9, 2])
        assert len(h) == 6
        assert h.peek() == 1

    def test_heapify_matches_extract_all_of_sorted(self) -> None:
        data = [5, 3, 8, 1, 9, 2, 7]
        h = MinHeap[int]()
        h.heapify(data)
        assert h.extract_all() == sorted(data)

    def test_heapify_does_not_mutate_input(self) -> None:
        data = [5, 3, 8]
        h = MinHeap[int]()
        h.heapify(data)
        h.insert(-100)
        assert data == [5, 3, 8]


class TestClear:
    def test_clear(self) -> None:
        h = MinHeap[int]()
        h.insert(5)
        h.clear()
        assert h.is_empty()