import random
from collections import deque

import pytest

from pydsa.exc import EmptyError, InvalidPathError, InvalidValueError, PydsaError
from pydsa.trees import BinaryTree


def build(entries: list[tuple[int, str]]) -> BinaryTree[int]:
    tree: BinaryTree[int] = BinaryTree()
    for value, path in entries:
        tree.insert(value, path)
    return tree


# Shape used by several tests:
#          5
#       3     8
#      1 4   7
SAMPLE = [(5, ""), (3, "L"), (8, "R"), (1, "LL"), (4, "LR"), (7, "RL")]


def reference_traversals(model: dict[str, int]) -> dict[str, list[int]]:
    """Compute every traversal recursively from a ``path -> value`` mapping."""

    def pre(path: str) -> list[int]:
        if path not in model:
            return []
        return [model[path], *pre(path + "L"), *pre(path + "R")]

    def ino(path: str) -> list[int]:
        if path not in model:
            return []
        return [*ino(path + "L"), model[path], *ino(path + "R")]

    def post(path: str) -> list[int]:
        if path not in model:
            return []
        return [*post(path + "L"), *post(path + "R"), model[path]]

    level: list[int] = []
    queue = deque([""] if "" in model else [])
    while queue:
        path = queue.popleft()
        level.append(model[path])
        queue.extend(p for p in (path + "L", path + "R") if p in model)
    return {"preorder": pre(""), "inorder": ino(""), "postorder": post(""), "levelorder": level}


class TestEmptyTree:
    def test_size_and_truthiness(self) -> None:
        tree: BinaryTree[int] = BinaryTree()
        assert len(tree) == 0
        assert not tree

    def test_measures_are_zero(self) -> None:
        tree: BinaryTree[int] = BinaryTree()
        assert tree.height() == 0
        assert tree.leaves() == 0

    def test_traversals_are_empty(self) -> None:
        tree: BinaryTree[int] = BinaryTree()
        assert list(tree.preorder()) == []
        assert list(tree.inorder()) == []
        assert list(tree.postorder()) == []
        assert list(tree.levelorder()) == []

    def test_root_raises_empty_error(self) -> None:
        with pytest.raises(EmptyError, match="BinaryTree"):
            BinaryTree().root()

    def test_clear_is_a_no_op(self) -> None:
        tree: BinaryTree[int] = BinaryTree()
        tree.clear()
        assert len(tree) == 0


class TestInsert:
    def test_first_value_becomes_the_root(self) -> None:
        tree = build([(5, "")])
        assert tree.root() == 5
        assert len(tree) == 1
        assert tree
        assert tree.height() == 1
        assert tree.leaves() == 1

    @pytest.mark.parametrize("path", ["RR", "LLL", "LLR", "LRL", "LRR", "RLL", "RLR"])
    def test_every_empty_position_next_to_the_sample_is_accepted(self, path: str) -> None:
        tree = build(SAMPLE)
        tree.insert(99, path)
        assert len(tree) == 7
        assert 99 in tree.preorder()

    def test_children_are_attached_on_the_requested_side(self) -> None:
        tree = build([(5, ""), (3, "L"), (8, "R")])
        assert list(tree.preorder()) == [5, 3, 8]
        tree = build([(5, ""), (8, "R")])
        assert list(tree.inorder()) == [5, 8]
        tree = build([(5, ""), (3, "L")])
        assert list(tree.inorder()) == [3, 5]

    def test_deep_path(self) -> None:
        tree = build([(1, ""), (2, "L"), (3, "LR"), (4, "LRL")])
        assert list(tree.preorder()) == [1, 2, 3, 4]
        assert tree.height() == 4

    def test_every_insert_increases_len_by_one(self) -> None:
        tree: BinaryTree[int] = BinaryTree()
        for count, (value, path) in enumerate(SAMPLE, start=1):
            tree.insert(value, path)
            assert len(tree) == count

    def test_none_and_falsy_values_are_ordinary_values(self) -> None:
        tree: BinaryTree[object] = BinaryTree()
        tree.insert(0, "")
        tree.insert(None, "L")
        tree.insert("", "R")
        assert list(tree.levelorder()) == [0, None, ""]
        assert len(tree) == 3

    def test_equal_values_may_repeat(self) -> None:
        tree = build([(7, ""), (7, "L"), (7, "R")])
        assert list(tree.inorder()) == [7, 7, 7]
        assert len(tree) == 3

    def test_siblings_can_be_added_in_any_order(self) -> None:
        a = build([(5, ""), (3, "L"), (8, "R")])
        b = build([(5, ""), (8, "R"), (3, "L")])
        assert list(a.preorder()) == list(b.preorder())


