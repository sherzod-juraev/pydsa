"""Greedy algorithms.

Provides classic greedy solutions: Activity Selection, Job Sequencing,
Fractional Knapsack, and Huffman Coding.
"""

import heapq
from collections import Counter
from collections.abc import Sequence
from typing import Self

from ..linear import Stack


def activity_selection(start: Sequence[int], finish: Sequence[int], /) -> list[int]:
    """
    Select the maximum number of non-overlapping activities.

    Uses a greedy algorithm that always picks the activity with the
    earliest finish time. Runs in O(n log n) due to sorting.

    Parameters
    ----------
    start : Sequence[int]
        Start times of activities.
    finish : Sequence[int]
        Finish times of activities.

    Returns
    -------
    list[int]
        Indices of selected activities, sorted by finish time.

    Raises
    ------
    ValueError
        If ``start`` and ``finish`` have different lengths.

    Examples
    --------
    >>> activity_selection([1, 3, 0, 5, 8, 5], [2, 4, 6, 7, 9, 9])
    [0, 1, 3, 4]
    """
    if len(start) != len(finish):
        raise ValueError("start and finish must have the same length")
    n = len(start)
    if n == 0:
        return []
    sorted_idx = sorted(range(n), key=lambda i: finish[i])
    selected = [sorted_idx[0]]
    last_finish = finish[sorted_idx[0]]
    for i in range(1, n):
        idx = sorted_idx[i]
        if last_finish <= start[idx]:
            selected.append(idx)
            last_finish = finish[idx]
    return selected


def job_sequencing(deadlines: Sequence[int], profits: Sequence[int], /) -> list[int]:
    """
    Schedule jobs with deadlines to maximize total profit.

    Uses a greedy algorithm that sorts jobs by descending profit
    and assigns each to the latest available slot before its
    deadline. Runs in O(n²) time.

    Parameters
    ----------
    deadlines : Sequence[int]
        Deadline for each job (1-based).
    profits : Sequence[int]
        Profit for each job.

    Returns
    -------
    list[int]
        Indices of selected jobs that yield maximum profit.

    Raises
    ------
    ValueError
        If ``deadlines`` and ``profits`` have different lengths.
    """
    if len(deadlines) != len(profits):
        raise ValueError("deadlines and profits must have the same length")
    n = len(deadlines)
    if n == 0:
        return []
    sorted_idx = sorted(range(n), key=lambda i: profits[i], reverse=True)
    max_deadline = max(deadlines)
    slots: list[int | None] = [None] * max_deadline
    for idx in sorted_idx:
        for t in range(deadlines[idx] - 1, -1, -1):
            if slots[t] is None:
                slots[t] = idx
                break
    return [idx for idx in slots if idx is not None]


def fractional_knapsack(
    weights: Sequence[float], prices: Sequence[float], capacity: float, /
) -> tuple[float, float]:
    """
    Solve the Fractional Knapsack problem greedily.

    Items can be divided arbitrarily. Greedy strategy picks items
    in descending order of price-to-weight ratio (unit value).
    Runs in O(n log n) due to sorting.

    Parameters
    ----------
    weights : Sequence[float]
        Weights of items.
    prices : Sequence[float]
        Prices (values) of items.
    capacity : float
        Maximum weight capacity.

    Returns
    -------
    tuple
        ``(total_weight, total_price)`` — the total weight and
        total price achieved by the greedy selection.

    Raises
    ------
    ValueError
        If ``weights`` and ``prices`` have different lengths.
    """
    if len(weights) != len(prices):
        raise ValueError("weights and prices must have the same length")
    n = len(weights)
    if n == 0:
        return (0.0, 0.0)
    total_price = 0.0
    total_weight = 0.0
    unit_prices = [prices[i] / weights[i] for i in range(n)]
    sorted_idx = sorted(range(n), key=lambda i: unit_prices[i], reverse=True)
    for idx in sorted_idx:
        if capacity <= 0:
            break
        amount = min(weights[idx], capacity)
        total_price += amount * unit_prices[idx]
        capacity -= amount
        total_weight += amount
    return total_weight, total_price


class Node:
    """Internal node for the Huffman coding tree.

    Not intended for direct use outside :func:`huffman_coding`.
    """

    def __init__(
        self,
        char: str | None,
        freq: int,
        left: Self | None = None,
        right: Self | None = None,
    ) -> None:
        """Initialize a node with a character (or None for internal nodes) and frequency."""
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: Self) -> bool:
        """Compare nodes by frequency for priority queue sorting (<)."""
        return self.freq < other.freq

    def __le__(self, other: Self) -> bool:
        """Compare nodes by frequency (<=)."""
        return self.freq <= other.freq

    def __gt__(self, other: Self) -> bool:
        """Compare nodes by frequency (>)."""
        return self.freq > other.freq

    def __ge__(self, other: Self) -> bool:
        """Compare nodes by frequency (>=)."""
        return self.freq >= other.freq

    def __add__(self, other: Self) -> "Node":
        """Combine two nodes into a parent node with their combined frequency."""
        return Node(char=None, freq=self.freq + other.freq, left=self, right=other)


def huffman_coding(text: str, /) -> tuple[str, dict[str, str]]:
    """
    Build Huffman codes and encode text using a greedy frequency-based tree.

    Constructs an optimal prefix code by repeatedly merging the two
    lowest-frequency nodes. Uses a custom min-heap (``heapq``) and
    iterative tree traversal via ``Stack``.

    Parameters
    ----------
    text : str
        Input text to encode.

    Returns
    -------
    tuple[str, dict[str, str]]
        ``(encoded_text, codes)`` — the Huffman-encoded binary string
        and a dictionary mapping each character to its code.

    Notes
    -----
    - For single-character text, returns ``"0"`` repeated.
    - For empty text, returns ``("", {})``.
    """
    if not text:
        return "", {}
    frequencies = Counter(text)
    if len(frequencies) == 1:
        char = list(frequencies.keys())[0]
        return "0" * len(text), {char: "0"}
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left_node = heapq.heappop(heap)
        right_node = heapq.heappop(heap)
        parent_node = left_node + right_node
        heapq.heappush(heap, parent_node)

    root = heap[0]
    codes = {}
    stack: Stack[tuple[Node, str]] = Stack()
    stack.push((root, ""))

    while not stack.is_empty():
        current_node, current_path = stack.pop()

        if current_node.char is not None:
            codes[current_node.char] = current_path
            continue
        if current_node.right is not None:
            stack.push((current_node.right, current_path + "1"))
        if current_node.left is not None:
            stack.push((current_node.left, current_path + "0"))

    encoded_text = "".join(codes[char] for char in text)
    return encoded_text, codes
