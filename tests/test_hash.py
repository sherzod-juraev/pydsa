import random
from collections.abc import Iterator

import pytest

from pydsa.core import BaseStructure
from pydsa.exc import InvalidValueError, KeyNotFoundError, PydsaError
from pydsa.hash import HashTable


def make(capacity: int = 8) -> HashTable[int, str]:
    return HashTable[int, str](capacity)


class TestConstruction:
    def test_new_table_is_empty(self) -> None:
        table = make()
        assert len(table) == 0
        assert not table

    def test_is_a_base_structure(self) -> None:
        assert isinstance(make(), BaseStructure)

    @pytest.mark.parametrize("capacity", [1, 2, 16, 1000])
    def test_accepts_positive_capacity(self, capacity: int) -> None:
        table = make(capacity)
        table[1] = "one"
        assert table[1] == "one"

    @pytest.mark.parametrize("capacity", [0, -1, -100])
    def test_rejects_non_positive_capacity(self, capacity: int) -> None:
        with pytest.raises(InvalidValueError):
            make(capacity)

    def test_invalid_capacity_error_names_the_value(self) -> None:
        with pytest.raises(InvalidValueError, match="-5"):
            make(-5)

    def test_invalid_capacity_is_also_a_value_error(self) -> None:
        with pytest.raises(ValueError):
            make(0)


class TestSizeAndTruthiness:
    def test_len_counts_distinct_keys(self) -> None:
        table = make()
        table[1] = "a"
        table[2] = "b"
        assert len(table) == 2

    def test_non_empty_table_is_truthy(self) -> None:
        table = make()
        table[1] = "a"
        assert table

    def test_table_becomes_falsy_again_after_last_removal(self) -> None:
        table = make()
        table[1] = "a"
        del table[1]
        assert not table

    def test_updating_a_key_does_not_change_len(self) -> None:
        table = make()
        table[1] = "a"
        table[1] = "b"
        assert len(table) == 1


class TestSetAndGet:
    def test_set_then_get(self) -> None:
        table = make()
        table[1] = "one"
        assert table[1] == "one"

    def test_update_replaces_value(self) -> None:
        table = make()
        table[1] = "one"
        table[1] = "uno"
        assert table[1] == "uno"

    def test_none_is_a_valid_value(self) -> None:
        table = HashTable[str, None](8)
        table["a"] = None
        assert table["a"] is None
        assert "a" in table
        assert len(table) == 1

    def test_falsy_keys_are_ordinary_keys(self) -> None:
        table = HashTable[object, int](8)
        table[0] = 1
        table[""] = 2
        table[None] = 3
        assert (table[0], table[""], table[None]) == (1, 2, 3)

    def test_tuple_keys(self) -> None:
        table = HashTable[tuple[int, int], str](8)
        table[(1, 2)] = "p"
        assert table[(1, 2)] == "p"
        assert (2, 1) not in table

    def test_equal_keys_with_equal_hashes_are_one_key(self) -> None:
        table = HashTable[object, str](8)
        table[1] = "int"
        table[1.0] = "float"
        table[True] = "bool"
        assert len(table) == 1
        assert table[1] == "bool"

    def test_distinct_values_for_distinct_keys(self) -> None:
        table = make()
        for i in range(5):
            table[i] = str(i)
        assert [table[i] for i in range(5)] == ["0", "1", "2", "3", "4"]


class TestMissingKey:
    def test_getitem_raises_key_not_found(self) -> None:
        with pytest.raises(KeyNotFoundError):
            make()[1]

    def test_error_is_catchable_as_key_error_and_pydsa_error(self) -> None:
        table = make()
        with pytest.raises(KeyError):
            table[1]
        with pytest.raises(PydsaError):
            table[1]

    def test_error_message_shows_the_repr_of_the_key(self) -> None:
        table = HashTable[str, int](8)
        with pytest.raises(KeyNotFoundError) as info:
            table["1"]
        assert str(info.value) == "Key '1' not found"

    def test_message_distinguishes_int_from_str_keys(self) -> None:
        table = HashTable[object, int](8)
        with pytest.raises(KeyNotFoundError) as as_int:
            table[1]
        with pytest.raises(KeyNotFoundError) as as_str:
            table["1"]
        assert str(as_int.value) != str(as_str.value)

    def test_lookup_in_a_populated_bucket_still_raises(self) -> None:
        table = make(8)
        table[1] = "one"
        with pytest.raises(KeyNotFoundError):
            table[9]  # same bucket as 1, different key


class TestUnhashableKeys:
    def test_every_operation_rejects_unhashable_keys(self) -> None:
        table = HashTable[object, int](8)
        with pytest.raises(TypeError):
            table[[1]] = 1
        with pytest.raises(TypeError):
            table[[1]]
        with pytest.raises(TypeError):
            [1] in table  # noqa: B015
        with pytest.raises(TypeError):
            table.remove([1])
        with pytest.raises(TypeError):
            table.get([1])
        assert len(table) == 0


