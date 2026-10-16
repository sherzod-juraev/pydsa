"""Behaviour specific to the doubly linked list."""

import random

import pytest

from pydsa.linear.doubly import DoublyList


def make(values: range | list[int]) -> DoublyList[int]:
    items = DoublyList[int]()
    for value in values:
        items.insert_last(value)
    return items


class TestReversedIteration:
    def test_empty_list_yields_nothing(self) -> None:
        assert list(reversed(DoublyList[int]())) == []

    def test_single_element(self) -> None:
        assert list(reversed(make([1]))) == [1]

    def test_yields_values_back_to_front(self) -> None:
        assert list(reversed(make([1, 2, 3]))) == [3, 2, 1]

    def test_can_be_repeated_and_leaves_the_list_alone(self) -> None:
        items = make([1, 2, 3])
        assert list(reversed(items)) == list(reversed(items)) == [3, 2, 1]
        assert list(items) == [1, 2, 3]

    def test_stays_consistent_through_random_mutations(self) -> None:
        rng = random.Random(7)
        items = DoublyList[int]()
        model: list[int] = []
        for step in range(200):
            action = rng.choice(("first", "last", "pop_first", "pop_last", "reverse"))
            if action == "first":
                items.insert_first(step)
                model.insert(0, step)
            elif action == "last":
                items.insert_last(step)
                model.append(step)
            elif action == "pop_first" and model:
                assert items.remove_first() == model.pop(0)
            elif action == "pop_last" and model:
                assert items.remove_last() == model.pop()
            elif action == "reverse":
                items.reverse()
                model.reverse()
            assert list(reversed(items)) == model[::-1]


class TestLinks:
    def test_insert_first_links_the_old_head_back(self) -> None:
        items = make([2])
        old_head = items._head
        items.insert_first(1)
        assert old_head is not None
        assert old_head.prev is items._head
        assert items._head is not None
        assert items._head.prev is None

    def test_insert_last_links_the_new_tail_back(self) -> None:
        items = make([1])
        items.insert_last(2)
        assert items._tail is not None
        assert items._tail.prev is items._head
        assert items._tail.next is None

    def test_insert_in_the_middle_links_all_four_pointers(self) -> None:
        items = make([1, 3])
        left, right = items._node_at(0), items._node_at(1)
        items.insert_at(1, 2)
        middle = left.next
        assert middle is not None
        assert middle.value == 2
        assert middle.prev is left
        assert middle.next is right
        assert right.prev is middle

    def test_remove_last_makes_the_previous_node_the_tail(self) -> None:
        items = make([1, 2, 3])
        second = items._node_at(1)
        items.remove_last()
        assert items._tail is second
        assert second.next is None

    def test_remove_first_makes_the_next_node_the_head(self) -> None:
        items = make([1, 2, 3])
        second = items._node_at(1)
        items.remove_first()
        assert items._head is second
        assert second.prev is None

    def test_remove_in_the_middle_bridges_both_neighbours(self) -> None:
        items = make([1, 2, 3])
        left, right = items._node_at(0), items._node_at(2)
        items.remove_at(1)
        assert left.next is right
        assert right.prev is left

    def test_removing_by_value_keeps_the_back_links_intact(self) -> None:
        items = make([1, 2, 3, 4])
        items.remove(2)
        assert list(items) == [1, 3, 4]
        assert list(reversed(items)) == [4, 3, 1]

    @pytest.mark.parametrize("remove", ["first", "last", "middle"])
    def test_removed_nodes_are_fully_detached(self, remove: str) -> None:
        items = make([1, 2, 3])
        index = {"first": 0, "last": 2, "middle": 1}[remove]
        node = items._node_at(index)
        items.remove_at(index)
        assert node.prev is None
        assert node.next is None

    def test_reverse_flips_every_link(self) -> None:
        items = make([1, 2, 3])
        forward = list(items)
        items.reverse()
        assert list(reversed(items)) == forward
        assert items._head is not None
        assert items._head.prev is None
        assert items._tail is not None
        assert items._tail.next is None


class TestNearestEnd:
    """_node_at must walk from the closer end, so a broken far half is never touched."""

    def test_front_half_is_reached_from_the_head(self) -> None:
        items = make(range(8))
        third = items._node_at(3)
        third.prev = None  # backward links in the front half are not needed
        assert [items._node_at(i).value for i in range(0, 4)] == [0, 1, 2, 3]

    def test_back_half_is_reached_from_the_tail(self) -> None:
        items = make(range(8))
        third = items._node_at(3)
        third.next = None  # forward links up to the middle are cut
        assert [items._node_at(i).value for i in range(5, 8)] == [5, 6, 7]

    def test_every_index_agrees_with_a_plain_list(self) -> None:
        for size in range(1, 10):
            items = make(range(size))
            assert [items[i] for i in range(size)] == list(range(size))
            assert [items[-i] for i in range(1, size + 1)] == list(range(size))[::-1]

    def test_insert_at_and_remove_at_work_from_both_halves(self) -> None:
        items = make(range(10))
        items.insert_at(8, 99)
        items.insert_at(1, 98)
        assert list(items) == [0, 98, 1, 2, 3, 4, 5, 6, 7, 99, 8, 9]
        assert items.remove_at(9) == 99
        assert items.remove_at(1) == 98
        assert list(items) == list(range(10))
        assert list(reversed(items)) == list(range(10))[::-1]


class TestLongLists:
    SIZE = 50_000

    def test_iteration_copy_and_reverse_do_not_recurse(self) -> None:
        items = make(range(self.SIZE))
        clone = items.copy()
        clone.reverse()
        assert clone.get_first() == self.SIZE - 1
        assert sum(reversed(clone)) == sum(range(self.SIZE))

    def test_clearing_a_long_list_does_not_overflow_the_stack(self) -> None:
        items = make(range(self.SIZE))
        items.clear()
        assert len(items) == 0

    def test_both_ends_are_constant_time(self) -> None:
        items = make(range(self.SIZE))
        for _ in range(5_000):
            assert items.get_last() == self.SIZE - 1
        for expected in range(5_000):
            assert items.remove_first() == expected
        for expected in range(self.SIZE - 1, self.SIZE - 5_001, -1):
            assert items.remove_last() == expected
