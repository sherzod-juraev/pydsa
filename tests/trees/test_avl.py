import pytest
from pydsa.trees.avl.avl_tree import AVLTree
from pydsa.exc import Empty


class TestAVLTreeInit:
    """__init__"""

    def test_empty_tree_has_zero_nodes(self):
        avl = AVLTree()
        assert len(avl) == 0

    def test_empty_tree_is_falsy(self):
        avl = AVLTree()
        assert not avl

    def test_empty_tree_is_empty(self):
        avl = AVLTree()
        assert avl.is_empty()


class TestAVLTreeInsert:
    """insert"""

    def test_insert_root(self):
        avl = AVLTree()
        avl.insert(10)
        assert len(avl) == 1
        assert avl.root() == 10

    def test_insert_duplicate_ignored(self):
        avl = AVLTree()
        avl.insert(5)
        avl.insert(5)
        avl.insert(5)
        assert len(avl) == 1

    def test_insert_builds_balanced_tree(self):
        avl = AVLTree()
        for v in [1, 2, 3, 4, 5, 6, 7]:
            avl.insert(v)
        assert len(avl) == 7
        # Balanced: height ≈ log2(7) + 1 = 3
        assert avl.height() <= 3

    def test_insert_right_skewed_becomes_balanced(self):
        avl = AVLTree()
        for v in [10, 20, 30, 40, 50]:
            avl.insert(v)
        # Without AVL: height = 5. With AVL: height ≤ 3
        assert avl.height() <= 3

    def test_insert_left_skewed_becomes_balanced(self):
        avl = AVLTree()
        for v in [50, 40, 30, 20, 10]:
            avl.insert(v)
        assert avl.height() <= 3


class TestAVLTreeSearch:
    """search"""

    def test_search_existing(self):
        avl = AVLTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            avl.insert(v)
        assert avl.search(4) is True
        assert avl.search(9) is True
        assert avl.search(5) is True

    def test_search_non_existing(self):
        avl = AVLTree()
        avl.insert(5)
        assert avl.search(99) is False

    def test_search_empty_tree(self):
        avl = AVLTree()
        assert avl.search(10) is False


class TestAVLTreeContains:
    """__contains__"""

    def test_contains_existing(self):
        avl = AVLTree()
        avl.insert(42)
        assert 42 in avl

    def test_contains_non_existing(self):
        avl = AVLTree()
        avl.insert(42)
        assert 99 not in avl

    def test_contains_empty(self):
        avl = AVLTree()
        assert 10 not in avl


class TestAVLTreeMinMax:
    """min_value / max_value"""

    def test_min_value(self):
        avl = AVLTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            avl.insert(v)
        assert avl.min_value() == 1

    def test_max_value(self):
        avl = AVLTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            avl.insert(v)
        assert avl.max_value() == 9

    def test_min_value_single_node(self):
        avl = AVLTree()
        avl.insert(42)
        assert avl.min_value() == 42
        assert avl.max_value() == 42

    def test_min_value_on_empty_raises(self):
        avl = AVLTree()
        with pytest.raises(Empty):
            avl.min_value()

    def test_max_value_on_empty_raises(self):
        avl = AVLTree()
        with pytest.raises(Empty):
            avl.max_value()


class TestAVLTreeRemove:
    """remove"""

    def test_remove_leaf(self):
        avl = AVLTree()
        for v in [5, 3, 8]:
            avl.insert(v)
        avl.remove(3)
        assert len(avl) == 2
        assert 3 not in avl

    def test_remove_node_with_one_child(self):
        avl = AVLTree()
        for v in [5, 3, 8, 1]:
            avl.insert(v)
        avl.remove(3)
        assert len(avl) == 3
        assert 3 not in avl
        assert 1 in avl

    def test_remove_node_with_two_children(self):
        avl = AVLTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            avl.insert(v)
        avl.remove(5)
        assert len(avl) == 6
        assert 5 not in avl

    def test_remove_root_single_node(self):
        avl = AVLTree()
        avl.insert(10)
        avl.remove(10)
        assert avl.is_empty()

    def test_remove_non_existing(self):
        avl = AVLTree()
        for v in [5, 3, 8]:
            avl.insert(v)
        avl.remove(99)
        assert len(avl) == 3

    def test_remove_from_empty(self):
        avl = AVLTree()
        avl.remove(10)
        assert avl.is_empty()

    def test_remove_maintains_balance(self):
        avl = AVLTree()
        for v in range(1, 32):
            avl.insert(v)
        for v in [10, 15, 20, 25]:
            avl.remove(v)
        assert avl.height() <= 6  # log2(27) ≈ 5, +1 margin


