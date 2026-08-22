"""Dynamic programming algorithms.

Provides classic DP solutions: Fibonacci (memoized and tabulated),
0/1 Knapsack, Longest Common Subsequence, Coin Change, and Levenshtein
edit distance.
"""

import math
from collections.abc import Sequence


def fib_memo(n: int, memo: dict[int, int] | None = None, /) -> int:
    """
    Compute the n-th Fibonacci number using memoization (top-down DP).

    Caches previously computed values in a dictionary to avoid
    redundant recursive calls. Runs in O(n) time and O(n) space.

    Parameters
    ----------
    n : int
        The index of the Fibonacci number (0-based).
    memo : dict | None, optional
        Internal memoization dictionary (do not pass manually).

    Returns
    -------
    int
        The n-th Fibonacci number.

    Examples
    --------
    >>> fib_memo(10)
    55
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_tab(n: int, /) -> int:
    """
    Compute the n-th Fibonacci number using tabulation (bottom-up DP).

    Builds the solution iteratively from the base cases upward,
    using only O(1) extra space. Runs in O(n) time.

    Parameters
    ----------
    n : int
        The index of the Fibonacci number (0-based).

    Returns
    -------
    int
        The n-th Fibonacci number.

    Examples
    --------
    >>> fib_tab(10)
    55
    """
    if n <= 1:
        return n
    prev2 = 0
    prev1 = 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1


def knapsack_tab(weights: Sequence[int], prices: Sequence[int], capacity: int, /) -> list[int]:
    """
    Solve the 0/1 Knapsack problem using tabulation (bottom-up DP).

    Given item weights and prices, finds the subset of items that
    maximizes total price without exceeding the weight capacity.
    Returns the indices of the selected items.

    Parameters
    ----------
    weights : Sequence[int]
        Item weights.
    prices : Sequence[int]
        Item prices.
    capacity : int
        Maximum weight capacity.

    Returns
    -------
    list[int]
        Indices of items selected for the optimal solution.

    Raises
    ------
    ValueError
        If ``weights`` and ``prices`` have different lengths.

    Examples
    --------
    >>> knapsack_tab([1, 3, 4, 5], [1, 4, 5, 7], 7)
    [1, 2]
    """
    if len(weights) != len(prices):
        raise ValueError("weights and prices must have the same length")
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            if weights[i - 1] <= j:
                take = prices[i - 1] + dp[i - 1][j - weights[i - 1]]
                skip = dp[i - 1][j]
                dp[i][j] = max(take, skip)
            else:
                dp[i][j] = dp[i - 1][j]
    i = n
    w = capacity
    selected_items: list[int] = []
    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]
        i -= 1
    return selected_items[::-1]


def lcs_tab(s1: str, s2: str, /) -> str:
    """
    Compute the Longest Common Subsequence (LCS) of two strings.

    Uses bottom-up DP to build the LCS table, then backtracks
    to reconstruct the actual subsequence. O(m×n) time and space.

    Parameters
    ----------
    s1 : str
        First string.
    s2 : str
        Second string.

    Returns
    -------
    str
        The longest common subsequence.

    Examples
    --------
    >>> lcs_tab("ABCBDAB", "BDCABA")
    'BCBA'
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    i, j = m, n
    word = ""
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            word = s1[i - 1] + word
            i -= 1
            j -= 1
        elif dp[i][j - 1] <= dp[i - 1][j]:
            i -= 1
        else:
            j -= 1
    return word


def coin_change(coins: Sequence[int], amount: int, /) -> list[int]:
    """
    Solve the Coin Change problem (fewest coins) using bottom-up DP.

    Given coin denominations and a target amount, returns the
    combination of coins that uses the fewest total coins.
    If the amount cannot be formed, returns an empty list.

    Parameters
    ----------
    coins : Sequence[int]
        Coin denominations.
    amount : int
        Target amount to form.

    Returns
    -------
    list[int]
        Coins used in the optimal solution, or empty list if impossible.

    Examples
    --------
    >>> sorted(coin_change([1, 2, 5], 11))
    [1, 5, 5]
    """
    dp: list[float] = [math.inf] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for cur_amount in range(coin, amount + 1):
            dp[cur_amount] = min(dp[cur_amount], dp[cur_amount - coin] + 1)
    if dp[amount] == math.inf:
        return []
    selected_coins: list[int] = []
    while amount > 0:
        for coin in coins:
            if coin <= amount and dp[amount] == dp[amount - coin] + 1:
                selected_coins.append(coin)
                amount -= coin
                break
    return selected_coins[::-1]


def edit_distance(s1: str, s2: str, /) -> int:
    """
    Compute the Levenshtein edit distance between two strings.

    Uses bottom-up DP to find the minimum number of insertions,
    deletions, and substitutions required to transform ``s1``
    into ``s2``. O(m×n) time and space.

    Parameters
    ----------
    s1 : str
        Source string.
    s2 : str
        Target string.

    Returns
    -------
    int
        Minimum edit distance.

    Examples
    --------
    >>> edit_distance("kitten", "sitting")
    3
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(m + 1):
        dp[i][0] = i
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                insert = dp[i][j - 1] + 1
                delete = dp[i - 1][j] + 1
                replace = dp[i - 1][j - 1] + 1
                dp[i][j] = min(insert, delete, replace)
    return dp[m][n]
