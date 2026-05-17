import numpy as np


def fib_memo(n: int, memo: dict | None = None, /) -> int:
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
    """
    if n <= 1:
        return n
    prev2 = 0
    prev1 = 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1


def knapsack_tab(weights: np.ndarray, prices: np.ndarray, capacity: int, /) -> np.ndarray:
    """
    Solve the 0/1 Knapsack problem using tabulation (bottom-up DP).

    Given item weights and prices, finds the subset of items that
    maximizes total price without exceeding the weight capacity.
    Returns the indices of the selected items.

    Parameters
    ----------
    weights : np.ndarray
        1D array of item weights.
    prices : np.ndarray
        1D array of item prices.
    capacity : int
        Maximum weight capacity.

    Returns
    -------
    np.ndarray
        Indices of items selected for the optimal solution.

    Raises
    ------
    ValueError
        If ``weights`` and ``prices`` have different shapes.
    """
    if weights.shape != prices.shape:
        raise ValueError('shape does not match')
    dp = np.full((weights.shape[0] + 1, capacity + 1), 0, dtype=int)
    for i in range(1, weights.shape[0] + 1):
        for j in range(1, capacity + 1):
            if weights[i - 1] <= j:
                take = prices[i - 1] + dp[i - 1][j - weights[i - 1]]
                skip = dp[i - 1][j]
                dp[i][j] = max(take, skip)
            else:
                dp[i][j] = dp[i - 1][j]
    i = dp.shape[0] - 1
    w = capacity
    selected_items = []
    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]
        i -= 1
    return np.array(selected_items)[::-1]


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
    """
    dp = np.full((len(s1) + 1, len(s2) + 1), 0, dtype=int)
    for i in range(1, dp.shape[0]):
        for j in range(1, dp.shape[1]):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    i = dp.shape[0] - 1
    j = dp.shape[1] - 1
    word = ''
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


def coin_change(coins: np.ndarray, amount, /) -> np.ndarray:
    """
    Solve the Coin Change problem (fewest coins) using bottom-up DP.

    Given coin denominations and a target amount, returns the
    combination of coins that uses the fewest total coins.
    If the amount cannot be formed, returns an empty array.

    Parameters
    ----------
    coins : np.ndarray
        1D array of coin denominations.
    amount : int
        Target amount to form.

    Returns
    -------
    np.ndarray
        Coins used in the optimal solution, or empty array if impossible.
    """
    dp = np.full(amount + 1, np.inf, dtype=float)
    dp[0] = 0
    for coin in coins:
        for cur_amount in range(coin, amount + 1):
            dp[cur_amount] = min(dp[cur_amount], dp[cur_amount - coin] + 1)
    if dp[amount] == np.inf:
        return np.array([])
    selected_coins = []
    i = coins.shape[0] - 1
    while 0 < amount:
        for coin in coins:
            if coin <= amount and dp[amount] == dp[amount - coin] + 1:
                selected_coins.append(coin)
                amount -= coin
                break
    return np.array(selected_coins)[::-1]


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
    """
    dp = np.full((len(s1) + 1, len(s2) + 1), 0, dtype=int)
    dp[0] = np.arange(len(s2) + 1)
    dp[:, 0] = np.arange(len(s1) + 1)
    for i in range(1, dp.shape[0]):
        for j in range(1, dp.shape[1]):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                insert = dp[i][j - 1] + 1
                delete = dp[i - 1][j] + 1
                replace = dp[i - 1][j - 1] + 1
                dp[i][j] = min(insert, delete, replace)
    return dp[-1][-1]