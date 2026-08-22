import pytest

from pydsa import EmptyError, AVLTree


class TestBasics:
    def test_new_tree_is_empty(self) -> None:
        avl = AVLTree[int]()
        assert avl.is_empty()
        assert len(avl) == 0

    def test_root_raises_when_empty(self) -> None:
        with pytest.raises(EmptyError):
            AVLTree[int]().root()

    def test_insert_ignores_duplicates(self) -> None:
        avl = AVLTree[int]()
        avl.insert(5)
        avl.insert(5)
        assert len(avl) == 1


class TestBalancing:
    def test_sequential_insert_stays_balanced(self) -> None:
        """The whole point of AVL over a plain BST: sequential inserts
        that would degenerate a BST into a height-n chain must stay
        at O(log n) height here.
        """
        avl = AVLTree[int]()
        for v in [10, 20, 30]:
            avl.insert(v)
        assert avl.height() == 2  # not 3, as a plain BST would give

    def test_larger_sequential_insert_stays_logarithmic(self) -> None:
        avl = AVLTree[int]()
        for v in range(1, 16):  # 15 sequential inserts
            avl.insert(v)
        assert len(avl) == 15
        assert avl.height() <= 5  # log2(15) rounded up + slack

    def test_ll_rotation_case(self) -> None:
        avl = AVLTree[int]()
        for v in [30, 20, 10]:  # triggers a single right rotation
            avl.insert(v)
        assert list(avl.inorder()) == [10, 20, 30]
        assert avl.root() == 20

    def test_rr_rotation_case(self) -> None:
        avl = AVLTree[int]()
        for v in [10, 20, 30]:  # triggers a single left rotation
            avl.insert(v)
        assert avl.root() == 20

    def test_lr_rotation_case(self) -> None:
        avl = AVLTree[int]()
        for v in [30, 10, 20]:  # triggers left-right rotation
            avl.insert(v)
        assert avl.root() == 20

    def test_rl_rotation_case(self) -> None:
        avl = AVLTree[int]()
        for v in [10, 30, 20]:  # triggers right-left rotation
            avl.insert(v)
        assert avl.root() == 20

    def test_remove_keeps_tree_balanced(self) -> None:
        avl = AVLTree[int]()
        for v in [10, 20, 30, 40, 50]:
            avl.insert(v)
        avl.remove(10)
        avl.remove(20)
        # after removals the tree must still respect AVL height bound
        assert avl.height() <= 3


class TestSearchMinMax:
    def test_search(self) -> None:
        avl = AVLTree[int]()
        avl.insert(5)
        assert avl.search(5) is True
        assert avl.search(99) is False

    def test_min_max_value(self) -> None:
        avl = AVLTree[int]()
        for v in [5, 3, 8, 1, 9]:
            avl.insert(v)
        assert avl.min_value() == 1
        assert avl.max_value() == 9

    def test_min_value_raises_on_empty(self) -> None:
        with pytest.raises(EmptyError):
            AVLTree[int]().min_value()


class TestRemove:
    def test_remove_leaf(self) -> None:
        avl = AVLTree[int]()
        for v in [5, 3, 8]:
            avl.insert(v)
        avl.remove(3)
        assert 3 not in avl
        assert len(avl) == 2

    def test_remove_missing_value_is_noop(self) -> None:
        avl = AVLTree[int]()
        avl.insert(5)
        avl.remove(999)
        assert len(avl) == 1

    def test_remove_all_nodes(self) -> None:
        avl = AVLTree[int]()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            avl.insert(v)
        for v in [5, 3, 8, 1, 4, 7, 9]:
            avl.remove(v)
        assert avl.is_empty()


class TestTraversals:
    def test_inorder_is_sorted(self) -> None:
        avl = AVLTree[int]()
        for v in [5, 3, 8, 1, 4]:
            avl.insert(v)
        assert list(avl.inorder()) == [1, 3, 4, 5, 8]

    def test_preorder_postorder_levelorder_lengths(self) -> None:
        avl = AVLTree[int]()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            avl.insert(v)
        assert len(list(avl.preorder())) == 7
        assert len(list(avl.postorder())) == 7
        assert len(list(avl.levelorder())) == 7


class TestClear:
    def test_clear(self) -> None:
        avl = AVLTree[int]()
        avl.insert(5)
        avl.clear()
        assert avl.is_empty()