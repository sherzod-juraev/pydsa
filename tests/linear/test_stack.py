import pytest
from pydsa import Stack
from pydsa.exc import Empty


class TestStackInit:
    """__init__"""

    def test_empty_stack_has_zero_length(self):
        s = Stack()
        assert len(s) == 0

    def test_empty_stack_is_empty(self):
        s = Stack()
        assert s.is_empty()


class TestStackPush:
    """push"""

    def test_push_increases_length(self):
        s = Stack()
        s.push(10)
        assert len(s) == 1

    def test_push_multiple(self):
        s = Stack()
        s.push(10)
        s.push(20)
        s.push(30)
        assert len(s) == 3

    def test_push_and_peek(self):
        s = Stack()
        s.push(42)
        assert s.peek() == 42


class TestStackPop:
    """pop"""

    def test_pop_returns_last_pushed(self):
        s = Stack()
        s.push(10)
        s.push(20)
        assert s.pop() == 20

    def test_pop_removes_element(self):
        s = Stack()
        s.push(10)
        s.push(20)
        s.pop()
        assert len(s) == 1
        assert s.peek() == 10

    def test_pop_until_empty(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        s.pop()
        s.pop()
        s.pop()
        assert s.is_empty()

    def test_pop_on_empty_raises(self):
        s = Stack()
        with pytest.raises(Empty):
            s.pop()


class TestStackPeek:
    """peek"""

    def test_peek_does_not_remove(self):
        s = Stack()
        s.push(10)
        assert s.peek() == 10
        assert len(s) == 1

    def test_peek_on_empty_raises(self):
        s = Stack()
        with pytest.raises(Empty):
            s.peek()


class TestStackLIFO:
    """LIFO behavior"""

    def test_lifo_order(self):
        s = Stack()
        for v in [1, 2, 3, 4, 5]:
            s.push(v)
        result = []
        while not s.is_empty():
            result.append(s.pop())
        assert result == [5, 4, 3, 2, 1]

    def test_interleaved_push_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        s.push(3)
        assert s.pop() == 3
        assert s.pop() == 1
        assert s.is_empty()


class TestStackLargeData:
    """Large data"""

    def test_many_push_pop(self):
        s = Stack()
        n = 1000
        for i in range(n):
            s.push(i)
        for i in range(n - 1, -1, -1):
            assert s.pop() == i
        assert s.is_empty()