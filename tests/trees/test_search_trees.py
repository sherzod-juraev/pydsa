"""Contract shared by every binary searching tree (BSTree and AVLTree)."""

import random

import pytest

from pydsa.exc import EmptyError
from pydsa.trees import AVLTree, BSTree

TREES = [BSTree, AVLTree]


class Record:
    """Ordered and compared by key only, so equal keys are distinguishable by tag."""

    def __init__(self, key: int, tag: str) -> None:
        self.key = key
        self.tag = tag

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Record) and self.key == other.key

    def __lt__(self, other: "Record") -> bool:
        return self.key < other.key

    def __le__(self, other: "Record") -> bool:
        return self.key <= other.key

    def __gt__(self, other: "Record") -> bool:
        return self.key > other.key

    def __ge__(self, other: "Record") -> bool:
        return self.key >= other.key

    __hash__ = None  # type: ignore[assignment]


def make(tree_cls, values):
    tree = tree_cls()
    for value in values:
        tree.insert(value)
    return tree


@pytest.fixture(params=TREES, ids=lambda cls: cls.__name__)
def tree_cls(request):
    return request.param


class TestEmptyTree:
    def test_size_and_truthiness(self, tree_cls) -> None:
        tree = tree_cls()
        assert len(tree) == 0
        assert not tree

    def test_nothing_is_contained(self, tree_cls) -> None:
        tree = tree_cls()
        assert 1 not in tree
        assert not tree.search(1)

    def test_measures_and_traversals(self, tree_cls) -> None:
        tree = tree_cls()
        assert tree.height() == 0
        assert tree.leaves() == 0
        assert list(tree.preorder()) == list(tree.inorder()) == []
        assert list(tree.postorder()) == list(tree.levelorder()) == []

    @pytest.mark.parametrize("accessor", ["root", "min_value", "max_value"])
    def test_accessors_raise_empty_error(self, tree_cls, accessor: str) -> None:
        with pytest.raises(EmptyError, match=tree_cls.__name__):
            getattr(tree_cls(), accessor)()

    def test_remove_is_a_silent_no_op(self, tree_cls) -> None:
        tree = tree_cls()
        tree.remove(5)
        assert len(tree) == 0

    def test_clear_is_a_no_op(self, tree_cls) -> None:
        tree = tree_cls()
        tree.clear()
        assert len(tree) == 0


class TestInsertAndSearch:
    def test_single_value(self, tree_cls) -> None:
        tree = make(tree_cls, [5])
        assert len(tree) == 1
        assert tree
        assert 5 in tree
        assert tree.root() == 5
        assert tree.min_value() == tree.max_value() == 5
        assert tree.height() == 1
        assert tree.leaves() == 1

    def test_inorder_is_sorted_whatever_the_insertion_order(self, tree_cls) -> None:
        tree = make(tree_cls, [5, 3, 8, 1, 4, 7, 9, 2, 6])
        assert list(tree.inorder()) == list(range(1, 10))

    def test_duplicates_are_ignored(self, tree_cls) -> None:
        tree = make(tree_cls, [5, 3, 8])
        before = (list(tree.preorder()), tree.height())
        for value in (5, 3, 8, 5):
            tree.insert(value)
        assert len(tree) == 3
        assert (list(tree.preorder()), tree.height()) == before

    def test_first_of_equal_keys_is_kept(self, tree_cls) -> None:
        tree = tree_cls()
        tree.insert(Record(1, "first"))
        tree.insert(Record(1, "second"))
        assert len(tree) == 1
        assert [r.tag for r in tree.inorder()] == ["first"]

    def test_search_and_in_agree(self, tree_cls) -> None:
        tree = make(tree_cls, [10, 5, 15, 3, 7, 12, 18])
        for value in range(0, 21):
            assert tree.search(value) == (value in tree) == (value in {10, 5, 15, 3, 7, 12, 18})

    @pytest.mark.parametrize("target", [-100, 0, 2, 4, 6, 8, 9, 100])
    def test_absent_values_below_between_and_above(self, tree_cls, target: int) -> None:
        tree = make(tree_cls, [1, 3, 5, 7])
        assert target not in tree

    def test_min_and_max_follow_inserts(self, tree_cls) -> None:
        tree = tree_cls()
        for value, low, high in [(5, 5, 5), (3, 3, 5), (9, 3, 9), (1, 1, 9), (20, 1, 20)]:
            tree.insert(value)
            assert (tree.min_value(), tree.max_value()) == (low, high)

    def test_negative_numbers_and_floats(self, tree_cls) -> None:
        tree = make(tree_cls, [3.5, -1, 0, -7.25, 2, 0.5])
        assert list(tree.inorder()) == [-7.25, -1, 0, 0.5, 2, 3.5]
        assert -1 in tree
        assert 1 not in tree

    def test_strings(self, tree_cls) -> None:
        tree = make(tree_cls, ["pear", "apple", "fig", "mango"])
        assert list(tree.inorder()) == ["apple", "fig", "mango", "pear"]
        assert tree.min_value() == "apple"
        assert tree.max_value() == "pear"
        assert "kiwi" not in tree

    def test_tuples(self, tree_cls) -> None:
        tree = make(tree_cls, [(2, "b"), (1, "z"), (2, "a")])
        assert list(tree.inorder()) == [(1, "z"), (2, "a"), (2, "b")]

    def test_zero_and_falsy_values_are_ordinary(self, tree_cls) -> None:
        tree = make(tree_cls, [0, -1, 1])
        assert 0 in tree
        assert tree.min_value() == -1


