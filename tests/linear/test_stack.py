import pytest

from pydsa import EmptyError, Stack


@pytest.fixture
def empty_stack() -> Stack[int]:
    return Stack[int]()


@pytest.fixture
def filled_stack() -> Stack[int]:
    s = Stack[int]()
    for v in [1, 2, 3]:
        s.push(v)
    return s


class TestConstruction:
    def test_new_stack_is_empty(self, empty_stack: Stack[int]) -> None:
        assert empty_stack.is_empty()
        assert len(empty_stack) == 0
        assert bool(empty_stack) is False


class TestPush:
    def test_into_empty(self, empty_stack: Stack[int]) -> None:
        empty_stack.push(1)
        assert len(empty_stack) == 1
        assert empty_stack.peek() == 1
        assert bool(empty_stack) is True

    def test_last_pushed_is_on_top(self, empty_stack: Stack[int]) -> None:
        for v in [1, 2, 3]:
            empty_stack.push(v)
        assert empty_stack.peek() == 3
        assert len(empty_stack) == 3


class TestPop:
    def test_raises_on_empty(self, empty_stack: Stack[int]) -> None:
        with pytest.raises(EmptyError):
            empty_stack.pop()

    def test_lifo_order(self, filled_stack: Stack[int]) -> None:
        assert filled_stack.pop() == 3
        assert filled_stack.pop() == 2
        assert filled_stack.pop() == 1

    def test_length_decreases(self, filled_stack: Stack[int]) -> None:
        filled_stack.pop()
        assert len(filled_stack) == 2

    def test_drains_to_empty(self, filled_stack: Stack[int]) -> None:
        for _ in range(3):
            filled_stack.pop()
        assert filled_stack.is_empty()
        with pytest.raises(EmptyError):
            filled_stack.pop()

    def test_usable_after_draining(self, filled_stack: Stack[int]) -> None:
        for _ in range(3):
            filled_stack.pop()
        filled_stack.push(99)
        assert filled_stack.peek() == 99
        assert len(filled_stack) == 1


class TestPeek:
    def test_raises_on_empty(self, empty_stack: Stack[int]) -> None:
        with pytest.raises(EmptyError):
            empty_stack.peek()

    def test_does_not_remove_element(self, filled_stack: Stack[int]) -> None:
        filled_stack.peek()
        assert len(filled_stack) == 3
        assert filled_stack.peek() == 3


class TestInterleavedOperations:
    def test_push_pop_push_maintains_lifo(self, empty_stack: Stack[int]) -> None:
        empty_stack.push(1)
        empty_stack.push(2)
        assert empty_stack.pop() == 2
        empty_stack.push(3)
        assert empty_stack.pop() == 3
        assert empty_stack.pop() == 1
        assert empty_stack.is_empty()