class TestInvalidInsert:
    """Every rejected insert raises InvalidPathError and leaves the tree untouched."""

    @staticmethod
    def snapshot(tree: BinaryTree[int]) -> tuple[int, list[int], list[int]]:
        return len(tree), list(tree.preorder()), list(tree.levelorder())

    def test_second_root_is_rejected(self) -> None:
        tree = build(SAMPLE)
        before = self.snapshot(tree)
        with pytest.raises(InvalidPathError, match="Root already exists"):
            tree.insert(99, "")
        assert self.snapshot(tree) == before
        assert tree.root() == 5

    @pytest.mark.parametrize(
        "path", ["X", "LX", "XL", "LXR", "l", "lr", "L R", "L ", " ", "0", "LRZ"]
    )
    def test_illegal_characters_are_rejected(self, path: str) -> None:
        tree = build(SAMPLE)
        before = self.snapshot(tree)
        with pytest.raises(InvalidPathError, match="may only contain"):
            tree.insert(99, path)
        assert self.snapshot(tree) == before

    def test_illegal_characters_are_rejected_on_an_empty_tree_too(self) -> None:
        tree: BinaryTree[int] = BinaryTree()
        with pytest.raises(InvalidPathError, match="may only contain"):
            tree.insert(1, "X")
        assert len(tree) == 0

    @pytest.mark.parametrize("path", ["L", "R", "LL", "RL"])
    def test_non_empty_path_on_an_empty_tree_is_rejected(self, path: str) -> None:
        tree: BinaryTree[int] = BinaryTree()
        with pytest.raises(InvalidPathError, match="empty tree"):
            tree.insert(1, path)
        assert len(tree) == 0

    @pytest.mark.parametrize("path", ["RRL", "RRR", "LLLL", "LRLR", "RLRR", "LLLR"])
    def test_missing_node_on_the_path_is_rejected(self, path: str) -> None:
        tree = build(SAMPLE)
        before = self.snapshot(tree)
        with pytest.raises(InvalidPathError, match="broken"):
            tree.insert(99, path)
        assert self.snapshot(tree) == before

    @pytest.mark.parametrize("path", ["L", "R", "LL", "LR", "RL"])
    def test_occupied_position_is_rejected(self, path: str) -> None:
        tree = build(SAMPLE)
        before = self.snapshot(tree)
        with pytest.raises(InvalidPathError, match="occupied"):
            tree.insert(99, path)
        assert self.snapshot(tree) == before

    def test_the_error_is_also_a_value_error_and_a_pydsa_error(self) -> None:
        tree = build([(1, "")])
        with pytest.raises(ValueError):
            tree.insert(2, "X")
        with pytest.raises(InvalidValueError):
            tree.insert(2, "X")
        with pytest.raises(PydsaError):
            tree.insert(2, "X")

    def test_tree_is_still_usable_after_an_error(self) -> None:
        tree = build([(1, "")])
        with pytest.raises(InvalidPathError):
            tree.insert(2, "LL")
        tree.insert(2, "L")
        tree.insert(3, "LL")
        assert list(tree.preorder()) == [1, 2, 3]
        assert len(tree) == 3


