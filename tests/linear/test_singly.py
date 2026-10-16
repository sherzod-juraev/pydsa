"""Behaviour specific to the singly linked list."""

import pytest

from pydsa.linear.singly import SinglyList


def make(values: range | list[int]) -> SinglyList[int]:
    items = SinglyList[int]()
    for value in values:
        items.insert_last(value)
    return items


class TestNodes:
    def test_nodes_have_no_back_link(self) -> None:
        items = make([1, 2])
        assert not hasattr(items._head, "prev")

    def test_tail_is_the_last_node_and_ends_the_chain(self) -> None:
        items = make([1, 2, 3])
        assert items._tail is not None
        assert items._tail.value == 3
        assert items._tail.next is None

    def test_single_element_is_both_head_and_tail(self) -> None:
        items = make([1])
        assert items._head is items._tail


class TestTailPointer:
    def test_remove_last_moves_the_tail_back_one_node(self) -> None:
        items = make([1, 2, 3])
        second = items._node_at(1)
        items.remove_last()
        assert items._tail is second
        assert second.next is None

    def test_removing_down_to_one_node_makes_head_and_tail_equal(self) -> None:
        items = make([1, 2])
        items.remove_last()
        assert items._head is items._tail

    def test_remove_first_of_a_single_element_clears_the_tail(self) -> None:
        items = make([1])
        items.remove_first()
        assert items._head is None
        assert items._tail is None

    def test_remove_at_last_index_moves_the_tail(self) -> None:
        items = make([1, 2, 3])
        second = items._node_at(1)
        items.remove_at(2)
        assert items._tail is second

    def test_insert_first_into_an_empty_list_sets_the_tail(self) -> None:
        items = SinglyList[int]()
        items.insert_first(1)
        assert items._tail is items._head

    def test_insert_first_into_a_non_empty_list_keeps_the_tail(self) -> None:
        items = make([2])
        tail = items._tail
        items.insert_first(1)
        assert items._tail is tail


class TestRemovedNodes:
    def test_removed_middle_node_does_not_keep_a_link_into_the_list(self) -> None:
        items = make([1, 2, 3])
        node = items._node_at(1)
        items.remove_at(1)
        assert node.next is None

    def test_relinking_skips_exactly_the_removed_node(self) -> None:
        items = make([1, 2, 3, 4])
        before = items._node_at(1)
        after = items._node_at(3)
        items.remove_at(2)
        assert before.next is after


class TestReverse:
    def test_reverse_swaps_the_head_and_tail_nodes(self) -> None:
        items = make([1, 2, 3])
        old_head, old_tail = items._head, items._tail
        items.reverse()
        assert items._head is old_tail
        assert items._tail is old_head
        assert old_head is not None
        assert old_head.next is None

    def test_reversing_an_empty_list_keeps_it_empty(self) -> None:
        items = SinglyList[int]()
        items.reverse()
        assert items._head is None
        assert items._tail is None


class TestInsertAt:
    def test_insert_in_the_middle_links_both_neighbours(self) -> None:
        items = make([1, 3])
        first = items._node_at(0)
        last = items._node_at(1)
        items.insert_at(1, 2)
        assert first.next is not None
        assert first.next.value == 2
        assert first.next.next is last


class TestLongLists:
    SIZE = 50_000

    def test_iteration_copy_and_reverse_do_not_recurse(self) -> None:
        items = make(range(self.SIZE))
        assert sum(items) == sum(range(self.SIZE))
        clone = items.copy()
        clone.reverse()
        assert clone.get_first() == self.SIZE - 1
        assert len(clone) == self.SIZE

    def test_clearing_a_long_list_does_not_overflow_the_stack(self) -> None:
        items = make(range(self.SIZE))
        items.clear()
        assert len(items) == 0

    def test_get_last_is_constant_time(self) -> None:
        items = make(range(self.SIZE))
        # 5_000 calls on 50_000 nodes would take minutes if each one walked the chain
        assert all(items.get_last() == self.SIZE - 1 for _ in range(5_000))


@pytest.mark.parametrize("size", [1, 2, 3])
def test_node_at_walks_from_the_head(size: int) -> None:
    items = make(range(size))
    assert [items._node_at(i).value for i in range(size)] == list(range(size))
