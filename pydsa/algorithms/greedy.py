import numpy as np
from typing import Self
from collections import Counter
from ..linear import Stack
import heapq


def activity_selection(start: np.ndarray, finish: np.ndarray, ) -> np.ndarray:
    """
    Select the maximum number of non-overlapping activities.

    Uses a greedy algorithm that always picks the activity with the
    earliest finish time. Runs in O(n log n) due to sorting.

    Parameters
    ----------
    start : np.ndarray
        Start times of activities.
    finish : np.ndarray
        Finish times of activities.

    Returns
    -------
    np.ndarray
        Indices of selected activities, sorted by finish time.

    Raises
    ------
    ValueError
        If ``start`` and ``finish`` have different shapes.
    """
    if start.shape != finish.shape:
        raise ValueError('Shapes does not match')
    if start.shape[0] == 0:
        return np.array([])
    sorted_idx = np.argsort(finish)
    selected = []
    selected.append(sorted_idx[0])
    n = sorted_idx.shape[0]
    last_finish = finish[sorted_idx[0]]
    for i in range(1, n):
        if last_finish <= start[sorted_idx[i]]:
            selected.append(sorted_idx[i])
            last_finish = finish[sorted_idx[i]]
    return np.array(selected)


def job_sequencing(deadlines: np.ndarray, profits: np.ndarray, /) -> np.ndarray:
    """
    Schedule jobs with deadlines to maximize total profit.

    Uses a greedy algorithm that sorts jobs by descending profit
    and assigns each to the latest available slot before its
    deadline. Runs in O(n²) time.

    Parameters
    ----------
    deadlines : np.ndarray
        Deadline for each job (1-based).
    profits : np.ndarray
        Profit for each job.

    Returns
    -------
    np.ndarray
        Indices of selected jobs that yield maximum profit.

    Raises
    ------
    ValueError
        If ``deadlines`` and ``profits`` have different shapes.
    """
    if deadlines.shape != profits.shape:
        raise ValueError('Shapes does not match')
    if deadlines.shape[0] == 0:
        return np.array([], dtype=int)
    sorted_idx = np.argsort(profits)[::-1]
    max_deadline = np.max(deadlines)
    slots = np.full(max_deadline, -1, dtype=int)
    for idx in sorted_idx:
        for t in range(deadlines[idx] - 1, -1, -1):
            if slots[t] == -1:
                slots[t] = idx
                break
    selected_jobs = slots[slots != -1]
    return selected_jobs


def fractional_knapsack(weights: np.ndarray, prices: np.ndarray, capacity: int, /) -> tuple:
    """
    Solve the Fractional Knapsack problem greedily.

    Items can be divided arbitrarily. Greedy strategy picks items
    in descending order of price-to-weight ratio (unit value).
    Runs in O(n log n) due to sorting.

    Parameters
    ----------
    weights : np.ndarray
        Weights of items.
    prices : np.ndarray
        Prices (values) of items.
    capacity : int
        Maximum weight capacity.

    Returns
    -------
    tuple
        ``(total_weight, total_price)`` — the total weight and
        total price achieved by the greedy selection.

    Raises
    ------
    ValueError
        If ``weights`` and ``prices`` have different shapes.
    """
    if weights.shape != prices.shape:
        raise ValueError('Shapes does not match')
    if weights.shape[0] == 0:
        return (0, 0)
    total_price = 0
    total_weight = 0
    unit_prices = prices / weights
    sorted_idx = np.argsort(unit_prices)[::-1]
    n = sorted_idx.shape[0]
    for idx in sorted_idx:
        if capacity <= 0:
            break
        amount = min(weights[idx], capacity)
        total_price += amount * unit_prices[idx]
        capacity -= amount
        total_weight += amount
    return total_weight, total_price


class Node:
    """Internal node for Huffman coding tree."""
    def __init__(
            self,
            char: str | None,
            freq: int,
            left: Self | None = None,
            right: Self | None = None
    ):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: Self) -> bool:
        return self.freq < other.freq

    def __le__(self, other: Self) -> bool:
        return self.freq <= other.freq

    def __gt__(self, other: Self) -> bool:
        return self.freq > other.freq

    def __ge__(self, other: Self) -> bool:
        return self.freq >= other.freq

    def __add__(self, other: Self) -> Self:
        return Node(
            char=None,
            freq=self.freq + other.freq,
            left=self,
            right=other
        )


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
    stack = Stack()
    stack.push((root, ""))

    while not stack.is_empty():
        current_node, current_path = stack.pop()

        if current_node is None:
            continue
        if current_node.char is not None:
            codes[current_node.char] = current_path
            continue
        if current_node.right is not None:
            stack.push((current_node.right, current_path + "1"))
        if current_node.left is not None:
            stack.push((current_node.left, current_path + "0"))

    encoded_text = "".join(codes[char] for char in text)
    return encoded_text, codes