class TestContains:
    def test_present_and_absent(self) -> None:
        table = make()
        table[1] = "one"
        assert 1 in table
        assert 2 not in table

    def test_values_are_not_keys(self) -> None:
        table = HashTable[object, int](8)
        table["a"] = 99
        assert 99 not in table

    def test_contains_is_false_after_delete(self) -> None:
        table = make()
        table[1] = "one"
        del table[1]
        assert 1 not in table

    def test_contains_does_not_insert(self) -> None:
        table = make()
        _ = 5 in table
        assert len(table) == 0


class TestGet:
    def test_existing_key(self) -> None:
        table = make()
        table[1] = "one"
        assert table.get(1) == "one"

    def test_missing_key_defaults_to_none(self) -> None:
        assert make().get(1) is None

    def test_missing_key_returns_given_default(self) -> None:
        assert make().get(1, "fallback") == "fallback"

    def test_default_is_ignored_when_key_exists(self) -> None:
        table = make()
        table[1] = "one"
        assert table.get(1, "fallback") == "one"

    def test_default_is_not_stored(self) -> None:
        table = make()
        table.get(1, "fallback")
        assert len(table) == 0
        assert 1 not in table

    def test_stored_none_is_not_replaced_by_default(self) -> None:
        table = HashTable[str, int | None](8)
        table["a"] = None
        assert table.get("a", 5) is None


class TestRemove:
    def test_returns_true_when_removed(self) -> None:
        table = make()
        table[1] = "one"
        assert table.remove(1) is True
        assert 1 not in table
        assert len(table) == 0

    def test_returns_false_when_missing(self) -> None:
        table = make()
        table[1] = "one"
        assert table.remove(2) is False
        assert len(table) == 1

    def test_second_removal_returns_false(self) -> None:
        table = make()
        table[1] = "one"
        table.remove(1)
        assert table.remove(1) is False
        assert len(table) == 0

    def test_removal_leaves_other_keys_alone(self) -> None:
        table = make()
        table[1] = "one"
        table[2] = "two"
        table.remove(1)
        assert table[2] == "two"

    def test_key_can_be_reinserted(self) -> None:
        table = make()
        table[1] = "one"
        table.remove(1)
        table[1] = "again"
        assert table[1] == "again"
        assert len(table) == 1


class TestDelItem:
    def test_deletes_the_key(self) -> None:
        table = make()
        table[1] = "one"
        del table[1]
        assert 1 not in table
        assert len(table) == 0

    def test_missing_key_raises_key_not_found(self) -> None:
        with pytest.raises(KeyNotFoundError):
            del make()[1]

    def test_missing_key_message_uses_repr(self) -> None:
        table = HashTable[str, int](8)
        with pytest.raises(KeyNotFoundError) as info:
            del table["x"]
        assert str(info.value) == "Key 'x' not found"

    def test_failed_delete_does_not_change_len(self) -> None:
        table = make()
        table[1] = "one"
        with pytest.raises(KeyNotFoundError):
            del table[2]
        assert len(table) == 1


class TestCollisions:
    # With capacity 8 and no rehash (3 keys / 8 buckets), 1, 9 and 17 share a bucket.
    KEYS = (1, 9, 17)

    def table(self) -> HashTable[int, str]:
        table = make(8)
        for key in self.KEYS:
            table[key] = f"v{key}"
        assert len({table._index(key) for key in self.KEYS}) == 1
        return table

    def test_all_colliding_keys_are_retrievable(self) -> None:
        table = self.table()
        assert [table[key] for key in self.KEYS] == ["v1", "v9", "v17"]
        assert len(table) == 3

    @pytest.mark.parametrize("victim", KEYS)
    def test_removing_any_chain_position_keeps_the_others(self, victim: int) -> None:
        table = self.table()
        del table[victim]
        assert victim not in table
        for key in self.KEYS:
            if key != victim:
                assert table[key] == f"v{key}"
        assert len(table) == 2

    @pytest.mark.parametrize("target", KEYS)
    def test_updating_any_chain_position_keeps_the_others(self, target: int) -> None:
        table = self.table()
        table[target] = "new"
        assert table[target] == "new"
        assert len(table) == 3
        for key in self.KEYS:
            if key != target:
                assert table[key] == f"v{key}"

    def test_missing_key_in_a_busy_bucket(self) -> None:
        table = self.table()
        assert 25 not in table
        assert table.get(25) is None
        assert table.remove(25) is False


