import pytest
from pydsa import HashTable


class TestHashTableInit:
    """__init__"""

    def test_empty_table_has_zero_length(self):
        ht = HashTable(8)
        assert len(ht) == 0

    def test_empty_table_is_falsy(self):
        ht = HashTable(8)
        assert not ht


class TestHashTableSetItem:
    """__setitem__"""

    def test_insert_single_pair(self):
        ht = HashTable(8)
        ht["name"] = "Sherzod"
        assert len(ht) == 1

    def test_insert_multiple_pairs(self):
        ht = HashTable(8)
        for i in range(10):
            ht[f"key{i}"] = i
        assert len(ht) == 10

    def test_update_existing_key(self):
        ht = HashTable(8)
        ht["age"] = 25
        ht["age"] = 26
        assert len(ht) == 1
        assert ht["age"] == 26

    def test_insert_triggers_rehash(self):
        ht = HashTable(4)  # capacity 4
        for i in range(10):
            ht[f"key{i}"] = i
        assert len(ht) == 10
        # all keys accessible after rehash
        for i in range(10):
            assert ht[f"key{i}"] == i

    def test_collision_handling(self):
        ht = HashTable(4)
        ht["a"] = 1
        ht["b"] = 2
        ht["c"] = 3
        ht["d"] = 4
        ht["e"] = 5
        assert ht["a"] == 1
        assert ht["b"] == 2
        assert ht["c"] == 3
        assert ht["d"] == 4
        assert ht["e"] == 5


class TestHashTableGetItem:
    """__getitem__"""

    def test_get_existing_key(self):
        ht = HashTable(8)
        ht["name"] = "Sherzod"
        assert ht["name"] == "Sherzod"

    def test_get_non_existing_raises_keyerror(self):
        ht = HashTable(8)
        with pytest.raises(KeyError):
            _ = ht["missing"]

    def test_get_after_update(self):
        ht = HashTable(8)
        ht["x"] = 100
        ht["x"] = 200
        assert ht["x"] == 200


class TestHashTableDelItem:
    """__delitem__"""

    def test_delete_existing_key(self):
        ht = HashTable(8)
        ht["name"] = "Sherzod"
        del ht["name"]
        assert len(ht) == 0
        assert "name" not in ht

    def test_delete_non_existing_raises_keyerror(self):
        ht = HashTable(8)
        with pytest.raises(KeyError):
            del ht["missing"]

    def test_delete_after_collision(self):
        ht = HashTable(4)
        for i in range(5):
            ht[f"key{i}"] = i
        del ht["key2"]
        assert "key2" not in ht
        assert len(ht) == 4
        # other keys still accessible
        for i in [0, 1, 3, 4]:
            assert ht[f"key{i}"] == i


class TestHashTableRemove:
    """remove"""

    def test_remove_existing_key(self):
        ht = HashTable(8)
        ht["name"] = "Sherzod"
        assert ht.remove("name") is True
        assert len(ht) == 0

    def test_remove_non_existing_key(self):
        ht = HashTable(8)
        assert ht.remove("missing") is False
        assert len(ht) == 0

    def test_remove_after_collision(self):
        ht = HashTable(4)
        for i in range(5):
            ht[f"key{i}"] = i
        assert ht.remove("key1") is True
        assert "key1" not in ht
        assert len(ht) == 4


class TestHashTableContains:
    """__contains__"""

    def test_contains_existing(self):
        ht = HashTable(8)
        ht["hello"] = "world"
        assert "hello" in ht

    def test_contains_non_existing(self):
        ht = HashTable(8)
        assert "world" not in ht

    def test_contains_empty_table(self):
        ht = HashTable(8)
        assert "anything" not in ht


class TestHashTableGet:
    """get"""

    def test_get_existing(self):
        ht = HashTable(8)
        ht["name"] = "Sherzod"
        assert ht.get("name") == "Sherzod"

    def test_get_non_existing_returns_none(self):
        ht = HashTable(8)
        assert ht.get("missing") is None

    def test_get_with_default(self):
        ht = HashTable(8)
        assert ht.get("missing", 42) == 42

    def test_get_with_default_none(self):
        ht = HashTable(8)
        ht["key"] = None
        assert ht.get("key", 42) is None  # None is the value, not default


class TestHashTableKeys:
    """keys"""

    def test_keys_empty(self):
        ht = HashTable(8)
        assert list(ht.keys()) == []

    def test_keys_returns_all(self):
        ht = HashTable(8)
        ht["a"] = 1
        ht["b"] = 2
        ht["c"] = 3
        assert sorted(ht.keys()) == ["a", "b", "c"]


