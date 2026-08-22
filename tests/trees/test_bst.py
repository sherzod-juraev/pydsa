import pytest

from pydsa import EmptyError, BSTree


def build_bst() -> BSTree[int]:
    bst = BSTree[int]()
    for v in [5, 3, 8, 1, 4, 7, 9]:
        bst.insert(v)
    return bst


class TestBasics:
    def test_new_tree_is_empty(self) -> None:
        bst = BSTree[int]()
        assert bst.is_empty()
        assert len(bst) == 0

    def test_root_raises_when_empty(self) -> None:
        with pytest.raises(EmptyError):
            BSTree[int]().root()

    def test_insert_ignores_duplicates(self) -> None:
        bst = BSTree[int]()
        bst.insert(5)
        bst.insert(3)
        bst.insert(5)  # duplicate
        assert len(bst) == 2

    def test_contains(self) -> None:
        bst = build_bst()
        assert 5 in bst
        assert 99 not in bst


class TestSearch:
    def test_search_found(self) -> None:
        bst = build_bst()
        assert bst.search(5) is True

    def test_search_not_found(self) -> None:
        bst = build_bst()
        assert bst.search(99) is False

    def test_search_empty_tree(self) -> None:
        assert BSTree[int]().search(1) is False


class TestMinMax:
    def test_min_value(self) -> None:
        assert build_bst().min_value() == 1

    def test_max_value(self) -> None:
        assert build_bst().max_value() == 9

    def test_min_value_raises_on_empty(self) -> None:
        with pytest.raises(EmptyError):
            BSTree[int]().min_value()

    def test_max_value_raises_on_empty(self) -> None:
        with pytest.raises(EmptyError):
            BSTree[int]().max_value()


class TestRemove:
    def test_remove_leaf(self) -> None:
        bst = build_bst()
        bst.remove(1)
        assert 1 not in bst
        assert len(bst) == 6

    def test_remove_node_with_one_child(self) -> None:
        bst = BSTree[int]()
        for v in [5, 3, 1]:  # 3 has only a left child
            bst.insert(v)
        bst.remove(3)
        assert 3 not in bst
        assert list(bst.inorder()) == [1, 5]

    def test_remove_node_with_two_children(self) -> None:
        bst = build_bst()
        bst.remove(3)  # has children 1 and 4
        assert 3 not in bst
        assert list(bst.inorder()) == [1, 4, 5, 7, 8, 9]

    def test_remove_root(self) -> None:
        bst = build_bst()
        bst.remove(5)
        assert 5 not in bst
        assert list(bst.inorder()) == [1, 3, 4, 7, 8, 9]

    def test_remove_missing_value_is_noop(self) -> None:
        bst = build_bst()
        bst.remove(999)
        assert len(bst) == 7

    def test_remove_on_empty_tree_is_noop(self) -> None:
        bst = BSTree[int]()
        bst.remove(1)  # should not raise
        assert len(bst) == 0

    def test_remove_all_nodes(self) -> None:
        bst = build_bst()
        for v in [5, 3, 8, 1, 4, 7, 9]:
            bst.remove(v)
        assert bst.is_empty()


class TestTraversals:
    def test_preorder(self) -> None:
        assert list(build_bst().preorder()) == [5, 3, 1, 4, 8, 7, 9]

    def test_inorder_is_sorted(self) -> None:
        assert list(build_bst().inorder()) == [1, 3, 4, 5, 7, 8, 9]

    def test_postorder(self) -> None:
        assert list(build_bst().postorder()) == [1, 4, 3, 7, 9, 8, 5]

    def test_levelorder(self) -> None:
        assert list(build_bst().levelorder()) == [5, 3, 8, 1, 4, 7, 9]

    def test_traversals_on_empty_tree(self) -> None:
        bst = BSTree[int]()
        assert list(bst.preorder()) == []
        assert list(bst.inorder()) == []


class TestHeight:
    def test_height(self) -> None:
        assert build_bst().height() == 3

    def test_height_empty(self) -> None:
        assert BSTree[int]().height() == 0

    def test_degenerate_tree_height_equals_count(self) -> None:
        # inserting sorted data degenerates the BST into a linked list
        bst = BSTree[int]()
        for v in [1, 2, 3, 4, 5]:
            bst.insert(v)
        assert bst.height() == 5


class TestClear:
    def test_clear(self) -> None:
        bst = build_bst()
        bst.clear()
        assert bst.is_empty()
        assert len(bst) == 0