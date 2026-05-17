import numpy as np
import pytest
from pydsa import (
    fib_memo,
    fib_tab,
    knapsack_tab,
    lcs_tab,
    coin_change,
    edit_distance,
)


class TestFibMemo:
    """fib_memo"""

    def test_base_cases(self):
        assert fib_memo(0) == 0
        assert fib_memo(1) == 1

    def test_small_values(self):
        assert fib_memo(2) == 1
        assert fib_memo(3) == 2
        assert fib_memo(4) == 3
        assert fib_memo(5) == 5
        assert fib_memo(6) == 8

    def test_larger_value(self):
        assert fib_memo(20) == 6765

    def test_high_value(self):
        assert fib_memo(50) == 12586269025

    def test_memo_reuse(self):
        memo = {}
        fib_memo(10, memo)
        assert 10 in memo
        assert memo[10] == 55


class TestFibTab:
    """fib_tab"""

    def test_base_cases(self):
        assert fib_tab(0) == 0
        assert fib_tab(1) == 1

    def test_small_values(self):
        assert fib_tab(5) == 5
        assert fib_tab(10) == 55

    def test_large_value(self):
        assert fib_tab(50) == 12586269025

    def test_matches_memo(self):
        for n in range(20):
            assert fib_tab(n) == fib_memo(n)


class TestKnapsack:
    """knapsack_tab"""

    def test_simple_case(self):
        weights = np.array([2, 3, 4, 5], dtype=int)
        prices = np.array([3, 4, 5, 6], dtype=int)
        result = knapsack_tab(weights, prices, 5)
        assert np.sum(prices[result]) == 7  # items 0 and 1 (3+4=7)

    def test_single_item_fits(self):
        weights = np.array([3], dtype=int)
        prices = np.array([10], dtype=int)
        result = knapsack_tab(weights, prices, 5)
        assert list(result) == [0]
        assert np.sum(prices[result]) == 10

    def test_single_item_too_heavy(self):
        weights = np.array([10], dtype=int)
        prices = np.array([5], dtype=int)
        result = knapsack_tab(weights, prices, 5)
        assert len(result) == 0

    def test_all_items_fit(self):
        weights = np.array([1, 2, 3], dtype=int)
        prices = np.array([10, 20, 30], dtype=int)
        result = knapsack_tab(weights, prices, 10)
        assert list(result) == [0, 1, 2]
        assert np.sum(prices[result]) == 60

    def test_large_capacity(self):
        weights = np.array([1, 2, 3], dtype=int)
        prices = np.array([1, 2, 3], dtype=int)
        result = knapsack_tab(weights, prices, 100)
        assert list(result) == [0, 1, 2]

    def test_empty_arrays(self):
        weights = np.array([], dtype=int)
        prices = np.array([], dtype=int)
        result = knapsack_tab(weights, prices, 10)
        assert len(result) == 0

    def test_zero_capacity(self):
        weights = np.array([1, 2, 3], dtype=int)
        prices = np.array([10, 20, 30], dtype=int)
        result = knapsack_tab(weights, prices, 0)
        assert len(result) == 0

    def test_exact_fit(self):
        weights = np.array([5, 5, 5], dtype=int)
        prices = np.array([10, 20, 30], dtype=int)
        result = knapsack_tab(weights, prices, 10)
        assert np.sum(prices[result]) == 50

    def test_shape_mismatch_raises(self):
        with pytest.raises(ValueError):
            knapsack_tab(np.array([1, 2]), np.array([1, 2, 3]), 5)

    def test_classic_case(self):
        weights = np.array([10, 20, 30], dtype=int)
        prices = np.array([60, 100, 120], dtype=int)
        result = knapsack_tab(weights, prices, 50)
        assert np.sum(prices[result]) == 220


class TestLCS:
    """lcs_tab"""

    def test_empty_strings(self):
        assert lcs_tab("", "") == ""
        assert lcs_tab("abc", "") == ""
        assert lcs_tab("", "abc") == ""

    def test_no_common(self):
        assert lcs_tab("abc", "xyz") == ""

    def test_identical(self):
        assert lcs_tab("hello", "hello") == "hello"

    def test_common_subsequence(self):
        assert lcs_tab("abcdef", "acf") == "acf"

    def test_multiple_lcs(self):
        result = lcs_tab("abc", "bac")
        assert result in ["ac", "bc"]

    def test_long_strings(self):
        s1 = "AGGTAB"
        s2 = "GXTXAYB"
        assert lcs_tab(s1, s2) == "GTAB"


class TestCoinChange:
    """coin_change"""

    def test_exact_change(self):
        coins = np.array([1, 5, 10, 25], dtype=int)
        result = coin_change(coins, 30)
        assert np.sum(result) == 30

    def test_single_coin(self):
        coins = np.array([7], dtype=int)
        result = coin_change(coins, 14)
        assert list(result) == [7, 7]

    def test_impossible(self):
        coins = np.array([2, 4], dtype=int)
        result = coin_change(coins, 5)
        assert len(result) == 0

    def test_minimum_coins(self):
        coins = np.array([1, 2, 5], dtype=int)
        result = coin_change(coins, 11)
        assert len(result) == 3  # 5+5+1

    def test_zero_amount(self):
        coins = np.array([1, 2, 5], dtype=int)
        result = coin_change(coins, 0)
        assert len(result) == 0

    def test_large_amount(self):
        coins = np.array([1, 5, 10, 25, 50], dtype=int)
        result = coin_change(coins, 99)
        assert np.sum(result) == 99


class TestEditDistance:
    """edit_distance"""

    def test_identical(self):
        assert edit_distance("abc", "abc") == 0

    def test_empty_strings(self):
        assert edit_distance("", "") == 0
        assert edit_distance("abc", "") == 3
        assert edit_distance("", "abc") == 3

    def test_single_substitution(self):
        assert edit_distance("cat", "cut") == 1

    def test_insertion(self):
        assert edit_distance("cat", "cats") == 1

    def test_deletion(self):
        assert edit_distance("cats", "cat") == 1

    def test_kitten_sitting(self):
        assert edit_distance("kitten", "sitting") == 3

    def test_sunday_saturday(self):
        assert edit_distance("sunday", "saturday") == 3