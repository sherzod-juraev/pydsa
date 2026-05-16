from ..trees import MinHeap


def heap_sort(arr: list, /) -> list:
    """
    Sort a list using heap sort. O(n log n) time, O(n) space.

    Builds a min-heap from the input array using Floyd's O(n)
    heapify algorithm, then repeatedly extracts the minimum
    element to produce a sorted list in ascending order.

    Parameters
    ----------
    arr : list
        Input list.

    Returns
    -------
    list
        Sorted copy of the input list.
    Notes
    -----
    - **Stable**: No — heap operations do not preserve relative order
      of equal elements.
    - **In-place**: No — ``extract_all`` builds a new list.
    - Uses the custom ``MinHeap`` class with O(n) heapify and
      O(n log n) total extraction.
    - Performs consistently in O(n log n) regardless of input
      distribution, making it a reliable worst-case performer.
    """
    min_heap = MinHeap()
    min_heap.heapify(arr)
    return min_heap.extract_all()