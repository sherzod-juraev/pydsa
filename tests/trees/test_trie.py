import random

import pytest

from pydsa.core import BaseStructure
from pydsa.trees import Trie
from pydsa.trees.base import BinaryTreeBase


def make(words) -> Trie:
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie


def check_invariants(trie: Trie, expected: set[str]) -> None:
    """No node may be left over without a word below it, and the size must match."""
    words = 0
    stack = [trie._root]
    while stack:
        node = stack.pop()
        words += node.is_end
        for child in node.children.values():
            assert child.is_end or child.children, "dangling node"
            stack.append(child)
    assert words == len(trie) == len(expected)


class TestEmptyTrie:
    def test_size_and_truthiness(self) -> None:
        trie = Trie()
        assert len(trie) == 0
        assert not trie

    def test_nothing_is_found(self) -> None:
        trie = Trie()
        assert "a" not in trie
        assert not trie.search("a")
        assert not trie.starts_with("a")
        assert "" not in trie

    def test_empty_prefix_matches_nothing_in_an_empty_trie(self) -> None:
        assert not Trie().starts_with("")

    def test_no_words(self) -> None:
        trie = Trie()
        assert list(trie.all_words()) == []
        assert list(trie.words_with_prefix("a")) == []
        assert list(trie.words_with_prefix("")) == []

    def test_remove_returns_false(self) -> None:
        assert Trie().remove("a") is False
        assert Trie().remove("") is False

    def test_clear_is_a_no_op(self) -> None:
        trie = Trie()
        trie.clear()
        assert len(trie) == 0


class TestInsertAndSearch:
    def test_inserted_word_is_found(self) -> None:
        trie = make(["cat"])
        assert "cat" in trie
        assert trie.search("cat")
        assert len(trie) == 1
        assert trie

    def test_a_prefix_of_a_word_is_not_a_word(self) -> None:
        trie = make(["cat"])
        assert "ca" not in trie
        assert "c" not in trie
        assert not trie.search("")

    def test_an_extension_of_a_word_is_not_a_word(self) -> None:
        trie = make(["cat"])
        assert "cats" not in trie
        assert "cat " not in trie

    def test_a_word_that_prefixes_another_word(self) -> None:
        trie = make(["cat", "cats"])
        assert "cat" in trie
        assert "cats" in trie
        assert len(trie) == 2

    def test_insertion_order_does_not_matter(self) -> None:
        a = make(["cats", "cat", "car"])
        b = make(["car", "cat", "cats"])
        assert list(a.all_words()) == list(b.all_words())
        assert len(a) == len(b) == 3

    def test_duplicates_are_ignored(self) -> None:
        trie = make(["cat", "cat", "cat"])
        assert len(trie) == 1
        assert list(trie.all_words()) == ["cat"]

    def test_inserting_a_prefix_later_counts_as_a_new_word(self) -> None:
        trie = make(["cats"])
        trie.insert("cat")
        assert len(trie) == 2
        assert "cat" in trie

    def test_search_and_in_agree(self) -> None:
        trie = make(["a", "ab", "abc", "b"])
        for word in ["", "a", "ab", "abc", "abcd", "b", "ba", "c"]:
            assert trie.search(word) == (word in trie) == (word in {"a", "ab", "abc", "b"})

    def test_search_is_case_sensitive(self) -> None:
        trie = make(["Cat"])
        assert "Cat" in trie
        assert "cat" not in trie
        assert "CAT" not in trie

    def test_single_characters(self) -> None:
        trie = make(["a", "b", "c"])
        assert len(trie) == 3
        assert "b" in trie

    def test_digits_spaces_and_punctuation(self) -> None:
        trie = make(["a b", "a-b", "123", "x_y"])
        assert all(w in trie for w in ["a b", "a-b", "123", "x_y"])
        assert "a" not in trie

    def test_unicode_words(self) -> None:
        words = ["niño", "ñandú", "straße", "日本語", "日本", "😀", "😀😀"]
        trie = make(words)
        assert all(w in trie for w in words)
        assert "日" not in trie
        assert list(trie.all_words()) == sorted(words)

    def test_the_empty_string_is_a_word(self) -> None:
        trie = make([""])
        assert "" in trie
        assert trie.search("")
        assert len(trie) == 1
        assert trie
        assert list(trie.all_words()) == [""]

    def test_the_empty_string_coexists_with_other_words(self) -> None:
        trie = make(["", "a", "ab"])
        assert len(trie) == 3
        assert list(trie.all_words()) == ["", "a", "ab"]

    def test_the_empty_string_is_inserted_only_once(self) -> None:
        trie = make(["", ""])
        assert len(trie) == 1

    def test_a_very_long_word(self) -> None:
        word = "a" * 20_000
        trie = make([word])
        assert word in trie
        assert word[:-1] not in trie
        assert trie.remove(word)
        assert len(trie) == 0


