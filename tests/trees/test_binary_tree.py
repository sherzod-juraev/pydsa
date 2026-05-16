import pytest
from pydsa import BinaryTree
from pydsa.exc import Empty


class TestBinaryTreeInit:
    """__init__"""

    def test_empty_tree_has_zero_nodes(self):
        tree = BinaryTree()
        assert len(tree) == 0

    def test_empty_tree_is_falsy(self):
        tree = BinaryTree()
        assert not tree

    def test_empty_tree_is_empty(self):
        tree = BinaryTree()
        assert tree.is_empty()


class TestBinaryTreeInsert:
    """insert"""

    def test_insert_root(self):
        tree = BinaryTree()
        tree.insert(5, "")
        assert len(tree) == 1
        assert tree.root() == 5

    def test_insert_left_child(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        assert len(tree) == 2
        assert tree.root() == 5

    def test_insert_right_child(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(8, "R")
        assert len(tree) == 2
        assert tree.root() == 5

    def test_insert_multiple_levels(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        tree.insert(4, "LR")
        tree.insert(7, "RL")
        tree.insert(9, "RR")
        assert len(tree) == 7

    def test_insert_replaces_existing_node(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(99, "L")
        assert len(tree) == 3

    def test_insert_preserves_subtree_on_replace(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(1, "LL")
        tree.insert(99, "L")
        assert len(tree) == 4

    def test_insert_broken_path_raises(self):
        tree = BinaryTree()
        tree.insert(5, "")
        with pytest.raises(ValueError, match="Path is broken"):
            tree.insert(10, "LL")

    def test_insert_broken_path_deep_raises(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        with pytest.raises(ValueError, match="Path is broken"):
            tree.insert(10, "LRR")

    def test_insert_invalid_path_char_does_nothing(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "X")  # invalid char, silently ignored
        assert len(tree) == 2


class TestBinaryTreeRoot:
    """root"""

    def test_root_returns_value(self):
        tree = BinaryTree()
        tree.insert(42, "")
        assert tree.root() == 42

    def test_root_on_empty_raises(self):
        tree = BinaryTree()
        with pytest.raises(Empty):
            tree.root()


class TestBinaryTreePreorder:
    """preorder"""

    def test_preorder_single_node(self):
        tree = BinaryTree()
        tree.insert(5, "")
        assert list(tree.preorder()) == [5]

    def test_preorder_full_tree(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        tree.insert(4, "LR")
        tree.insert(7, "RL")
        tree.insert(9, "RR")
        assert list(tree.preorder()) == [5, 3, 1, 4, 8, 7, 9]

    def test_preorder_left_skewed(self):
        tree = BinaryTree()
        tree.insert(1, "")
        tree.insert(2, "L")
        tree.insert(3, "LL")
        assert list(tree.preorder()) == [1, 2, 3]

    def test_preorder_right_skewed(self):
        tree = BinaryTree()
        tree.insert(1, "")
        tree.insert(2, "R")
        tree.insert(3, "RR")
        assert list(tree.preorder()) == [1, 2, 3]

    def test_preorder_empty_tree(self):
        tree = BinaryTree()
        assert list(tree.preorder()) == []


class TestBinaryTreeInorder:
    """inorder"""

    def test_inorder_single_node(self):
        tree = BinaryTree()
        tree.insert(5, "")
        assert list(tree.inorder()) == [5]

    def test_inorder_full_tree(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        tree.insert(4, "LR")
        tree.insert(7, "RL")
        tree.insert(9, "RR")
        assert list(tree.inorder()) == [1, 3, 4, 5, 7, 8, 9]

    def test_inorder_left_skewed(self):
        tree = BinaryTree()
        tree.insert(1, "")
        tree.insert(2, "L")
        tree.insert(3, "LL")
        assert list(tree.inorder()) == [3, 2, 1]

    def test_inorder_right_skewed(self):
        tree = BinaryTree()
        tree.insert(1, "")
        tree.insert(2, "R")
        tree.insert(3, "RR")
        assert list(tree.inorder()) == [1, 2, 3]

    def test_inorder_empty_tree(self):
        tree = BinaryTree()
        assert list(tree.inorder()) == []


class TestBinaryTreePostorder:
    """postorder"""

    def test_postorder_single_node(self):
        tree = BinaryTree()
        tree.insert(5, "")
        assert list(tree.postorder()) == [5]

    def test_postorder_full_tree(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        tree.insert(4, "LR")
        tree.insert(7, "RL")
        tree.insert(9, "RR")
        assert list(tree.postorder()) == [1, 4, 3, 7, 9, 8, 5]

    def test_postorder_left_skewed(self):
        tree = BinaryTree()
        tree.insert(1, "")
        tree.insert(2, "L")
        tree.insert(3, "LL")
        assert list(tree.postorder()) == [3, 2, 1]

    def test_postorder_right_skewed(self):
        tree = BinaryTree()
        tree.insert(1, "")
        tree.insert(2, "R")
        tree.insert(3, "RR")
        assert list(tree.postorder()) == [3, 2, 1]

    def test_postorder_empty_tree(self):
        tree = BinaryTree()
        assert list(tree.postorder()) == []


class TestBinaryTreeLevelorder:
    """levelorder"""

    def test_levelorder_single_node(self):
        tree = BinaryTree()
        tree.insert(5, "")
        assert list(tree.levelorder()) == [5]

    def test_levelorder_full_tree(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        tree.insert(4, "LR")
        tree.insert(7, "RL")
        tree.insert(9, "RR")
        assert list(tree.levelorder()) == [5, 3, 8, 1, 4, 7, 9]

    def test_levelorder_left_skewed(self):
        tree = BinaryTree()
        tree.insert(1, "")
        tree.insert(2, "L")
        tree.insert(3, "LL")
        assert list(tree.levelorder()) == [1, 2, 3]

    def test_levelorder_empty_tree(self):
        tree = BinaryTree()
        assert list(tree.levelorder()) == []


class TestBinaryTreeHeight:
    """height"""

    def test_height_empty_tree(self):
        tree = BinaryTree()
        assert tree.height() == 0

    def test_height_single_node(self):
        tree = BinaryTree()
        tree.insert(5, "")
        assert tree.height() == 1

    def test_height_full_tree(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        assert tree.height() == 3

    def test_height_skewed_tree(self):
        tree = BinaryTree()
        tree.insert(1, "")
        tree.insert(2, "L")
        tree.insert(3, "LL")
        tree.insert(4, "LLL")
        assert tree.height() == 4

    def test_height_complete_tree(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        tree.insert(4, "LR")
        tree.insert(7, "RL")
        tree.insert(9, "RR")
        assert tree.height() == 3


class TestBinaryTreeLeaves:
    """leaves"""

    def test_leaves_empty_tree(self):
        tree = BinaryTree()
        assert tree.leaves() == 0

    def test_leaves_single_node(self):
        tree = BinaryTree()
        tree.insert(5, "")
        assert tree.leaves() == 1

    def test_leaves_full_tree(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.insert(1, "LL")
        tree.insert(4, "LR")
        tree.insert(7, "RL")
        tree.insert(9, "RR")
        assert tree.leaves() == 4  # 1, 4, 7, 9

    def test_leaves_skewed_tree(self):
        tree = BinaryTree()
        tree.insert(1, "")
        tree.insert(2, "L")
        tree.insert(3, "LL")
        assert tree.leaves() == 1  # faqat 3

    def test_leaves_two_nodes(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        assert tree.leaves() == 1  # faqat 3


class TestBinaryTreeClear:
    """clear"""

    def test_clear_non_empty_tree(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        tree.clear()
        assert tree.is_empty()
        assert len(tree) == 0

    def test_clear_empty_tree(self):
        tree = BinaryTree()
        tree.clear()
        assert tree.is_empty()


class TestBinaryTreeBool:
    """__bool__"""

    def test_non_empty_is_truthy(self):
        tree = BinaryTree()
        tree.insert(1, "")
        assert bool(tree)

    def test_empty_is_falsy(self):
        tree = BinaryTree()
        assert not tree


class TestBinaryTreeLen:
    """__len__"""

    def test_len_after_inserts(self):
        tree = BinaryTree()
        assert len(tree) == 0
        tree.insert(5, "")
        assert len(tree) == 1
        tree.insert(3, "L")
        assert len(tree) == 2
        tree.insert(8, "R")
        assert len(tree) == 3

    def test_len_after_clear(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.clear()
        assert len(tree) == 0


class TestBinaryTreeMultipleTraversalCalls:
    """Multiple traversal calls on same tree"""

    def test_multiple_preorder_calls(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        assert list(tree.preorder()) == [5, 3, 8]
        assert list(tree.preorder()) == [5, 3, 8]

    def test_mixed_traversals(self):
        tree = BinaryTree()
        tree.insert(5, "")
        tree.insert(3, "L")
        tree.insert(8, "R")
        pre = list(tree.preorder())
        ino = list(tree.inorder())
        post = list(tree.postorder())
        level = list(tree.levelorder())
        assert pre == [5, 3, 8]
        assert ino == [3, 5, 8]
        assert post == [3, 8, 5]
        assert level == [5, 3, 8]


class TestBinaryTreeLargeData:
    """Large tree"""

    def test_deep_left_skewed(self):
        tree = BinaryTree()
        n = 500
        path = ""
        for i in range(n):
            tree.insert(i, path)
            path += "L"
        assert len(tree) == n
        assert tree.height() == n
        assert tree.leaves() == 1

    def test_complete_tree_traversals(self):
        tree = BinaryTree()
        tree.insert(1, "")
        tree.insert(2, "L")
        tree.insert(3, "R")
        tree.insert(4, "LL")
        tree.insert(5, "LR")
        tree.insert(6, "RL")
        tree.insert(7, "RR")
        assert list(tree.levelorder()) == [1, 2, 3, 4, 5, 6, 7]
        assert list(tree.preorder()) == [1, 2, 4, 5, 3, 6, 7]
        assert list(tree.inorder()) == [4, 2, 5, 1, 6, 3, 7]
        assert list(tree.postorder()) == [4, 5, 2, 6, 7, 3, 1]