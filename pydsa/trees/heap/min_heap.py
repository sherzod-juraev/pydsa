from ..._types import Comparable
from ...exc import EmptyError


class MinHeap[T: Comparable]:
    """
    A binary min-heap implemented with a dynamic array.

    The heap is a complete binary tree where every parent node is
    less than or equal to its children. The minimum element is always
    at the root (index 0), accessible in O(1) time.

    .. csv-table:: Array Index Relations (0-based)
       :header: "Relation", "Formula"
       :widths: 20, 20

       "parent", "(i - 1) // 2"
       "left child", "2 * i + 1"
       "right child", "2 * i + 2"

    .. csv-table:: Heap Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 15, 10

       "insert", "O(log n)", "O(1)"
       "extract_min/max", "O(log n)", "O(1)"
       "peek", "O(1)", "O(1)"
       "heapify", "O(n)", "O(n)"
       "extract_all", "O(n log n)", "O(n)"
       "__contains__", "O(n)", "O(1)"

    Notes
    -----
    - Uses Floyd's linear-time algorithm for ``heapify``.
    - ``extract_all`` empties the heap and returns elements in sorted
      ascending order (heap sort).
    - For a max-heap, see ``MaxHeap``.
    """

    def __init__(self) -> None:

        self.__data: list[T]= []

    def __len__(self) -> int:
        """Return the number of elements. O(1)."""
        return len(self.__data)

    def __bool__(self) -> bool:
        """Return True if the heap is not empty. O(1)."""
        return len(self) > 0

    def __contains__(self, item: T) -> bool:
        """Return True if the value exists in the heap. O(n)."""
        return item in self.__data

    def is_empty(self) -> bool:
        """Return True if the heap has no elements. O(1)."""
        return len(self) == 0

    def peek(self) -> T:
        """Return the minimum value without removing it. O(1).

        Raises
        ------
        EmptyError
            If the heap is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        return self.__data[0]

    def insert(self, value: T, /) -> None:
        """Insert a value into the heap. O(log n).

        The value is appended to the end of the array and bubbled up
        until the min-heap invariant is restored.
        """
        self.__data.append(value)
        self.__shift_up()

    def extract_min(self) -> T:
        """Remove and return the minimum value. O(log n).

        The root is swapped with the last element, removed, and the
        new root is bubbled down to restore the invariant.

        Raises
        ------
        EmptyError
            If the heap is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        root = self.__data[0]
        self.__swap(0, len(self) - 1)
        del self.__data[-1]
        self.__shift_down()
        return root

    def extract_all(self) -> list[T]:
        """Remove all elements and return them in sorted ascending order. O(n log n).

        This empties the heap. Equivalent to performing heap sort.

        Returns
        -------
        list
            Values sorted from smallest to largest.
        """
        n = len(self)
        sorted_arr: list[T] = []
        for _ in range(n):
            sorted_arr.append(self.extract_min())
        return sorted_arr

    def heapify(self, arr: list[T], /) -> None:
        """Build a heap from an existing list in O(n) time.

        Uses Floyd's algorithm: starting from the last non-leaf node
        and calling ``__shift_down`` on each parent up to the root.

        Parameters
        ----------
        arr : list
            The list from which to build the heap. A copy is made.
        """
        self.__data = arr.copy()
        n = len(self)
        for i in range(n // 2 - 1, -1, -1):
            self.__shift_down(i)

    def __shift_up(self) -> None:
        """Bubble the last element up to its correct position."""
        child = len(self) - 1
        while child > 0:
            parent = (child - 1) // 2
            if self.__data[child] >= self.__data[parent]:
                break
            self.__swap(parent, child)
            child = parent

    def __shift_down(self, parent: int = 0, /) -> None:
        """Bubble the element at the given index down to its correct position."""
        n = len(self)
        while True:
            left: int = parent * 2 + 1
            right: int = parent * 2 + 2
            smallest = parent
            if left < n and self.__data[left] < self.__data[smallest]:
                smallest = left
            if right < n and self.__data[right] < self.__data[smallest]:
                smallest = right
            if smallest == parent:
                break
            self.__swap(parent, smallest)
            parent = smallest

    def __swap(self, i: int, j: int, /) -> None:
        """Swap two elements by index."""
        self.__data[i], self.__data[j] = self.__data[j], self.__data[i]

    def clear(self) -> None:
        """Remove all elements from the heap. O(1)."""
        self.__data.clear()
