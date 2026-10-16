"""Behaviour that BinaryTree, BSTree and AVLTree inherit from BinaryTreeBase."""

import random
from collections import deque

import pytest

from pydsa.core import BaseStructure
from pydsa.exc import EmptyError
from pydsa.trees import AVLTree, BinaryTree, BSTree
from pydsa.trees.base import BinaryTreeBase, SearchTreeBase
from pydsa.trees.heap import HeapBase


def nested(node):
    """Turn the node structure into ``(value, left, right)`` tuples."""
    return None if node is None else (node.value, nested(node.left), nested(node.right))


def ref_preorder(t):
    return [] if t is None else [t[0], *ref_preorder(t[1]), *ref_preorder(t[2])]


def ref_inorder(t):
    return [] if t is None else [*ref_inorder(t[1]), t[0], *ref_inorder(t[2])]


def ref_postorder(t):
    return [] if t is None else [*ref_postorder(t[1]), *ref_postorder(t[2]), t[0]]


def ref_levelorder(t):
    out, queue = [], deque([t] if t else [])
    while queue:
        node = queue.popleft()
        out.append(node[0])
        queue.extend(child for child in node[1:] if child)
    return out


def ref_height(t):
    return 0 if t is None else 1 + max(ref_height(t[1]), ref_height(t[2]))


def ref_leaves(t):
    if t is None:
        return 0
    return 1 if t[1] is None and t[2] is None else ref_leaves(t[1]) + ref_leaves(t[2])


def random_tree(kind: str, rng: random.Random) -> BinaryTreeBase[int]:
    if kind == "BinaryTree":
        binary: BinaryTree[int] = BinaryTree()
        paths: set[str] = set()
        for value in range(rng.randrange(0, 50)):
            free = [""] if not paths else [p + c for p in paths for c in "LR" if p + c not in paths]
            path = rng.choice(free)
            binary.insert(value, path)
            paths.add(path)
        return binary
    search: SearchTreeBase[int] = BSTree() if kind == "BSTree" else AVLTree()
    for _ in range(rng.randrange(0, 80)):
        search.insert(rng.randrange(100))
    return search


KINDS = ["BinaryTree", "BSTree", "AVLTree"]


@pytest.mark.parametrize("kind", KINDS)
class TestSharedTraversalsAndMeasures:
    @pytest.mark.parametrize("seed", range(40))
    def test_match_a_recursive_reference(self, kind: str, seed: int) -> None:
        tree = random_tree(kind, random.Random(seed))
        shape = nested(tree._root)
        assert list(tree.preorder()) == ref_preorder(shape)
        assert list(tree.inorder()) == ref_inorder(shape)
        assert list(tree.postorder()) == ref_postorder(shape)
        assert list(tree.levelorder()) == ref_levelorder(shape)
        assert tree.height() == ref_height(shape)
        assert tree.leaves() == ref_leaves(shape)
        assert len(tree) == len(ref_preorder(shape))

    @pytest.mark.parametrize("seed", range(10))
    def test_root_is_the_value_at_the_root_node(self, kind: str, seed: int) -> None:
        tree = random_tree(kind, random.Random(seed))
        root = tree._root
        if root is not None:
            assert tree.root() == root.value
        else:
            with pytest.raises(EmptyError):
                tree.root()

    @pytest.mark.parametrize("seed", range(10))
    def test_clear_resets_the_tree(self, kind: str, seed: int) -> None:
        tree = random_tree(kind, random.Random(seed))
        tree.clear()
        assert len(tree) == 0
        assert not tree
        assert tree._root is None
        assert (tree.height(), tree.leaves()) == (0, 0)
        assert list(tree.preorder()) == list(tree.levelorder()) == []

    def test_traversals_are_lazy_iterators(self, kind: str) -> None:
        tree = random_tree(kind, random.Random(1))
        assert tree
        for traversal in (tree.preorder, tree.inorder, tree.postorder, tree.levelorder):
            iterator = traversal()
            assert iter(iterator) is iterator
            next(iterator)

    def test_is_a_pydsa_structure(self, kind: str) -> None:
        tree = random_tree(kind, random.Random(1))
        assert isinstance(tree, BaseStructure)
        assert isinstance(tree, BinaryTreeBase)
        assert not isinstance(tree, HeapBase)


class TestHierarchy:
    def test_search_trees_share_the_search_base(self) -> None:
        assert issubclass(BSTree, SearchTreeBase)
        assert issubclass(AVLTree, SearchTreeBase)
        assert not issubclass(BinaryTree, SearchTreeBase)

    def test_every_tree_shares_the_binary_base(self) -> None:
        for cls in (BinaryTree, BSTree, AVLTree, SearchTreeBase):
            assert issubclass(cls, BinaryTreeBase)

    def test_search_base_is_abstract(self) -> None:
        with pytest.raises(TypeError):
            SearchTreeBase()  # type: ignore[abstract]

    def test_binary_tree_has_no_search_operations(self) -> None:
        for name in ("search", "min_value", "max_value", "remove", "__contains__"):
            assert not hasattr(BinaryTree, name)

    def test_search_trees_gain_leaves_from_the_base(self) -> None:
        tree = BSTree[int]()
        for value in (5, 3, 8, 1, 4, 7, 9):
            tree.insert(value)
        assert tree.leaves() == 4
        avl = AVLTree[int]()
        for value in (1, 2, 3):
            avl.insert(value)
        assert avl.leaves() == 2

    def test_avl_overrides_only_height(self) -> None:
        assert AVLTree.height is not BinaryTreeBase.height
        assert BSTree.height is BinaryTreeBase.height
        assert AVLTree.preorder is BinaryTreeBase.preorder