class TestHashTableValues:
    """values"""

    def test_values_empty(self):
        ht = HashTable(8)
        assert list(ht.values()) == []

    def test_values_returns_all(self):
        ht = HashTable(8)
        ht["a"] = 1
        ht["b"] = 2
        ht["c"] = 3
        assert sorted(ht.values()) == [1, 2, 3]


class TestHashTableItems:
    """items"""

    def test_items_empty(self):
        ht = HashTable(8)
        assert list(ht.items()) == []

    def test_items_returns_all(self):
        ht = HashTable(8)
        ht["a"] = 1
        ht["b"] = 2
        assert sorted(ht.items()) == [("a", 1), ("b", 2)]


class TestHashTableClear:
    """clear"""

    def test_clear_empties_table(self):
        ht = HashTable(8)
        ht["a"] = 1
        ht["b"] = 2
        ht.clear()
        assert len(ht) == 0
        assert not ht

    def test_clear_empty_table(self):
        ht = HashTable(8)
        ht.clear()
        assert len(ht) == 0


class TestHashTableRehash:
    """rehash behavior"""

    def test_rehash_doubles_capacity(self):
        ht = HashTable(4)
        for i in range(10):
            ht[f"key{i}"] = i
        assert len(ht) == 10
        for i in range(10):
            assert ht[f"key{i}"] == i

    def test_rehash_preserves_all_data(self):
        ht = HashTable(2)
        keys = [f"k{i}" for i in range(20)]
        for k in keys:
            ht[k] = k
        for k in keys:
            assert ht[k] == k
        assert len(ht) == 20


class TestHashTableLoadFactor:
    """load factor"""

    def test_load_factor_empty(self):
        ht = HashTable(8)
        assert ht.check_load() is False

    def test_load_factor_after_inserts(self):
        ht = HashTable(4)
        ht["a"] = 1
        ht["b"] = 2
        assert ht.check_load() is False  # 2/4 = 0.5
        ht["c"] = 3
        assert ht.check_load() is False  # 3/4 = 0.75 (<=)
        ht["d"] = 4
        # 4/4 = 1.0 before rehash, but rehash triggers
        assert len(ht) == 4


class TestHashTableDifferentKeyTypes:
    """Various key types"""

    def test_string_keys(self):
        ht = HashTable(8)
        ht["hello"] = "world"
        assert ht["hello"] == "world"

    def test_int_keys(self):
        ht = HashTable(8)
        ht[42] = "answer"
        assert ht[42] == "answer"

    def test_float_keys(self):
        ht = HashTable(8)
        ht[3.14] = "pi"
        assert ht[3.14] == "pi"

    def test_tuple_keys(self):
        ht = HashTable(8)
        ht[(1, 2)] = "point"
        assert ht[(1, 2)] == "point"

    def test_mixed_keys(self):
        ht = HashTable(8)
        ht["str"] = 1
        ht[42] = 2
        ht[3.14] = 3
        ht[(1, 2)] = 4
        assert ht["str"] == 1
        assert ht[42] == 2
        assert ht[3.14] == 3
        assert ht[(1, 2)] == 4


class TestHashTableBool:
    """__bool__"""

    def test_non_empty_is_truthy(self):
        ht = HashTable(8)
        ht["a"] = 1
        assert bool(ht)

    def test_empty_is_falsy(self):
        ht = HashTable(8)
        assert not ht


class TestHashTableLen:
    """__len__"""

    def test_len_updates(self):
        ht = HashTable(8)
        assert len(ht) == 0
        ht["a"] = 1
        assert len(ht) == 1
        ht["b"] = 2
        assert len(ht) == 2
        del ht["a"]
        assert len(ht) == 1


class TestHashTableLargeData:
    """Large data"""

    def test_many_inserts(self):
        ht = HashTable(16)
        n = 1000
        for i in range(n):
            ht[f"key{i}"] = i
        assert len(ht) == n
        for i in range(n):
            assert ht[f"key{i}"] == i

    def test_many_updates(self):
        ht = HashTable(16)
        ht["counter"] = 0
        for i in range(1, 501):
            ht["counter"] = i
        assert ht["counter"] == 500

    def test_many_inserts_and_deletes(self):
        ht = HashTable(16)
        for i in range(100):
            ht[f"key{i}"] = i
        for i in range(50):
            del ht[f"key{i}"]
        assert len(ht) == 50
        for i in range(50, 100):
            assert ht[f"key{i}"] == i