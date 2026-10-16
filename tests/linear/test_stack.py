import random
from collections.abc import Iterable

import pytest

from pydsa.core import BaseStructure
from pydsa.exc import EmptyError, PydsaError
from pydsa.linear.base import LinkedListBase
from pydsa.linear.stack import Stack


def make(values: Iterable[int] = ()) -> Stack[int]:
    stack = Stack[int]()
    for value in values:
        stack.push(value)
    return stack


class TestConstruction:
    def test_new_stack_is_empty(self) -> None:
        stack = Stack[int]()
        assert len(stack) == 0
        assert not stack

    def test_is_a_base_structure_but_not_a_list(self) -> None:
        stack = Stack[int]()
        assert isinstance(stack, BaseStructure)
        assert not isinstance(stack, LinkedListBase)

    def test_non_empty_stack_is_truthy(self) -> None:
        assert make([1])


class TestPushAndPop:
    def test_pops_in_reverse_order_of_pushing(self) -> None:
        stack = make([1, 2, 3])
        assert [stack.pop() for _ in range(3)] == [3, 2, 1]

    def test_len_follows_pushes_and_pops(self) -> None:
        stack = make([1, 2, 3])
        assert len(stack) == 3
        stack.pop()
        assert len(stack) == 2

    def test_becomes_falsy_once_drained(self) -> None:
        stack = make([1])
        stack.pop()
        assert not stack

    def test_pushing_after_popping_to_empty(self) -> None:
        stack = make([1])
        stack.pop()
        stack.push(2)
        assert stack.pop() == 2

    def test_equal_values_are_all_kept(self) -> None:
        stack = make([7, 7, 7])
        assert len(stack) == 3
        assert [stack.pop() for _ in range(3)] == [7, 7, 7]

    def test_none_is_an_ordinary_value(self) -> None:
        stack = Stack[int | None]()
        stack.push(None)
        assert len(stack) == 1
        assert stack.pop() is None

    def test_many_values(self) -> None:
        stack = make(range(10_000))
        assert [stack.pop() for _ in range(10_000)] == list(range(9_999, -1, -1))


class TestPeek:
    def test_returns_the_top_without_removing_it(self) -> None:
        stack = make([1, 2])
        assert stack.peek() == 2
        assert stack.peek() == 2
        assert len(stack) == 2

    def test_follows_pushes_and_pops(self) -> None:
        stack = make([1])
        stack.push(2)
        assert stack.peek() == 2
        stack.pop()
        assert stack.peek() == 1


class TestEmptyStack:
    @pytest.mark.parametrize("operation", ["pop", "peek"])
    def test_raises_empty_error_naming_the_stack(self, operation: str) -> None:
        with pytest.raises(EmptyError) as info:
            getattr(Stack[int](), operation)()
        assert str(info.value) == "Stack is empty"

    def test_error_does_not_leak_the_inner_list(self) -> None:
        with pytest.raises(EmptyError) as info:
            Stack[int]().pop()
        assert "SinglyList" not in str(info.value)

    def test_empty_error_is_a_pydsa_error(self) -> None:
        with pytest.raises(PydsaError):
            Stack[int]().peek()

    def test_failed_pop_leaves_the_stack_usable(self) -> None:
        stack = Stack[int]()
        with pytest.raises(EmptyError):
            stack.pop()
        stack.push(1)
        assert stack.pop() == 1


class TestClear:
    def test_clear_empties_the_stack(self) -> None:
        stack = make([1, 2, 3])
        stack.clear()
        assert len(stack) == 0
        assert not stack
        with pytest.raises(EmptyError):
            stack.pop()

    def test_stack_is_reusable_after_clear(self) -> None:
        stack = make([1, 2])
        stack.clear()
        stack.push(3)
        assert stack.peek() == 3
        assert len(stack) == 1

    def test_clear_on_an_empty_stack_is_harmless(self) -> None:
        stack = Stack[int]()
        stack.clear()
        assert len(stack) == 0


class TestEncapsulation:
    @pytest.mark.parametrize(
        "name",
        ["insert_first", "insert_last", "insert_at", "remove_at", "remove_first", "reverse"],
    )
    def test_list_operations_are_not_exposed(self, name: str) -> None:
        assert not hasattr(Stack[int](), name)

    def test_the_stack_is_not_indexable_or_iterable(self) -> None:
        stack = make([1, 2])
        with pytest.raises(TypeError):
            stack[0]  # type: ignore[index]
        with pytest.raises(TypeError):
            iter(stack)  # type: ignore[call-overload]


class TestAgainstPythonList:
    @pytest.mark.parametrize("seed", range(10))
    def test_random_operations_match_a_list_used_as_a_stack(self, seed: int) -> None:
        rng = random.Random(seed)
        stack = Stack[int]()
        model: list[int] = []
        for step in range(300):
            action = rng.choice(("push", "push", "pop", "peek", "clear"))
            if action == "push":
                stack.push(step)
                model.append(step)
            elif action == "clear" and rng.random() < 0.2:
                stack.clear()
                model.clear()
            elif model:
                if action == "pop":
                    assert stack.pop() == model.pop()
                elif action == "peek":
                    assert stack.peek() == model[-1]
            else:
                with pytest.raises(EmptyError):
                    stack.pop() if action == "pop" else stack.peek()
            assert len(stack) == len(model)
            assert bool(stack) is bool(model)
