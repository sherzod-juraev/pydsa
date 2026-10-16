import random
from collections import deque
from collections.abc import Iterable

import pytest

from pydsa.core import BaseStructure
from pydsa.exc import EmptyError, PydsaError
from pydsa.linear.base import LinkedListBase
from pydsa.linear.queue import Queue


def make(values: Iterable[int] = ()) -> Queue[int]:
    queue = Queue[int]()
    for value in values:
        queue.enqueue(value)
    return queue


class TestConstruction:
    def test_new_queue_is_empty(self) -> None:
        queue = Queue[int]()
        assert len(queue) == 0
        assert not queue

    def test_is_a_base_structure_but_not_a_list(self) -> None:
        queue = Queue[int]()
        assert isinstance(queue, BaseStructure)
        assert not isinstance(queue, LinkedListBase)

    def test_non_empty_queue_is_truthy(self) -> None:
        assert make([1])


class TestEnqueueAndDequeue:
    def test_values_leave_in_the_order_they_arrived(self) -> None:
        queue = make([1, 2, 3])
        assert [queue.dequeue() for _ in range(3)] == [1, 2, 3]

    def test_len_follows_enqueues_and_dequeues(self) -> None:
        queue = make([1, 2, 3])
        assert len(queue) == 3
        queue.dequeue()
        assert len(queue) == 2

    def test_becomes_falsy_once_drained(self) -> None:
        queue = make([1])
        queue.dequeue()
        assert not queue

    def test_queue_works_again_after_draining(self) -> None:
        queue = make([1])
        queue.dequeue()
        queue.enqueue(2)
        queue.enqueue(3)
        assert [queue.dequeue(), queue.dequeue()] == [2, 3]

    def test_interleaved_use_keeps_fifo_order(self) -> None:
        queue = Queue[int]()
        queue.enqueue(1)
        queue.enqueue(2)
        assert queue.dequeue() == 1
        queue.enqueue(3)
        assert queue.dequeue() == 2
        assert queue.dequeue() == 3

    def test_repeated_fill_and_drain_cycles(self) -> None:
        queue = Queue[int]()
        for cycle in range(5):
            for value in range(3):
                queue.enqueue(cycle * 10 + value)
            assert [queue.dequeue() for _ in range(3)] == [cycle * 10 + v for v in range(3)]
            assert not queue

    def test_equal_values_are_all_kept(self) -> None:
        queue = make([7, 7, 7])
        assert len(queue) == 3

    def test_none_is_an_ordinary_value(self) -> None:
        queue = Queue[int | None]()
        queue.enqueue(None)
        assert len(queue) == 1
        assert queue.dequeue() is None

    def test_many_values(self) -> None:
        queue = make(range(10_000))
        assert [queue.dequeue() for _ in range(10_000)] == list(range(10_000))


class TestPeek:
    def test_returns_the_front_without_removing_it(self) -> None:
        queue = make([1, 2])
        assert queue.peek() == 1
        assert queue.peek() == 1
        assert len(queue) == 2

    def test_follows_enqueues_and_dequeues(self) -> None:
        queue = make([1])
        queue.enqueue(2)
        assert queue.peek() == 1
        queue.dequeue()
        assert queue.peek() == 2


class TestEmptyQueue:
    @pytest.mark.parametrize("operation", ["dequeue", "peek"])
    def test_raises_empty_error_naming_the_queue(self, operation: str) -> None:
        with pytest.raises(EmptyError) as info:
            getattr(Queue[int](), operation)()
        assert str(info.value) == "Queue is empty"

    def test_error_does_not_leak_the_inner_list(self) -> None:
        with pytest.raises(EmptyError) as info:
            Queue[int]().dequeue()
        assert "SinglyList" not in str(info.value)

    def test_empty_error_is_a_pydsa_error(self) -> None:
        with pytest.raises(PydsaError):
            Queue[int]().peek()

    def test_failed_dequeue_leaves_the_queue_usable(self) -> None:
        queue = Queue[int]()
        with pytest.raises(EmptyError):
            queue.dequeue()
        queue.enqueue(1)
        assert queue.dequeue() == 1


class TestClear:
    def test_clear_empties_the_queue(self) -> None:
        queue = make([1, 2, 3])
        queue.clear()
        assert len(queue) == 0
        assert not queue
        with pytest.raises(EmptyError):
            queue.dequeue()

    def test_queue_is_reusable_after_clear(self) -> None:
        queue = make([1, 2])
        queue.clear()
        queue.enqueue(3)
        queue.enqueue(4)
        assert [queue.dequeue(), queue.dequeue()] == [3, 4]

    def test_clear_on_an_empty_queue_is_harmless(self) -> None:
        queue = Queue[int]()
        queue.clear()
        assert len(queue) == 0


class TestEncapsulation:
    @pytest.mark.parametrize(
        "name",
        ["insert_first", "insert_last", "insert_at", "remove_at", "remove_last", "reverse"],
    )
    def test_list_operations_are_not_exposed(self, name: str) -> None:
        assert not hasattr(Queue[int](), name)

    def test_the_queue_is_not_indexable_or_iterable(self) -> None:
        queue = make([1, 2])
        with pytest.raises(TypeError):
            queue[0]  # type: ignore[index]
        with pytest.raises(TypeError):
            iter(queue)  # type: ignore[call-overload]


class TestAgainstDeque:
    @pytest.mark.parametrize("seed", range(10))
    def test_random_operations_match_a_deque(self, seed: int) -> None:
        rng = random.Random(seed)
        queue = Queue[int]()
        model: deque[int] = deque()
        for step in range(300):
            action = rng.choice(("enqueue", "enqueue", "dequeue", "peek", "clear"))
            if action == "enqueue":
                queue.enqueue(step)
                model.append(step)
            elif action == "clear" and rng.random() < 0.2:
                queue.clear()
                model.clear()
            elif model:
                if action == "dequeue":
                    assert queue.dequeue() == model.popleft()
                elif action == "peek":
                    assert queue.peek() == model[0]
            else:
                with pytest.raises(EmptyError):
                    queue.dequeue() if action == "dequeue" else queue.peek()
            assert len(queue) == len(model)
            assert bool(queue) is bool(model)
