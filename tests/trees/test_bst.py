import random

import pytest

from pydsa.trees import BSTree
from pydsa.trees.base import _BinaryNode


def make(values) -> BSTree[int]:
    tree: BSTree[int] = BSTree()
    for value in values:
        tree.insert(value)
    return tree


def check_invariants(tree: BSTree[int]) -> None:
    """Every value lies strictly between the bounds set by its ancestors."""
    count = 0
    stack: list[tuple[_BinaryNode[int] | None, int | None, int | None]] = [(tree._root, None, None)]
    while stack:
        node, low, high = stack.pop()
        if node is None:
            continue
        count += 1
        assert low is None or node.value > low
        assert high is None or node.value < high
        stack.append((node.left, low, node.value))
        stack.append((node.right, node.value, high))
    assert count == len(tree)


#          5
#       3     8
#      1 4   7 9
CLASSIC = [5, 3, 8, 1, 4, 7, 9]


class TestShape:
    def test_preorder(self) -> None:
        assert list(make(CLASSIC).preorder()) == [5, 3, 1, 4, 8, 7, 9]

    def test_inorder(self) -> None:
        assert list(make(CLASSIC).inorder()) == [1, 3, 4, 5, 7, 8, 9]

    def test_postorder(self) -> None:
        assert list(make(CLASSIC).postorder()) == [1, 4, 3, 7, 9, 8, 5]

    def test_levelorder(self) -> None:
        assert list(make(CLASSIC).levelorder()) == [5, 3, 8, 1, 4, 7, 9]

    def test_measures(self) -> None:
        tree = make(CLASSIC)
        assert (tree.height(), tree.leaves(), tree.root()) == (3, 4, 5)

    def test_the_root_is_always_the_first_value_inserted(self) -> None:
        assert make([2, 1, 3]).root() == 2
        assert make([1, 2, 3]).root() == 1
        assert make([3, 2, 1]).root() == 3

    def test_sorted_input_degenerates_into_a_chain(self) -> None:
        tree = make(range(1, 8))
        assert tree.height() == 7
        assert tree.leaves() == 1
        assert list(tree.preorder()) == list(range(1, 8))

    def test_greater_values_go_right_and_smaller_go_left(self) -> None:
        assert list(make([5, 3]).preorder()) == [5, 3]
        assert list(make([5, 3]).levelorder()) == [5, 3]
        tree = make([5, 8])
        assert list(tree.postorder()) == [8, 5]

    def test_the_tree_is_not_rebalanced(self) -> None:
        assert make([1, 2, 3]).height() == 3


class TestRemoveStructure:
    def test_leaf(self) -> None:
        tree = make(CLASSIC)
        tree.remove(1)
        assert list(tree.preorder()) == [5, 3, 4, 8, 7, 9]

    def test_node_with_only_a_left_child(self) -> None:
        tree = make([5, 3, 8, 1])
        tree.remove(3)
        assert list(tree.preorder()) == [5, 1, 8]

    def test_node_with_only_a_right_child(self) -> None:
        tree = make([5, 3, 8, 4])
        tree.remove(3)
        assert list(tree.preorder()) == [5, 4, 8]

    def test_two_children_successor_is_the_right_child(self) -> None:
        tree = make([5, 3, 8, 7, 9])
        tree.remove(8)
        assert list(tree.preorder()) == [5, 3, 9, 7]

    def test_two_children_successor_is_deeper(self) -> None:
        tree = make(CLASSIC)
        tree.remove(5)
        assert list(tree.preorder()) == [7, 3, 1, 4, 8, 9]

    def test_successor_with_a_right_child_keeps_it(self) -> None:
        tree = make([5, 3, 10, 7, 8])
        tree.remove(5)
        assert list(tree.preorder()) == [7, 3, 10, 8]

    def test_successor_two_levels_down_on_the_left_spine(self) -> None:
        tree = make([10, 5, 20, 15, 30, 12, 17, 11])
        tree.remove(10)
        assert list(tree.inorder()) == [5, 11, 12, 15, 17, 20, 30]
        assert list(tree.preorder()) == [11, 5, 20, 15, 12, 17, 30]

    def test_root_with_only_a_left_child(self) -> None:
        tree = make([5, 3, 1])
        tree.remove(5)
        assert tree.root() == 3
        assert list(tree.preorder()) == [3, 1]

    def test_root_with_only_a_right_child(self) -> None:
        tree = make([5, 8, 9])
        tree.remove(5)
        assert tree.root() == 8
        assert list(tree.preorder()) == [8, 9]

    def test_removing_the_last_node_leaves_no_root(self) -> None:
        tree = make([5])
        tree.remove(5)
        assert tree._root is None

    def test_removing_a_missing_value_between_nodes(self) -> None:
        tree = make(CLASSIC)
        tree.remove(6)
        assert list(tree.preorder()) == [5, 3, 1, 4, 8, 7, 9]

    def test_removed_value_can_be_inserted_in_a_new_place(self) -> None:
        tree = make(CLASSIC)
        tree.remove(8)
        tree.insert(8)
        assert list(tree.inorder()) == [1, 3, 4, 5, 7, 8, 9]


class TestInvariants:
    @pytest.mark.parametrize("seed", range(60))
    def test_order_and_size_hold_after_every_operation(self, seed: int) -> None:
        rng = random.Random(seed)
        tree: BSTree[int] = BSTree()
        for _ in range(rng.randrange(0, 150)):
            value = rng.randrange(40)
            if rng.random() < 0.6:
                tree.insert(value)
            else:
                tree.remove(value)
            check_invariants(tree)
