import pytest
from pydsa import Queue
from pydsa.exc import EmptyError


class TestQueueInit:
    """__init__"""

    def test_EmptyError_queue_has_zero_length(self):
        q = Queue()
        assert len(q) == 0

    def test_EmptyError_queue_is_EmptyError(self):
        q = Queue()
        assert q.is_empty()


class TestQueueEnqueue:
    """enqueue"""

    def test_enqueue_increases_length(self):
        q = Queue()
        q.enqueue(10)
        assert len(q) == 1

    def test_enqueue_multiple(self):
        q = Queue()
        q.enqueue(10)
        q.enqueue(20)
        q.enqueue(30)
        assert len(q) == 3

    def test_enqueue_and_peek(self):
        q = Queue()
        q.enqueue(42)
        assert q.peek() == 42


class TestQueueDequeue:
    """dequeue"""

    def test_dequeue_returns_first_enqueued(self):
        q = Queue()
        q.enqueue(10)
        q.enqueue(20)
        assert q.dequeue() == 10

    def test_dequeue_removes_element(self):
        q = Queue()
        q.enqueue(10)
        q.enqueue(20)
        q.dequeue()
        assert len(q) == 1
        assert q.peek() == 20

    def test_dequeue_until_EmptyError(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        q.dequeue()
        q.dequeue()
        q.dequeue()
        assert q.is_empty()

    def test_dequeue_on_EmptyError_raises(self):
        q = Queue()
        with pytest.raises(EmptyError):
            q.dequeue()

    def test_dequeue_updates_tail_when_single_element(self):
        q = Queue()
        q.enqueue(1)
        q.dequeue()
        assert q.is_empty()
        q.enqueue(2)
        assert q.peek() == 2


class TestQueuePeek:
    """peek"""

    def test_peek_does_not_remove(self):
        q = Queue()
        q.enqueue(10)
        assert q.peek() == 10
        assert len(q) == 1

    def test_peek_on_EmptyError_raises(self):
        q = Queue()
        with pytest.raises(EmptyError):
            q.peek()


class TestQueueFIFO:
    """FIFO behavior"""

    def test_fifo_order(self):
        q = Queue()
        for v in [1, 2, 3, 4, 5]:
            q.enqueue(v)
        result = []
        while not q.is_empty():
            result.append(q.dequeue())
        assert result == [1, 2, 3, 4, 5]

    def test_interleaved_enqueue_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        assert q.dequeue() == 1
        q.enqueue(3)
        assert q.dequeue() == 2
        assert q.dequeue() == 3
        assert q.is_empty()


class TestQueueLargeData:
    """Large data"""

    def test_many_enqueue_dequeue(self):
        q = Queue()
        n = 1000
        for i in range(n):
            q.enqueue(i)
        for i in range(n):
            assert q.dequeue() == i
        assert q.is_empty()