class TestRehash:
    def test_entries_survive_growth(self) -> None:
        table = make(2)
        for i in range(100):
            table[i] = str(i)
        assert len(table) == 100
        assert all(table[i] == str(i) for i in range(100))

    def test_load_factor_exactly_at_threshold_does_not_grow(self) -> None:
        table = make(4)
        for key in (1, 5, 2):  # 3 / 4 == 0.75, not above it
            table[key] = "x"
        assert table._index(1) == table._index(5)

    def test_load_factor_above_threshold_doubles_capacity(self) -> None:
        table = make(4)
        for key in (1, 5, 2, 3):  # 4 / 4 > 0.75
            table[key] = "x"
        assert table._index(1) != table._index(5)  # 1 % 8 != 5 % 8
        assert table._index(3) == 3
        assert table._index(11) == 3  # 11 % 8, not 11 % 5 or 11 % 4

    def test_updating_an_existing_key_never_triggers_growth(self) -> None:
        table = make(4)
        for key in (1, 5, 2):
            table[key] = "x"
        for _ in range(10):
            table[1] = "y"
        assert table._index(1) == table._index(5)
        assert len(table) == 3

    def test_values_updated_before_growth_are_kept(self) -> None:
        table = make(2)
        table[1] = "old"
        table[1] = "new"
        for i in range(2, 50):
            table[i] = str(i)
        assert table[1] == "new"

    def test_growth_does_not_duplicate_or_drop_entries(self) -> None:
        table = make(1)
        for i in range(37):
            table[i] = str(i)
        assert sorted(table.keys()) == list(range(37))
        assert len(list(table.items())) == len(table) == 37

    def test_negative_and_large_keys(self) -> None:
        table = make(2)
        keys = [-7, -1, 0, 3, 10**12, -(10**12)]
        for key in keys:
            table[key] = str(key)
        assert all(table[key] == str(key) for key in keys)


class TestIteration:
    def test_iterators_are_lazy_generators(self) -> None:
        table = make()
        assert isinstance(table.keys(), Iterator)
        assert isinstance(table.values(), Iterator)
        assert isinstance(table.items(), Iterator)

    def test_keys_values_items(self) -> None:
        table = make()
        table[1] = "one"
        table[2] = "two"
        assert sorted(table.keys()) == [1, 2]
        assert sorted(table.values()) == ["one", "two"]
        assert sorted(table.items()) == [(1, "one"), (2, "two")]

    def test_empty_table_yields_nothing(self) -> None:
        table = make()
        assert list(table.keys()) == []
        assert list(table.values()) == []
        assert list(table.items()) == []

    def test_each_entry_appears_once(self) -> None:
        table = make(2)
        for i in range(30):
            table[i] = str(i)
        assert len(list(table.keys())) == 30
        assert len(set(table.keys())) == 30

    def test_keys_values_items_are_aligned(self) -> None:
        table = make(2)
        for i in range(20):
            table[i] = str(i)
        assert list(table.items()) == list(zip(table.keys(), table.values(), strict=True))

    def test_items_reflect_updates_and_removals(self) -> None:
        table = make()
        table[1] = "one"
        table[2] = "two"
        table[1] = "uno"
        del table[2]
        assert list(table.items()) == [(1, "uno")]

    def test_colliding_keys_are_all_iterated(self) -> None:
        table = make(8)
        for key in (1, 9, 17):
            table[key] = str(key)
        assert sorted(table.keys()) == [1, 9, 17]


class TestClear:
    def test_clear_empties_the_table(self) -> None:
        table = make()
        table[1] = "one"
        table[2] = "two"
        table.clear()
        assert len(table) == 0
        assert not table
        assert 1 not in table
        assert list(table.items()) == []

    def test_clear_on_empty_table_is_harmless(self) -> None:
        table = make()
        table.clear()
        assert len(table) == 0

    def test_table_is_reusable_after_clear(self) -> None:
        table = make()
        table[1] = "one"
        table.clear()
        table[1] = "again"
        assert table[1] == "again"
        assert len(table) == 1

    def test_table_is_reusable_after_growth_and_clear(self) -> None:
        table = make(2)
        for i in range(50):
            table[i] = str(i)
        table.clear()
        assert len(table) == 0
        for i in range(50):
            table[i] = "z"
        assert len(table) == 50
        assert all(table[i] == "z" for i in range(50))

    def test_clear_leaves_no_stale_keys_behind(self) -> None:
        table = make()
        table[1] = "one"
        table.clear()
        with pytest.raises(KeyNotFoundError):
            table[1]


class TestAgainstDict:
    @pytest.mark.parametrize("seed", range(8))
    @pytest.mark.parametrize("capacity", [1, 3, 16])
    def test_random_operations_match_dict(self, seed: int, capacity: int) -> None:
        rng = random.Random(seed)
        table = make(capacity)
        model: dict[int, str] = {}
        for step in range(400):
            key = rng.randrange(-30, 30)
            action = rng.choice(("set", "set", "del", "remove", "get", "clear"))
            if action == "set":
                table[key] = str(step)
                model[key] = str(step)
            elif action == "del":
                if key in model:
                    del table[key]
                    del model[key]
                else:
                    with pytest.raises(KeyNotFoundError):
                        del table[key]
            elif action == "remove":
                assert table.remove(key) is (key in model)
                model.pop(key, None)
            elif action == "get":
                assert table.get(key) == model.get(key)
            elif step % 50 == 0:
                table.clear()
                model.clear()
            assert len(table) == len(model)
        assert dict(table.items()) == model
        assert sorted(table.keys()) == sorted(model)