class TestStartsWith:
    def test_proper_prefix_full_word_and_miss(self) -> None:
        trie = make(["cat"])
        assert trie.starts_with("c")
        assert trie.starts_with("ca")
        assert trie.starts_with("cat")
        assert not trie.starts_with("cats")
        assert not trie.starts_with("d")
        assert not trie.starts_with("cb")

    def test_empty_prefix_matches_any_non_empty_trie(self) -> None:
        assert make(["cat"]).starts_with("")
        assert make([""]).starts_with("")

    def test_a_prefix_that_is_itself_a_word(self) -> None:
        trie = make(["ca", "cat"])
        assert trie.starts_with("ca")

    def test_prefix_after_removal(self) -> None:
        trie = make(["cat", "car"])
        trie.remove("cat")
        assert trie.starts_with("ca")
        assert not trie.starts_with("cat")
        trie.remove("car")
        assert not trie.starts_with("c")
        assert not trie.starts_with("")


class TestRemove:
    def test_remove_returns_true_for_a_stored_word(self) -> None:
        trie = make(["cat"])
        assert trie.remove("cat") is True
        assert "cat" not in trie
        assert len(trie) == 0

    def test_remove_returns_false_for_an_absent_word(self) -> None:
        trie = make(["cat"])
        assert trie.remove("dog") is False
        assert trie.remove("cats") is False
        assert len(trie) == 1
        assert "cat" in trie

    def test_a_prefix_that_is_not_a_word_is_not_removed(self) -> None:
        trie = make(["cat"])
        assert trie.remove("ca") is False
        assert "cat" in trie
        assert len(trie) == 1

    def test_second_remove_returns_false(self) -> None:
        trie = make(["cat"])
        assert trie.remove("cat") is True
        assert trie.remove("cat") is False
        assert len(trie) == 0

    def test_removing_a_word_keeps_its_extension(self) -> None:
        trie = make(["cat", "cats"])
        assert trie.remove("cat")
        assert "cats" in trie
        assert "cat" not in trie
        assert len(trie) == 1
        assert trie.starts_with("cat")

    def test_removing_an_extension_keeps_the_word(self) -> None:
        trie = make(["cat", "cats"])
        assert trie.remove("cats")
        assert "cat" in trie
        assert "cats" not in trie
        assert not trie.starts_with("cats")

    def test_removing_keeps_words_that_share_a_prefix(self) -> None:
        trie = make(["car", "cat", "cart"])
        assert trie.remove("cat")
        assert list(trie.all_words()) == ["car", "cart"]
        assert trie.remove("cart")
        assert list(trie.all_words()) == ["car"]

    def test_removing_the_only_word_empties_the_structure(self) -> None:
        trie = make(["cat"])
        trie.remove("cat")
        assert trie._root.children == {}
        assert not trie.starts_with("c")

    def test_the_branch_is_cut_at_the_first_shared_node(self) -> None:
        trie = make(["abc", "abd"])
        trie.remove("abc")
        assert set(trie._root.children["a"].children["b"].children) == {"d"}

    def test_the_branch_is_cut_at_an_inner_word(self) -> None:
        trie = make(["ab", "abcd"])
        trie.remove("abcd")
        node = trie._root.children["a"].children["b"]
        assert node.is_end
        assert node.children == {}

    def test_remove_the_empty_string(self) -> None:
        trie = make(["", "a"])
        assert trie.remove("") is True
        assert "" not in trie
        assert "a" in trie
        assert len(trie) == 1

    def test_remove_the_empty_string_when_it_is_not_stored(self) -> None:
        trie = make(["a"])
        assert trie.remove("") is False
        assert len(trie) == 1

    def test_reinsert_after_remove(self) -> None:
        trie = make(["cat", "car"])
        trie.remove("cat")
        trie.insert("cat")
        assert list(trie.all_words()) == ["car", "cat"]
        assert len(trie) == 2

    def test_remove_all_words_one_by_one(self) -> None:
        words = ["a", "ab", "abc", "b", "bc", "c"]
        trie = make(words)
        for count, word in enumerate(words, start=1):
            assert trie.remove(word)
            assert len(trie) == len(words) - count
        assert trie._root.children == {}
        assert not trie


