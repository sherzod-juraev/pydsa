import random

import pytest

from pydsa.trees import AVLTree
from pydsa.trees.avl import _AVLNode


def make(values) -> AVLTree[int]:
    tree: AVLTree[int] = AVLTree()
    for value in values:
        tree.insert(value)
    return tree


def check_invariants(tree: AVLTree[int]) -> None:
    """Recompute every height and balance from the structure and compare."""
    count = 0

    def walk(node: _AVLNode[int] | None, low: int | None, high: int | None) -> int:
        nonlocal count
        if node is None:
            return 0
        count += 1
        assert low is None or node.value > low
        assert high is None or node.value < high
        left = walk(node.left, low, node.value)
        right = walk(node.right, node.value, high)
        assert abs(left - right) <= 1, f"unbalanced at {node.value}"
        assert node.height == 1 + max(left, right), f"stale height at {node.value}"
        return node.height

    assert tree.height() == walk(tree._root, None, None)
    assert count == len(tree)


class TestRotationsOnInsert:
    def test_ll_case(self) -> None:
        tree = make([3, 2, 1])
        assert list(tree.levelorder()) == [2, 1, 3]
        assert tree.height() == 2

    def test_rr_case(self) -> None:
        tree = make([1, 2, 3])
        assert list(tree.levelorder()) == [2, 1, 3]
        assert tree.height() == 2

    def test_lr_case(self) -> None:
        tree = make([3, 1, 2])
        assert list(tree.levelorder()) == [2, 1, 3]
        assert tree.height() == 2

    def test_rl_case(self) -> None:
        tree = make([1, 3, 2])
        assert list(tree.levelorder()) == [2, 1, 3]
        assert tree.height() == 2

    def test_the_root_changes_after_a_rotation(self) -> None:
        assert make([1, 2, 3]).root() == 2

    def test_ascending_inserts_stay_logarithmic(self) -> None:
        tree = make(range(1, 1001))
        assert tree.height() <= 14
        check_invariants(tree)

    def test_perfect_tree_from_sorted_input(self) -> None:
        tree = make(range(1, 1024))
        assert tree.height() == 10
        assert tree.root() == 512
        assert tree.leaves() == 512
        check_invariants(tree)

    def test_descending_inserts_stay_logarithmic(self) -> None:
        tree = make(range(1000, 0, -1))
        assert tree.height() <= 14
        check_invariants(tree)

    def test_rotation_in_the_middle_of_the_tree_is_linked_back(self) -> None:
        tree = make([50, 30, 70, 20, 40, 60, 80, 10, 5])
        check_invariants(tree)
        assert list(tree.inorder()) == [5, 10, 20, 30, 40, 50, 60, 70, 80]
        assert tree.root() == 50

    def test_sequences_that_trigger_double_rotations_below_the_root(self) -> None:
        tree = make([50, 25, 75, 10, 30, 60, 90, 27])
        check_invariants(tree)
        tree.insert(28)
        check_invariants(tree)
        assert 28 in tree


class TestRotationsOnRemove:
    def test_single_left_rotation_when_the_heavy_child_is_balanced(self) -> None:
        tree = make([2, 1, 4, 3, 5])
        tree.remove(1)
        assert list(tree.levelorder()) == [4, 2, 5, 3]
        check_invariants(tree)

    def test_single_right_rotation_when_the_heavy_child_is_balanced(self) -> None:
        tree = make([4, 5, 2, 3, 1])
        tree.remove(5)
        assert list(tree.levelorder()) == [2, 1, 4, 3]
        check_invariants(tree)

    def test_lr_rotation(self) -> None:
        tree = make([10, 5, 15, 7])
        tree.remove(15)
        assert list(tree.levelorder()) == [7, 5, 10]
        check_invariants(tree)

    def test_rl_rotation(self) -> None:
        tree = make([10, 15, 5, 12])
        tree.remove(5)
        assert list(tree.levelorder()) == [12, 10, 15]
        check_invariants(tree)

    def test_removal_can_rotate_more_than_once(self) -> None:
        tree = make(range(1, 32))
        for value in range(1, 16):
            tree.remove(value)
            check_invariants(tree)
        assert list(tree.inorder()) == list(range(16, 32))

    def test_removing_a_two_child_node_keeps_the_invariants(self) -> None:
        tree = make([20, 10, 30, 5, 15, 25, 35, 12, 17])
        tree.remove(10)
        check_invariants(tree)
        tree.remove(20)
        check_invariants(tree)

    def test_removing_the_root_repeatedly(self) -> None:
        tree = make(range(1, 64))
        while tree:
            tree.remove(tree.root())
            check_invariants(tree)

    def test_removing_the_last_node_leaves_no_root(self) -> None:
        tree = make([1])
        tree.remove(1)
        assert tree._root is None
        assert tree.height() == 0


class TestHeight:
    def test_height_of_small_trees(self) -> None:
        assert make([]).height() == 0
        assert make([1]).height() == 1
        assert make([1, 2]).height() == 2
        assert make([10, 20, 30]).height() == 2

    def test_height_matches_the_structure_not_the_node_count(self) -> None:
        tree = make(range(100))
        assert tree.height() == 7
        assert len(tree) == 100

    def test_height_is_read_from_the_root_without_traversing(self, monkeypatch) -> None:
        tree = make(range(50))

        def fail(self):
            raise AssertionError("height must not traverse the tree")

        monkeypatch.setattr(AVLTree, "levelorder", fail)
        monkeypatch.setattr(AVLTree, "inorder", fail)
        assert tree.height() == 6

    def test_duplicate_insert_does_not_change_the_height(self) -> None:
        tree = make([1, 2, 3, 4, 5])
        height = tree.height()
        for value in (1, 3, 5):
            tree.insert(value)
        assert tree.height() == height
        check_invariants(tree)

    def test_height_after_clear(self) -> None:
        tree = make(range(10))
        tree.clear()
        assert tree.height() == 0
        tree.insert(1)
        assert tree.height() == 1


class TestInvariants:
    @pytest.mark.parametrize("seed", range(80))
    @pytest.mark.parametrize("key_range", [12, 200])
    def test_balance_heights_order_and_size_after_every_operation(
        self, seed: int, key_range: int
    ) -> None:
        rng = random.Random(seed)
        tree: AVLTree[int] = AVLTree()
        for _ in range(rng.randrange(0, 150)):
            value = rng.randrange(key_range)
            if rng.random() < 0.6:
                tree.insert(value)
            else:
                tree.remove(value)
            check_invariants(tree)

    def test_height_bound_for_random_inserts(self) -> None:
        rng = random.Random(1)
        tree = make(rng.sample(range(100_000), 5000))
        assert tree.height() <= 1.45 * 13
        check_invariants(tree)
