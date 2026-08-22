from pydsa import Trie


def build_trie() -> Trie:
    trie = Trie()
    for w in ["car", "cat", "cats", "dog"]:
        trie.insert(w)
    return trie


class TestBasics:
    def test_new_trie_is_empty(self) -> None:
        trie = Trie()
        assert len(trie) == 0
        assert not trie

    def test_insert_and_contains(self) -> None:
        trie = Trie()
        trie.insert("cat")
        assert "cat" in trie
        assert "ca" not in trie  # prefix, not a full word

    def test_insert_duplicate_is_idempotent(self) -> None:
        trie = Trie()
        trie.insert("cat")
        trie.insert("cat")
        assert len(trie) == 1

    def test_shared_prefix_words_both_exist(self) -> None:
        trie = build_trie()
        assert "cat" in trie
        assert "cats" in trie
        assert len(trie) == 4


class TestSearchAndPrefix:
    def test_search_found_and_not_found(self) -> None:
        trie = build_trie()
        assert trie.search("cat") is True
        assert trie.search("ca") is False

    def test_starts_with(self) -> None:
        trie = build_trie()
        assert trie.starts_with("ca") is True
        assert trie.starts_with("xyz") is False

    def test_starts_with_full_word_prefix(self) -> None:
        trie = build_trie()
        assert trie.starts_with("cat") is True  # "cat" is itself a word and a prefix


class TestWordsWithPrefix:
    def test_alphabetical_order(self) -> None:
        trie = build_trie()
        assert list(trie.words_with_prefix("ca")) == ["car", "cat", "cats"]

    def test_no_matches(self) -> None:
        trie = build_trie()
        assert list(trie.words_with_prefix("xyz")) == []

    def test_all_words(self) -> None:
        trie = build_trie()
        assert list(trie.all_words()) == ["car", "cat", "cats", "dog"]


class TestRemove:
    def test_remove_existing_word(self) -> None:
        trie = build_trie()
        assert trie.remove("cat") is True
        assert "cat" not in trie
        assert "cats" in trie  # shared prefix survives

    def test_remove_missing_word(self) -> None:
        trie = Trie()
        assert trie.remove("ghost") is False

    def test_remove_shared_prefix_word_keeps_siblings(self) -> None:
        trie = build_trie()
        trie.remove("cats")
        assert "cat" in trie  # "cat" node still marks end-of-word
        assert "cats" not in trie

    def test_remove_cleans_up_dead_branch(self) -> None:
        trie = Trie()
        trie.insert("only")
        trie.remove("only")
        assert len(trie) == 0
        assert list(trie.all_words()) == []

    def test_remove_word_that_is_prefix_of_another(self) -> None:
        trie = Trie()
        trie.insert("cat")
        trie.insert("cats")
        trie.remove("cat")
        assert "cat" not in trie
        assert "cats" in trie


class TestClear:
    def test_clear(self) -> None:
        trie = build_trie()
        trie.clear()
        assert len(trie) == 0
        assert "car" not in trie