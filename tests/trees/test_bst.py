import pytest
from pydsa import BSTree
from pydsa.exc import Empty


class TestBSTreeInit:
    """__init__"""

    def test_empty_tree_has_zero_nodes(self):
        bst = BSTree()
        assert len(bst) == 0

    def test_empty_tree_is_falsy(self):
        bst = BSTree()
        assert not bst

    def test_empty_tree_is_empty(self):
        bst = BSTree()
        assert bst.is_empty()


class TestBSTreeInsert:
    """insert"""

    def test_insert_root(self):
        bst = BSTree()
        bst.insert(10)
        assert len(bst) == 1
        assert bst.root() == 10

    def test_insert_multiple(self):
        bst = BSTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        assert len(bst) == 7

    def test_insert_duplicate_ignored(self):
        bst = BSTree()
        bst.insert(5)
        bst.insert(5)
        bst.insert(5)
        assert len(bst) == 1

    def test_insert_duplicate_does_not_change_structure(self):
        bst = BSTree()
        bst.insert(5)
        bst.insert(3)
        bst.insert(5)
        bst.insert(3)
        assert len(bst) == 2
        assert bst.root() == 5

    def test_insert_left_and_right(self):
        bst = BSTree()
        bst.insert(10)
        bst.insert(5)
        bst.insert(15)
        assert len(bst) == 3
        assert list(bst.inorder()) == [5, 10, 15]


class TestBSTreeSearch:
    """searching"""

    def test_search_existing(self):
        bst = BSTree()
        for v in [5, 3, 8, 1, 4]:
            bst.insert(v)
        assert bst.search(4) is True
        assert bst.search(8) is True
        assert bst.search(5) is True

    def test_search_non_existing(self):
        bst = BSTree()
        bst.insert(5)
        assert bst.search(99) is False

    def test_search_empty_tree(self):
        bst = BSTree()
        assert bst.search(10) is False


class TestBSTreeContains:
    """__contains__"""

    def test_contains_existing(self):
        bst = BSTree()
        bst.insert(42)
        assert 42 in bst

    def test_contains_non_existing(self):
        bst = BSTree()
        bst.insert(42)
        assert 99 not in bst

    def test_contains_empty(self):
        bst = BSTree()
        assert 10 not in bst


class TestBSTreeRoot:
    """root"""

    def test_root_returns_value(self):
        bst = BSTree()
        bst.insert(42)
        assert bst.root() == 42

    def test_root_on_empty_raises(self):
        bst = BSTree()
        with pytest.raises(Empty):
            bst.root()


class TestBSTreeMinMax:
    """min_value / max_value"""

    def test_min_value(self):
        bst = BSTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        assert bst.min_value() == 1

    def test_max_value(self):
        bst = BSTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        assert bst.max_value() == 9

    def test_min_value_single_node(self):
        bst = BSTree()
        bst.insert(42)
        assert bst.min_value() == 42
        assert bst.max_value() == 42

    def test_min_value_on_empty_raises(self):
        bst = BSTree()
        with pytest.raises(Empty):
            bst.min_value()

    def test_max_value_on_empty_raises(self):
        bst = BSTree()
        with pytest.raises(Empty):
            bst.max_value()

    def test_min_value_skewed_right(self):
        bst = BSTree()
        for v in [1, 2, 3, 4, 5]:
            bst.insert(v)
        assert bst.min_value() == 1
        assert bst.max_value() == 5

    def test_min_value_skewed_left(self):
        bst = BSTree()
        for v in [5, 4, 3, 2, 1]:
            bst.insert(v)
        assert bst.min_value() == 1
        assert bst.max_value() == 5


class TestBSTreeRemove:
    """remove"""

    def test_remove_leaf(self):
        bst = BSTree()
        for v in [5, 3, 8]:
            bst.insert(v)
        bst.remove(3)
        assert len(bst) == 2
        assert 3 not in bst
        assert list(bst.inorder()) == [5, 8]

    def test_remove_node_with_one_child(self):
        bst = BSTree()
        for v in [5, 3, 8, 1]:
            bst.insert(v)
        bst.remove(3)
        assert len(bst) == 3
        assert 3 not in bst
        assert 1 in bst
        assert list(bst.inorder()) == [1, 5, 8]

    def test_remove_node_with_two_children(self):
        bst = BSTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        bst.remove(5)
        assert len(bst) == 6
        assert 5 not in bst
        assert list(bst.inorder()) == [1, 3, 4, 7, 8, 9]

    def test_remove_root_single_node(self):
        bst = BSTree()
        bst.insert(10)
        bst.remove(10)
        assert bst.is_empty()
        assert len(bst) == 0

    def test_remove_root_with_two_children(self):
        bst = BSTree()
        for v in [10, 5, 15]:
            bst.insert(v)
        bst.remove(10)
        assert len(bst) == 2
        assert 10 not in bst
        assert list(bst.inorder()) == [5, 15]

    def test_remove_non_existing(self):
        bst = BSTree()
        for v in [5, 3, 8]:
            bst.insert(v)
        bst.remove(99)
        assert len(bst) == 3

    def test_remove_from_empty(self):
        bst = BSTree()
        bst.remove(10)
        assert bst.is_empty()

    def test_remove_root_leaf(self):
        bst = BSTree()
        bst.insert(10)
        bst.remove(10)
        assert bst.is_empty()
        bst.insert(20)
        assert bst.root() == 20

    def test_remove_right_child_leaf(self):
        bst = BSTree()
        for v in [10, 5, 15]:
            bst.insert(v)
        bst.remove(15)
        assert list(bst.inorder()) == [5, 10]

    def test_remove_left_child_with_left_subtree(self):
        bst = BSTree()
        for v in [10, 5, 3]:
            bst.insert(v)
        bst.remove(5)
        assert list(bst.inorder()) == [3, 10]