class TestRemove:
    def test_remove_missing_value_changes_nothing(self, tree_cls) -> None:
        tree = make(tree_cls, [5, 3, 8])
        before = list(tree.preorder())
        tree.remove(99)
        tree.remove(4)
        assert len(tree) == 3
        assert list(tree.preorder()) == before

    def test_remove_leaf(self, tree_cls) -> None:
        tree = make(tree_cls, [5, 3, 8, 1])
        tree.remove(1)
        assert list(tree.inorder()) == [3, 5, 8]
        assert 1 not in tree
        assert len(tree) == 3

    def test_remove_node_with_one_child(self, tree_cls) -> None:
        tree = make(tree_cls, [5, 3, 8, 1])
        tree.remove(3)
        assert list(tree.inorder()) == [1, 5, 8]
        tree = make(tree_cls, [5, 3, 8, 4])
        tree.remove(3)
        assert list(tree.inorder()) == [4, 5, 8]

    def test_remove_node_with_two_children(self, tree_cls) -> None:
        tree = make(tree_cls, [5, 3, 8, 1, 4, 7, 9])
        tree.remove(8)
        assert list(tree.inorder()) == [1, 3, 4, 5, 7, 9]
        tree.remove(3)
        assert list(tree.inorder()) == [1, 4, 5, 7, 9]

    def test_remove_the_root_in_every_shape(self, tree_cls) -> None:
        for values in ([5], [5, 3], [5, 8], [5, 3, 8], [5, 3, 8, 1, 4, 7, 9]):
            tree = make(tree_cls, values)
            root = tree.root()
            tree.remove(root)
            assert root not in tree
            assert list(tree.inorder()) == sorted(set(values) - {root})
            assert len(tree) == len(values) - 1

    def test_remove_the_only_value_empties_the_tree(self, tree_cls) -> None:
        tree = make(tree_cls, [5])
        tree.remove(5)
        assert len(tree) == 0
        assert not tree
        assert tree.height() == 0
        with pytest.raises(EmptyError):
            tree.root()
        with pytest.raises(EmptyError):
            tree.min_value()

    def test_min_and_max_follow_removes(self, tree_cls) -> None:
        tree = make(tree_cls, [5, 3, 8, 1, 9])
        tree.remove(1)
        assert tree.min_value() == 3
        tree.remove(9)
        assert tree.max_value() == 8

    def test_remove_does_not_touch_other_values(self, tree_cls) -> None:
        tree = make(tree_cls, range(20))
        tree.remove(10)
        assert [v for v in range(20) if v in tree] == [v for v in range(20) if v != 10]

    def test_remove_by_equal_key_removes_the_stored_record(self, tree_cls) -> None:
        tree = tree_cls()
        tree.insert(Record(1, "stored"))
        tree.insert(Record(2, "other"))
        tree.remove(Record(1, "probe"))
        assert [r.tag for r in tree.inorder()] == ["other"]

    def test_reinsert_after_remove(self, tree_cls) -> None:
        tree = make(tree_cls, [5, 3, 8])
        tree.remove(3)
        tree.insert(3)
        assert list(tree.inorder()) == [3, 5, 8]
        assert len(tree) == 3

    @pytest.mark.parametrize("seed", range(10))
    def test_removing_everything_in_random_order(self, tree_cls, seed: int) -> None:
        rng = random.Random(seed)
        values = rng.sample(range(100), 40)
        tree = make(tree_cls, values)
        rng.shuffle(values)
        remaining = set(values)
        for value in values:
            tree.remove(value)
            remaining.discard(value)
            assert list(tree.inorder()) == sorted(remaining)
            assert len(tree) == len(remaining)
        assert not tree


class TestClear:
    def test_clear_resets_everything(self, tree_cls) -> None:
        tree = make(tree_cls, [5, 3, 8])
        tree.clear()
        assert len(tree) == 0
        assert not tree
        assert 5 not in tree
        assert tree.height() == 0
        assert list(tree.levelorder()) == []
        with pytest.raises(EmptyError):
            tree.max_value()

    def test_reusable_after_clear(self, tree_cls) -> None:
        tree = make(tree_cls, [5, 3, 8])
        tree.clear()
        tree.insert(1)
        tree.insert(2)
        assert list(tree.inorder()) == [1, 2]
        assert len(tree) == 2


class TestScale:
    def test_ascending_inserts_do_not_hit_the_recursion_limit(self, tree_cls) -> None:
        tree = make(tree_cls, range(2000))
        assert list(tree.inorder()) == list(range(2000))
        assert list(tree.preorder())[:1] == [tree.root()]
        assert len(list(tree.postorder())) == 2000
        assert 1999 in tree

    def test_descending_inserts(self, tree_cls) -> None:
        tree = make(tree_cls, range(2000, 0, -1))
        assert list(tree.inorder()) == list(range(1, 2001))
        assert tree.min_value() == 1
        assert tree.max_value() == 2000

    def test_remove_from_a_large_degenerate_tree(self, tree_cls) -> None:
        tree = make(tree_cls, range(1500))
        for value in range(0, 1500, 2):
            tree.remove(value)
        assert list(tree.inorder()) == list(range(1, 1500, 2))


class TestAgainstASetModel:
    @pytest.mark.parametrize("seed", range(40))
    @pytest.mark.parametrize("key_range", [8, 60])
    def test_random_operation_sequences(self, tree_cls, seed: int, key_range: int) -> None:
        rng = random.Random(seed)
        tree = tree_cls()
        model: set[int] = set()
        for _ in range(rng.randrange(0, 120)):
            value = rng.randrange(key_range)
            if rng.random() < 0.6:
                tree.insert(value)
                model.add(value)
            else:
                tree.remove(value)
                model.discard(value)
            assert len(tree) == len(model)
            assert list(tree.inorder()) == sorted(model)
            assert (value in tree) == (value in model)
            if model:
                assert tree.min_value() == min(model)
                assert tree.max_value() == max(model)
