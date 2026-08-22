import pytest

from pydsa import EmptyError, Queue


@pytest.fixture
def empty_queue() -> Queue[int]:
    return Queue[int]()


@pytest.fixture
def filled_queue() -> Queue[int]:
    q = Queue[int]()
    for v in [1, 2, 3]:
        q.enqueue(v)
    return q


class TestConstruction:
    def test_new_queue_is_empty(self, empty_queue: Queue[int]) -> None:
        assert empty_queue.is_empty()
        assert len(empty_queue) == 0
        assert bool(empty_queue) is False


class TestEnqueue:
    def test_into_empty(self, empty_queue: Queue[int]) -> None:
        empty_queue.enqueue(1)
        assert len(empty_queue) == 1
        assert empty_queue.peek() == 1
        assert bool(empty_queue) is True

    def test_first_enqueued_stays_at_front(self, empty_queue: Queue[int]) -> None:
        for v in [1, 2, 3]:
            empty_queue.enqueue(v)
        assert empty_queue.peek() == 1
        assert len(empty_queue) == 3


class TestDequeue:
    def test_raises_on_empty(self, empty_queue: Queue[int]) -> None:
        with pytest.raises(EmptyError):
            empty_queue.dequeue()

    def test_fifo_order(self, filled_queue: Queue[int]) -> None:
        assert filled_queue.dequeue() == 1
        assert filled_queue.dequeue() == 2
        assert filled_queue.dequeue() == 3

    def test_length_decreases(self, filled_queue: Queue[int]) -> None:
        filled_queue.dequeue()
        assert len(filled_queue) == 2

    def test_drains_to_empty_and_clears_tail(self, filled_queue: Queue[int]) -> None:
        for _ in range(3):
            filled_queue.dequeue()
        assert filled_queue.is_empty()
        with pytest.raises(EmptyError):
            filled_queue.dequeue()


class TestPeek:
    def test_raises_on_empty(self, empty_queue: Queue[int]) -> None:
        with pytest.raises(EmptyError):
            empty_queue.peek()

    def test_does_not_remove_element(self, filled_queue: Queue[int]) -> None:
        filled_queue.peek()
        assert len(filled_queue) == 3
        assert filled_queue.peek() == 1


class TestInterleavedOperations:
    def test_enqueue_dequeue_enqueue_maintains_fifo(self, empty_queue: Queue[int]) -> None:
        empty_queue.enqueue(1)
        empty_queue.enqueue(2)
        assert empty_queue.dequeue() == 1
        empty_queue.enqueue(3)
        assert empty_queue.dequeue() == 2
        assert empty_queue.dequeue() == 3
        assert empty_queue.is_empty()

    def test_tail_pointer_correct_after_full_drain_and_reenqueue(
        self, empty_queue: Queue[int]
    ) -> None:
        empty_queue.enqueue(1)
        empty_queue.dequeue()
        empty_queue.enqueue(2)
        empty_queue.enqueue(3)
        assert empty_queue.dequeue() == 2
        assert empty_queue.dequeue() == 3