class TestBSTreeInorder:
    """inorder — sorted output"""

    def test_inorder_sorted(self):
        bst = BSTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        assert list(bst.inorder()) == [1, 3, 4, 5, 7, 8, 9]

    def test_inorder_skewed_right(self):
        bst = BSTree()
        for v in [1, 2, 3, 4, 5]:
            bst.insert(v)
        assert list(bst.inorder()) == [1, 2, 3, 4, 5]

    def test_inorder_skewed_left(self):
        bst = BSTree()
        for v in [5, 4, 3, 2, 1]:
            bst.insert(v)
        assert list(bst.inorder()) == [1, 2, 3, 4, 5]

    def test_inorder_empty(self):
        bst = BSTree()
        assert list(bst.inorder()) == []


class TestBSTreeTraversals:
    """preorder / postorder / levelorder"""

    def test_preorder(self):
        bst = BSTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        assert list(bst.preorder()) == [5, 3, 1, 4, 8, 7, 9]

    def test_postorder(self):
        bst = BSTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        assert list(bst.postorder()) == [1, 4, 3, 7, 9, 8, 5]

    def test_levelorder(self):
        bst = BSTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        assert list(bst.levelorder()) == [5, 3, 8, 1, 4, 7, 9]

    def test_all_traversals_empty(self):
        bst = BSTree()
        assert list(bst.preorder()) == []
        assert list(bst.inorder()) == []
        assert list(bst.postorder()) == []
        assert list(bst.levelorder()) == []


class TestBSTreeHeight:
    """height"""

    def test_height_empty(self):
        bst = BSTree()
        assert bst.height() == 0

    def test_height_single_node(self):
        bst = BSTree()
        bst.insert(5)
        assert bst.height() == 1

    def test_height_balanced(self):
        bst = BSTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.insert(v)
        assert bst.height() == 3

    def test_height_degenerate_right(self):
        bst = BSTree()
        for v in [1, 2, 3, 4, 5]:
            bst.insert(v)
        assert bst.height() == 5

    def test_height_degenerate_left(self):
        bst = BSTree()
        for v in [5, 4, 3, 2, 1]:
            bst.insert(v)
        assert bst.height() == 5


class TestBSTreeClear:
    """clear"""

    def test_clear_non_empty(self):
        bst = BSTree()
        for v in [5, 3, 8]:
            bst.insert(v)
        bst.clear()
        assert bst.is_empty()
        assert len(bst) == 0

    def test_clear_empty(self):
        bst = BSTree()
        bst.clear()
        assert bst.is_empty()

    def test_insert_after_clear(self):
        bst = BSTree()
        bst.insert(5)
        bst.clear()
        bst.insert(10)
        assert bst.root() == 10
        assert len(bst) == 1


class TestBSTreeLen:
    """__len__"""

    def test_len_increases_on_insert(self):
        bst = BSTree()
        bst.insert(5)
        assert len(bst) == 1
        bst.insert(3)
        assert len(bst) == 2

    def test_len_decreases_on_remove(self):
        bst = BSTree()
        bst.insert(5)
        bst.insert(3)
        bst.remove(3)
        assert len(bst) == 1

    def test_len_stays_on_duplicate(self):
        bst = BSTree()
        bst.insert(5)
        bst.insert(5)
        assert len(bst) == 1

    def test_len_stays_on_failed_remove(self):
        bst = BSTree()
        bst.insert(5)
        bst.remove(99)
        assert len(bst) == 1


class TestBSTreeBool:
    """__bool__"""

    def test_non_empty_is_truthy(self):
        bst = BSTree()
        bst.insert(1)
        assert bool(bst)

    def test_empty_is_falsy(self):
        bst = BSTree()
        assert not bst


class TestBSTreeLargeData:
    """Large data"""

    def test_many_inserts(self):
        bst = BSTree()
        n = 500
        for i in range(n):
            bst.insert(i)
        assert len(bst) == n
        assert bst.min_value() == 0
        assert bst.max_value() == n - 1

    def test_many_inserts_and_search(self):
        bst = BSTree()
        for i in range(0, 500, 2):
            bst.insert(i)
        for i in range(0, 500, 2):
            assert i in bst
        for i in range(1, 500, 2):
            assert i not in bst

    def test_degenerate_height(self):
        bst = BSTree()
        n = 100
        for i in range(n):
            bst.insert(i)
        assert bst.height() == n