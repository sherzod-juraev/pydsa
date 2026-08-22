import pytest

from pydsa import HashTable


class TestBasics:
    def test_set_and_get(self) -> None:
        ht = HashTable[str, int](capacity=16)
        ht["age"] = 25
        assert ht["age"] == 25

    def test_update_existing_key(self) -> None:
        ht = HashTable[str, int](capacity=16)
        ht["age"] = 25
        ht["age"] = 26
        assert ht["age"] == 26
        assert len(ht) == 1  # update, not a new entry

    def test_getitem_missing_key_raises(self) -> None:
        ht = HashTable[str, int](capacity=16)
        with pytest.raises(KeyError):
            _ = ht["missing"]

    def test_contains(self) -> None:
        ht = HashTable[str, int](capacity=16)
        ht["age"] = 25
        assert "age" in ht
        assert "missing" not in ht

    def test_len_and_bool(self) -> None:
        ht = HashTable[str, int](capacity=16)
        assert len(ht) == 0
        assert not ht
        ht["a"] = 1
        assert len(ht) == 1
        assert ht


class TestDeletion:
    def test_delitem(self) -> None:
        ht = HashTable[str, int](capacity=16)
        ht["age"] = 25
        del ht["age"]
        assert "age" not in ht

    def test_delitem_missing_key_raises(self) -> None:
        ht = HashTable[str, int](capacity=16)
        with pytest.raises(KeyError):
            del ht["missing"]

    def test_remove_returns_true_when_found(self) -> None:
        ht = HashTable[str, int](capacity=16)
        ht["age"] = 25
        assert ht.remove("age") is True

    def test_remove_returns_false_when_missing(self) -> None:
        ht = HashTable[str, int](capacity=16)
        assert ht.remove("missing") is False


class TestGetWithDefault:
    def test_get_existing(self) -> None:
        ht = HashTable[str, int](capacity=16)
        ht["age"] = 25
        assert ht.get("age") == 25

    def test_get_missing_returns_default(self) -> None:
        ht = HashTable[str, int](capacity=16)
        assert ht.get("missing", 0) == 0

    def test_get_missing_no_default_returns_none(self) -> None:
        ht = HashTable[str, int](capacity=16)
        assert ht.get("missing") is None


class TestCollisions:
    def test_collision_handling(self) -> None:
        # capacity=1 forces every key into the same bucket
        ht = HashTable[str, int](capacity=1)
        ht["a"] = 1
        ht["b"] = 2
        ht["c"] = 3
        assert ht["a"] == 1
        assert ht["b"] == 2
        assert ht["c"] == 3
        assert len(ht) == 3


class TestRehashing:
    def test_rehash_triggers_past_load_factor(self) -> None:
        ht = HashTable[int, int](capacity=4)
        for i in range(10):
            ht[i] = i * 10
        # all entries must survive rehashing regardless of new capacity
        for i in range(10):
            assert ht[i] == i * 10
        assert len(ht) == 10


class TestIteration:
    def test_keys_values_items(self) -> None:
        ht = HashTable[str, int](capacity=16)
        ht["a"] = 1
        ht["b"] = 2
        assert set(ht.keys()) == {"a", "b"}
        assert set(ht.values()) == {1, 2}
        assert set(ht.items()) == {("a", 1), ("b", 2)}

    def test_iteration_on_empty_table(self) -> None:
        ht = HashTable[str, int](capacity=16)
        assert list(ht.keys()) == []
        assert list(ht.values()) == []
        assert list(ht.items()) == []


class TestClear:
    def test_clear(self) -> None:
        ht = HashTable[str, int](capacity=16)
        ht["a"] = 1
        ht.clear()
        assert len(ht) == 0
        assert "a" not in ht