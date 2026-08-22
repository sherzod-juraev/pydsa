import pytest

from pydsa import (
    coin_change,
    edit_distance,
    fib_memo,
    fib_tab,
    knapsack_tab,
    lcs_tab,
)


class TestFibMemo:
    def test_base_cases(self) -> None:
        assert fib_memo(0) == 0
        assert fib_memo(1) == 1

    def test_known_value(self) -> None:
        assert fib_memo(10) == 55

    def test_matches_tabulation(self) -> None:
        for n in range(20):
            assert fib_memo(n) == fib_tab(n)


class TestFibTab:
    def test_base_cases(self) -> None:
        assert fib_tab(0) == 0
        assert fib_tab(1) == 1

    def test_known_value(self) -> None:
        assert fib_tab(10) == 55


class TestKnapsackTab:
    def test_basic_selection(self) -> None:
        weights = [1, 3, 4, 5]
        prices = [1, 4, 5, 7]
        assert knapsack_tab(weights, prices, 7) == [1, 2]

    def test_zero_capacity(self) -> None:
        assert knapsack_tab([1, 2, 3], [10, 20, 30], 0) == []

    def test_empty_items(self) -> None:
        assert knapsack_tab([], [], 10) == []

    def test_mismatched_lengths_raises(self) -> None:
        with pytest.raises(ValueError):
            knapsack_tab([1, 2], [1, 2, 3], 5)

    def test_capacity_exceeds_all_weights(self) -> None:
        # every item should fit — selection is all indices
        weights = [1, 2, 3]
        prices = [10, 20, 30]
        assert knapsack_tab(weights, prices, 100) == [0, 1, 2]


class TestLcsTab:
    def test_known_value(self) -> None:
        assert lcs_tab("ABCBDAB", "BDCABA") == "BCBA"

    def test_identical_strings(self) -> None:
        assert lcs_tab("hello", "hello") == "hello"

    def test_no_common_subsequence(self) -> None:
        assert lcs_tab("abc", "xyz") == ""

    def test_empty_strings(self) -> None:
        assert lcs_tab("", "") == ""
        assert lcs_tab("abc", "") == ""


class TestCoinChange:
    def test_known_value(self) -> None:
        assert sorted(coin_change([1, 2, 5], 11)) == [1, 5, 5]

    def test_zero_amount(self) -> None:
        assert coin_change([1, 2, 5], 0) == []

    def test_impossible_amount(self) -> None:
        assert coin_change([5, 10], 3) == []

    def test_uses_fewest_coins(self) -> None:
        result = coin_change([1, 3, 4], 6)
        assert len(result) == 2  # 3+3, not 1+1+4 or six 1s


class TestEditDistance:
    def test_known_value(self) -> None:
        assert edit_distance("kitten", "sitting") == 3

    def test_identical_strings(self) -> None:
        assert edit_distance("abc", "abc") == 0

    def test_one_empty_string(self) -> None:
        assert edit_distance("abc", "") == 3
        assert edit_distance("", "abc") == 3

    def test_both_empty(self) -> None:
        assert edit_distance("", "") == 0