class TestTraversals:
    def test_preorder(self) -> None:
        assert list(build(SAMPLE).preorder()) == [5, 3, 1, 4, 8, 7]

    def test_inorder(self) -> None:
        assert list(build(SAMPLE).inorder()) == [1, 3, 4, 5, 7, 8]

    def test_postorder(self) -> None:
        assert list(build(SAMPLE).postorder()) == [1, 4, 3, 7, 8, 5]

    def test_levelorder(self) -> None:
        assert list(build(SAMPLE).levelorder()) == [5, 3, 8, 1, 4, 7]

    def test_single_node(self) -> None:
        tree = build([(9, "")])
        assert list(tree.preorder()) == list(tree.inorder()) == [9]
        assert list(tree.postorder()) == list(tree.levelorder()) == [9]

    def test_left_only_chain(self) -> None:
        tree = build([(1, ""), (2, "L"), (3, "LL")])
        assert list(tree.preorder()) == [1, 2, 3]
        assert list(tree.inorder()) == [3, 2, 1]
        assert list(tree.postorder()) == [3, 2, 1]
        assert list(tree.levelorder()) == [1, 2, 3]

    def test_right_only_chain(self) -> None:
        tree = build([(1, ""), (2, "R"), (3, "RR")])
        assert list(tree.preorder()) == [1, 2, 3]
        assert list(tree.inorder()) == [1, 2, 3]
        assert list(tree.postorder()) == [3, 2, 1]
        assert list(tree.levelorder()) == [1, 2, 3]

    def test_traversals_are_repeatable(self) -> None:
        tree = build(SAMPLE)
        assert list(tree.inorder()) == list(tree.inorder())

    def test_traversals_do_not_modify_the_tree(self) -> None:
        tree = build(SAMPLE)
        for traversal in (tree.preorder, tree.inorder, tree.postorder, tree.levelorder):
            list(traversal())
        assert len(tree) == 6
        assert list(tree.preorder()) == [5, 3, 1, 4, 8, 7]

    def test_traversals_are_lazy_iterators(self) -> None:
        tree = build(SAMPLE)
        for traversal in (tree.preorder, tree.inorder, tree.postorder, tree.levelorder):
            iterator = traversal()
            assert iter(iterator) is iterator
        assert next(tree.preorder()) == 5
        assert next(tree.inorder()) == 1
        assert next(tree.postorder()) == 1
        assert next(tree.levelorder()) == 5

    def test_deep_chain_does_not_hit_the_recursion_limit(self) -> None:
        tree = build([(0, "")])
        for depth in range(1, 1500):
            tree.insert(depth, "L" * depth)
        assert tree.height() == 1500
        assert list(tree.preorder()) == list(range(1500))
        assert list(tree.inorder()) == list(range(1499, -1, -1))
        assert list(tree.postorder()) == list(range(1499, -1, -1))
        assert list(tree.levelorder()) == list(range(1500))


class TestMeasures:
    def test_height_counts_nodes_on_the_longest_path(self) -> None:
        assert build(SAMPLE).height() == 3
        assert build([(1, ""), (2, "R"), (3, "RR"), (4, "RRR")]).height() == 4

    def test_height_follows_the_deepest_branch_not_the_first(self) -> None:
        tree = build([(1, ""), (2, "L"), (3, "R"), (4, "RL"), (5, "RLR")])
        assert tree.height() == 4

    def test_leaves(self) -> None:
        assert build(SAMPLE).leaves() == 3
        assert build([(1, "")]).leaves() == 1
        assert build([(1, ""), (2, "L")]).leaves() == 1
        assert build([(1, ""), (2, "L"), (3, "R")]).leaves() == 2

    def test_root_is_the_first_value_inserted_at_the_empty_path(self) -> None:
        assert build(SAMPLE).root() == 5


class TestClear:
    def test_clear_empties_the_tree(self) -> None:
        tree = build(SAMPLE)
        tree.clear()
        assert len(tree) == 0
        assert not tree
        assert tree.height() == 0
        assert tree.leaves() == 0
        assert list(tree.levelorder()) == []
        with pytest.raises(EmptyError):
            tree.root()

    def test_tree_is_reusable_after_clear(self) -> None:
        tree = build(SAMPLE)
        tree.clear()
        tree.insert(1, "")
        tree.insert(2, "R")
        assert list(tree.preorder()) == [1, 2]
        assert len(tree) == 2

    def test_old_paths_are_gone_after_clear(self) -> None:
        tree = build(SAMPLE)
        tree.clear()
        with pytest.raises(InvalidPathError):
            tree.insert(1, "L")


class TestAgainstARecursiveModel:
    @pytest.mark.parametrize("seed", range(40))
    def test_random_trees_with_random_rejected_inserts(self, seed: int) -> None:
        rng = random.Random(seed)
        tree: BinaryTree[int] = BinaryTree()
        model: dict[str, int] = {}
        for step in range(rng.randrange(0, 60)):
            free = [""] if not model else [p + c for p in model for c in "LR" if p + c not in model]
            path = rng.choice(free)
            tree.insert(step, path)
            model[path] = step
            if rng.random() < 0.3:
                before = list(tree.preorder())
                bad = rng.choice(["X", "LL" * 40, "", "LRX", *model])
                if (
                    bad in model
                    or bad.strip("LR")
                    or any(bad[:i] not in model for i in range(len(bad)))
                ):
                    with pytest.raises(InvalidPathError):
                        tree.insert(-1, bad)
                    assert list(tree.preorder()) == before
        expected = reference_traversals(model)
        assert len(tree) == len(model)
        assert list(tree.preorder()) == expected["preorder"]
        assert list(tree.inorder()) == expected["inorder"]
        assert list(tree.postorder()) == expected["postorder"]
        assert list(tree.levelorder()) == expected["levelorder"]
        assert tree.height() == max((len(p) + 1 for p in model), default=0)
        assert tree.leaves() == sum(
            1 for p in model if p + "L" not in model and p + "R" not in model
        )