class TestAVLTreeInorder:
    """inorder — sorted"""

    def test_inorder_sorted(self):
        avl = AVLTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            avl.insert(v)
        assert list(avl.inorder()) == [1, 3, 4, 5, 7, 8, 9]

    def test_inorder_after_many_inserts(self):
        avl = AVLTree()
        import random
        values = list(range(100))
        random.shuffle(values)
        for v in values:
            avl.insert(v)
        assert list(avl.inorder()) == list(range(100))

    def test_inorder_empty(self):
        avl = AVLTree()
        assert list(avl.inorder()) == []


class TestAVLTreeTraversals:
    """preorder / postorder / levelorder"""

    def test_all_traversals_non_empty(self):
        avl = AVLTree()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            avl.insert(v)
        pre = list(avl.preorder())
        post = list(avl.postorder())
        level = list(avl.levelorder())
        assert len(pre) == 7
        assert len(post) == 7
        assert len(level) == 7
        assert set(pre) == {1, 3, 4, 5, 7, 8, 9}  # no duplicates
        assert pre == pre  # just verifying no exceptions

    def test_all_traversals_empty(self):
        avl = AVLTree()
        assert list(avl.preorder()) == []
        assert list(avl.inorder()) == []
        assert list(avl.postorder()) == []
        assert list(avl.levelorder()) == []


class TestAVLTreeHeight:
    """height"""

    def test_height_empty(self):
        avl = AVLTree()
        assert avl.height() == 0

    def test_height_single_node(self):
        avl = AVLTree()
        avl.insert(5)
        assert avl.height() == 1

    def test_height_balanced_after_skewed_insert(self):
        avl = AVLTree()
        for v in range(1, 64):  # 63 nodes
            avl.insert(v)
        # Balanced AVL: height ≈ log2(63) + 1 ≈ 7
        assert avl.height() <= 7

    def test_height_stays_logarithmic(self):
        avl = AVLTree()
        n = 127
        for i in range(n):
            avl.insert(i)
        # log2(127) ≈ 7, height should be ≤ 8
        assert avl.height() <= 8


class TestAVLTreeClear:
    """clear"""

    def test_clear_non_empty(self):
        avl = AVLTree()
        for v in [5, 3, 8]:
            avl.insert(v)
        avl.clear()
        assert avl.is_empty()
        assert len(avl) == 0

    def test_clear_empty(self):
        avl = AVLTree()
        avl.clear()
        assert avl.is_empty()


class TestAVLTreeCorrectness:
    """Integration: AVL invariant holds after operations"""

    def _is_balanced(self, node) -> bool:
        """Recursive helper to verify |bf| ≤ 1 and height is correct."""
        if node is None:
            return True
        left_h = node.left.height if node.left else 0
        right_h = node.right.height if node.right else 0
        expected_h = 1 + max(left_h, right_h)
        if node.height != expected_h:
            return False
        if abs(left_h - right_h) > 1:
            return False
        return self._is_balanced(node.left) and self._is_balanced(node.right)

    def _get_root(self, avl):
        return avl._AVLTree__root  # access private for testing

    def test_avl_invariant_after_inserts(self):
        avl = AVLTree()
        for v in range(1, 50):
            avl.insert(v)
        assert self._is_balanced(self._get_root(avl))

    def test_avl_invariant_after_random_inserts(self):
        import random
        avl = AVLTree()
        values = list(range(100))
        random.shuffle(values)
        for v in values:
            avl.insert(v)
        assert self._is_balanced(self._get_root(avl))

    def test_avl_invariant_after_inserts_and_removes(self):
        import random
        avl = AVLTree()
        values = list(range(50))
        random.shuffle(values)
        for v in values:
            avl.insert(v)
        remove_vals = random.sample(values, 20)
        for v in remove_vals:
            avl.remove(v)
        assert self._is_balanced(self._get_root(avl))


class TestAVLTreeLargeData:
    """Large scale"""

    def test_many_inserts_search(self):
        avl = AVLTree()
        n = 500
        for i in range(n):
            avl.insert(i)
        assert len(avl) == n
        for i in range(n):
            assert i in avl

    def test_many_random_operations(self):
        import random
        avl = AVLTree()
        inserted = set()
        for _ in range(200):
            val = random.randint(0, 500)
            avl.insert(val)
            inserted.add(val)
        for v in inserted:
            assert v in avl
        # Remove some
        to_remove = random.sample(list(inserted), min(50, len(inserted)))
        for v in to_remove:
            avl.remove(v)
            inserted.discard(v)
        for v in inserted:
            assert v in avl