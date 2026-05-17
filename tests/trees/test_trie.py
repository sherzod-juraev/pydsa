import pytest
from pydsa import Trie


class TestTrieInit:
    """__init__"""

    def test_empty_trie_has_zero_length(self):
        trie = Trie()
        assert len(trie) == 0

    def test_empty_trie_is_falsy(self):
        trie = Trie()
        assert not trie


class TestTrieInsert:
    """insert"""

    def test_insert_single_word(self):
        trie = Trie()
        trie.insert("hello")
        assert len(trie) == 1

    def test_insert_multiple_words(self):
        trie = Trie()
        for word in ["cat", "car", "dog", "dot"]:
            trie.insert(word)
        assert len(trie) == 4

    def test_insert_duplicate_ignored(self):
        trie = Trie()
        trie.insert("hello")
        trie.insert("hello")
        trie.insert("hello")
        assert len(trie) == 1

    def test_insert_empty_string(self):
        trie = Trie()
        trie.insert("")
        assert len(trie) == 1
        assert "" in trie


class TestTrieSearch:
    """searching"""

    def test_search_existing(self):
        trie = Trie()
        trie.insert("hello")
        assert trie.search("hello") is True

    def test_search_non_existing(self):
        trie = Trie()
        trie.insert("hello")
        assert trie.search("world") is False

    def test_search_prefix_not_word(self):
        trie = Trie()
        trie.insert("hello")
        assert trie.search("hel") is False

    def test_search_empty_trie(self):
        trie = Trie()
        assert trie.search("hello") is False


class TestTrieContains:
    """__contains__"""

    def test_contains_existing(self):
        trie = Trie()
        trie.insert("world")
        assert "world" in trie

    def test_contains_non_existing(self):
        trie = Trie()
        assert "world" not in trie

    def test_contains_empty_string(self):
        trie = Trie()
        trie.insert("")
        assert "" in trie


class TestTrieStartsWith:
    """starts_with"""

    def test_starts_with_existing_prefix(self):
        trie = Trie()
        trie.insert("hello")
        assert trie.starts_with("hel") is True
        assert trie.starts_with("h") is True
        assert trie.starts_with("hello") is True

    def test_starts_with_non_existing_prefix(self):
        trie = Trie()
        trie.insert("hello")
        assert trie.starts_with("hex") is False
        assert trie.starts_with("world") is False

    def test_starts_with_empty_string(self):
        trie = Trie()
        trie.insert("hello")
        assert trie.starts_with("") is True

    def test_starts_with_empty_trie(self):
        trie = Trie()
        assert trie.starts_with("h") is False


class TestTrieRemove:
    """remove"""

    def test_remove_existing_word(self):
        trie = Trie()
        trie.insert("hello")
        assert trie.remove("hello") is True
        assert len(trie) == 0
        assert "hello" not in trie

    def test_remove_non_existing_word(self):
        trie = Trie()
        trie.insert("hello")
        assert trie.remove("world") is False
        assert len(trie) == 1

    def test_remove_prefix_does_not_affect_longer_word(self):
        trie = Trie()
        trie.insert("hello")
        trie.remove("hel")  # prefix, word emas
        assert len(trie) == 1
        assert "hello" in trie

    def test_remove_word_with_shared_prefix(self):
        trie = Trie()
        trie.insert("cat")
        trie.insert("cats")
        trie.remove("cats")
        assert len(trie) == 1
        assert "cat" in trie
        assert "cats" not in trie

    def test_remove_word_cleans_up_nodes(self):
        trie = Trie()
        trie.insert("cat")
        trie.remove("cat")
        assert trie.starts_with("c") is False
        assert trie.starts_with("ca") is False

    def test_remove_word_keeps_shared_prefix(self):
        trie = Trie()
        trie.insert("car")
        trie.insert("cat")
        trie.remove("car")
        assert len(trie) == 1
        assert "cat" in trie
        assert trie.starts_with("ca") is True

    def test_remove_empty_trie(self):
        trie = Trie()
        assert trie.remove("hello") is False


class TestTrieWordsWithPrefix:
    """words_with_prefix"""

    def test_words_with_prefix(self):
        trie = Trie()
        for word in ["cat", "car", "cart", "dog", "dot"]:
            trie.insert(word)
        result = list(trie.words_with_prefix("ca"))
        assert result == ["car", "cart", "cat"]

    def test_words_with_prefix_full_word(self):
        trie = Trie()
        trie.insert("hello")
        assert list(trie.words_with_prefix("hello")) == ["hello"]

    def test_words_with_prefix_none(self):
        trie = Trie()
        trie.insert("hello")
        assert list(trie.words_with_prefix("x")) == []

    def test_words_with_prefix_empty_string(self):
        trie = Trie()
        trie.insert("a")
        trie.insert("b")
        assert list(trie.words_with_prefix("")) == ["a", "b"]

    def test_words_with_prefix_empty_trie(self):
        trie = Trie()
        assert list(trie.words_with_prefix("a")) == []


class TestTrieAllWords:
    """all_words"""

    def test_all_words_sorted(self):
        trie = Trie()
        for word in ["dog", "apple", "cat", "bird"]:
            trie.insert(word)
        assert list(trie.all_words()) == ["apple", "bird", "cat", "dog"]

    def test_all_words_empty_trie(self):
        trie = Trie()
        assert list(trie.all_words()) == []

    def test_all_words_after_remove(self):
        trie = Trie()
        for word in ["cat", "car", "dog"]:
            trie.insert(word)
        trie.remove("car")
        assert list(trie.all_words()) == ["cat", "dog"]


class TestTrieClear:
    """clear"""

    def test_clear_non_empty(self):
        trie = Trie()
        for word in ["hello", "world"]:
            trie.insert(word)
        trie.clear()
        assert len(trie) == 0
        assert not trie

    def test_clear_empty(self):
        trie = Trie()
        trie.clear()
        assert len(trie) == 0


class TestTrieLargeData:
    """Large data"""

    def test_many_words(self):
        trie = Trie()
        words = [f"word{i:04d}" for i in range(1000)]
        for w in words:
            trie.insert(w)
        assert len(trie) == 1000
        for w in words:
            assert w in trie

    def test_many_words_with_common_prefix(self):
        trie = Trie()
        for i in range(500):
            trie.insert(f"prefix{i:04d}")
        result = list(trie.words_with_prefix("prefix"))
        assert len(result) == 500
        assert result[0] == "prefix0000"
        assert result[-1] == "prefix0499"


class TestTrieEdgeCases:
    """Edge cases"""

    def test_single_character_words(self):
        trie = Trie()
        for c in "abcxyz":
            trie.insert(c)
        assert len(trie) == 6
        assert list(trie.all_words()) == ["a", "b", "c", "x", "y", "z"]

    def test_case_sensitivity(self):
        trie = Trie()
        trie.insert("Hello")
        trie.insert("hello")
        assert len(trie) == 2
        assert "Hello" in trie
        assert "hello" in trie

    def test_long_word(self):
        trie = Trie()
        long_word = "a" * 1000
        trie.insert(long_word)
        assert len(trie) == 1
        assert long_word in trie
        assert trie.starts_with("a" * 500) is True