import pytest

from pydsa import EmptyError, BinaryTree


class TestBasics:
    def test_new_tree_is_empty(self) -> None:
        tree = BinaryTree[int]()
        assert tree.is_empty()
        assert len(tree) == 0
        assert not tree

    def test_root_raises_when_empty(self) -> None:
        tree = BinaryTree[int]()
        with pytest.raises(EmptyError):
            tree.root()

    def test_insert_at_root(self) -> None:
        tree = BinaryTree[int]()
        tree.insert(5, "")
        assert tree.root() == 5
        assert len(tree) == 1
        assert bool(tree)


class TestInsertPaths:
    def test_insert_builds_expected_shape(self) -> None:
        tree = BinaryTree[int]()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        assert list(tree.preorder()) == [5, 3, 1, 8]

    def test_broken_path_raises(self) -> None:
        tree = BinaryTree[int]()
        tree.insert(5, "")
        with pytest.raises(ValueError):
            tree.insert(1, "LL")  # "L" doesn't exist yet

    def test_insert_preserves_existing_subtree(self) -> None:
        tree = BinaryTree[int]()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(1, "LL")
        tree.insert(99, "L")  # overwrite at "L" — old subtree should hang off it
        assert list(tree.preorder()) == [5, 99, 3, 1]

    def test_empty_path_on_non_empty_tree_replaces_root(self) -> None:
        """Regression test: insert(value, "") used to raise IndexError
        when the tree was already non-empty, because path[-1] on an
        empty string is invalid. Empty path should always target the
        root and preserve its existing children.
        """
        tree = BinaryTree[int]()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(99, "")  # replace root — should not crash
        assert tree.root() == 99
        assert list(tree.preorder()) == [99, 3, 8]
        assert len(tree) == 4

    def test_non_empty_path_on_empty_tree_raises(self) -> None:
        """Regression test: an empty tree used to silently ignore a
        non-trivial path and insert at the root anyway, instead of
        raising as the docstring promises.
        """
        tree = BinaryTree[int]()
        with pytest.raises(ValueError):
            tree.insert(1, "LLR")


class TestTraversals:
    @pytest.fixture
    def tree(self) -> BinaryTree[int]:
        tree = BinaryTree[int]()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        return tree

    def test_preorder(self, tree: BinaryTree[int]) -> None:
        assert list(tree.preorder()) == [5, 3, 1, 8]

    def test_inorder(self, tree: BinaryTree[int]) -> None:
        assert list(tree.inorder()) == [1, 3, 5, 8]

    def test_postorder(self, tree: BinaryTree[int]) -> None:
        assert list(tree.postorder()) == [1, 3, 8, 5]

    def test_levelorder(self, tree: BinaryTree[int]) -> None:
        assert list(tree.levelorder()) == [5, 3, 8, 1]

    def test_traversals_on_empty_tree_yield_nothing(self) -> None:
        tree = BinaryTree[int]()
        assert list(tree.preorder()) == []
        assert list(tree.inorder()) == []
        assert list(tree.postorder()) == []
        assert list(tree.levelorder()) == []


class TestHeightAndLeaves:
    def test_height_single_node(self) -> None:
        tree = BinaryTree[int]()
        tree.insert(5, "")
        assert tree.height() == 1

    def test_height_empty_tree(self) -> None:
        assert BinaryTree[int]().height() == 0

    def test_height_multi_level(self) -> None:
        tree = BinaryTree[int]()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        assert tree.height() == 3

    def test_leaves_count(self) -> None:
        tree = BinaryTree[int]()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        assert tree.leaves() == 2  # nodes 1 and 8

    def test_leaves_empty_tree(self) -> None:
        assert BinaryTree[int]().leaves() == 0


class TestClear:
    def test_clear(self) -> None:
        tree = BinaryTree[int]()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.clear()
        assert tree.is_empty()
        assert len(tree) == 0