class TestWordsWithPrefix:
    def test_alphabetical_order(self) -> None:
        trie = make(["car", "cat", "cats", "dog"])
        assert list(trie.words_with_prefix("ca")) == ["car", "cat", "cats"]

    def test_the_prefix_itself_comes_first_when_it_is_a_word(self) -> None:
        trie = make(["cats", "cat", "ca"])
        assert list(trie.words_with_prefix("ca")) == ["ca", "cat", "cats"]

    def test_a_missing_prefix_gives_nothing(self) -> None:
        trie = make(["cat"])
        assert list(trie.words_with_prefix("x")) == []
        assert list(trie.words_with_prefix("cax")) == []
        assert list(trie.words_with_prefix("cats")) == []

    def test_a_prefix_equal_to_a_leaf_word(self) -> None:
        trie = make(["cat"])
        assert list(trie.words_with_prefix("cat")) == ["cat"]

    def test_empty_prefix_gives_every_word_sorted(self) -> None:
        words = ["pear", "apple", "fig", "apricot", "app"]
        trie = make(words)
        assert list(trie.words_with_prefix("")) == sorted(words)

    def test_order_is_by_code_point_like_sorted(self) -> None:
        words = ["b", "B", "a", "A", "ab", "aB", "Ab", "1", "_", "z", "é"]
        assert list(make(words).all_words()) == sorted(words)

    def test_the_result_is_a_lazy_iterator(self) -> None:
        trie = make(["a", "b"])
        iterator = trie.words_with_prefix("")
        assert iter(iterator) is iterator
        assert next(iterator) == "a"
        assert next(iterator) == "b"
        with pytest.raises(StopIteration):
            next(iterator)

    def test_iterating_twice_gives_the_same_words(self) -> None:
        trie = make(["a", "ab"])
        assert list(trie.all_words()) == list(trie.all_words())

    def test_iteration_does_not_change_the_trie(self) -> None:
        trie = make(["a", "ab", "b"])
        list(trie.all_words())
        assert len(trie) == 3
        assert "ab" in trie

    def test_all_words_is_the_same_as_the_empty_prefix(self) -> None:
        trie = make(["x", "xy", "y"])
        assert list(trie.all_words()) == list(trie.words_with_prefix(""))


class TestClear:
    def test_clear_removes_everything(self) -> None:
        trie = make(["a", "ab", "b"])
        trie.clear()
        assert len(trie) == 0
        assert not trie
        assert "a" not in trie
        assert list(trie.all_words()) == []
        assert not trie.starts_with("")

    def test_clear_also_removes_the_empty_string(self) -> None:
        trie = make(["", "a"])
        trie.clear()
        assert "" not in trie
        assert list(trie.all_words()) == []
        assert len(trie) == 0

    def test_reusable_after_clear(self) -> None:
        trie = make(["a", "ab"])
        trie.clear()
        trie.insert("z")
        assert list(trie.all_words()) == ["z"]
        assert len(trie) == 1


class TestHierarchy:
    def test_trie_is_a_pydsa_structure_but_not_a_binary_tree(self) -> None:
        assert issubclass(Trie, BaseStructure)
        assert not issubclass(Trie, BinaryTreeBase)

    def test_truthiness_follows_len(self) -> None:
        trie = Trie()
        assert not trie
        trie.insert("a")
        assert trie
        trie.remove("a")
        assert not trie


class TestAgainstASetModel:
    @pytest.mark.parametrize("seed", range(60))
    @pytest.mark.parametrize("alphabet", ["ab", "abcdef"])
    def test_random_operation_sequences(self, seed: int, alphabet: str) -> None:
        rng = random.Random(seed)
        trie = Trie()
        model: set[str] = set()
        prefixes = ["", "a", "b", "ab", "ba", "abc", "f"]
        for _ in range(rng.randrange(0, 80)):
            word = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 5)))
            if rng.random() < 0.6:
                trie.insert(word)
                model.add(word)
            else:
                assert trie.remove(word) == (word in model)
                model.discard(word)
            assert len(trie) == len(model)
            assert (word in trie) == (word in model)
            assert list(trie.all_words()) == sorted(model)
            for prefix in prefixes:
                assert trie.starts_with(prefix) == any(w.startswith(prefix) for w in model)
                assert list(trie.words_with_prefix(prefix)) == sorted(
                    w for w in model if w.startswith(prefix)
                )
            check_invariants(trie, model)
