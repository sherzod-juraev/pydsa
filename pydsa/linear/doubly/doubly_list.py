from .node import Node
from typing import Self, Iterator, Any
from ...exc import Empty


class DoublyList:
    """
    A doubly linked list with head and tail pointers.

    Each node stores a value and references to both the next
    and previous nodes. Bidirectional traversal enables O(1)
    removals at both ends and optimized O(n/2) indexed access.

    Time Complexity Summary
    .. csv-table:: Doubly Linked List Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 10, 10

       "insert_first", "O(1)", "O(1)"
       "insert_last", "O(1)", "O(1)"
       "insert_at", "O(n)", "O(1)"
       "remove_first", "O(1)", "O(1)"
       "remove_last", "O(1)", "O(1)"
       "remove_at", "O(n)", "O(1)"
       "remove", "O(n)", "O(1)"
       "get_first", "O(1)", "O(1)"
       "get_last", "O(1)", "O(1)"
       "get_at", "O(n)", "O(1)"
       "index_of", "O(n)", "O(1)"
       "count", "O(n)", "O(1)"
       "reverse", "O(n)", "O(1)"
       "copy", "O(n)", "O(n)"
       "has_cycle", "O(n)", "O(1)"
       "middle", "O(n)", "O(1)"


    Notes
    -----
    Indexed access traverses from the nearer end, halving the
    worst-case path compared to a singly linked list.
"""

    def __init__(self) -> None:

        self.__head: Node | None = None
        self.__tail: Node | None = None
        self.__length: int = 0

    def __len__(self) -> int:
        """Return the number of elements. O(1)."""
        return self.__length

    def __bool__(self) -> bool:
        """Return True if the list is not empty. O(1)."""
        return self.__length > 0

    def __iter__(self) -> Iterator:
        """Yield each value from head to tail. O(n)."""
        current = self.__head
        while current:
            yield current.value
            current = current.next

    def __reversed__(self) -> Iterator:
        """Yield each value from tail to head. O(n)."""
        current = self.__tail
        while current:
            yield current.value
            current = current.prev

    def __getitem__(self, item) -> Any:
        """Return the value at the given index. O(n).

        Traverses from the nearer end. Supports negative indexing.

        Raises
        ------
        IndexError
            If the index is out of bounds.
        """
        item = self.__get_index(item)
        if item <= self.__length // 2:
            current = self.__head
            for _ in range(item):
                current = current.next
            return current.value
        else:
            current = self.__tail
            for _ in range(self.__length - 1 - item):
                current = current.prev
            return current.value

    def __contains__(self, item) -> bool:
        """Return True if the value exists in the list. O(n)."""
        for val in self:
            if item == val:
                return True
        return False

    def __get_index(self, index: int, /) -> int:
        """Normalize a possibly negative index to a valid positive index.

        Raises
        ------
        IndexError
            If the index is out of bounds.
        """
        if index < 0:
            index += self.__length
        if index < 0 or index >= self.__length:
            raise IndexError(
                f"{type(self).__name__} index {index} out of range "
                f"for length {self.__length}"
            )
        return index

    def is_empty(self) -> bool:
        """Return True if the list has no elements. O(1)."""
        return self.__length == 0

    def get_first(self) -> Any:
        """Return the value of the first element. O(1).

        Raises
        ------
        Empty
            If the list is empty.
        """
        if self.is_empty():
            raise Empty(self)
        return self.__head.value

    def get_last(self) -> Any:
        """Return the value of the last element. O(1).

        Raises
        ------
        Empty
            If the list is empty.
        """
        if self.is_empty():
            raise Empty(self)
        return self.__tail.value

    def get_at(self, index: int, /) -> Any:
        """Return the value at the specified index. O(n).

        Raises
        ------
        IndexError
            If the index is out of bounds.
        """
        return self[index]

    def insert_first(self, value: Any, /) -> None:
        """Insert a value at the head of the list. O(1)."""
        new_node = Node(value)
        if self.is_empty():
            self.__head = self.__tail = new_node
        else:
            new_node.next = self.__head
            self.__head.prev = new_node
            self.__head = new_node
        self.__length += 1

    def insert_last(self, value: Any, /) -> None:
        """Insert a value at the tail of the list. O(1)."""
        if self.is_empty():
            return self.insert_first(value)
        new_node = Node(value)
        new_node.prev = self.__tail
        self.__tail.next = new_node
        self.__tail = new_node
        self.__length += 1

    def insert_at(self, index: int, value: Any, /) -> None:
        """Insert a value at the specified index. O(n).

        Elements at and after the index are shifted to the right.
        Supports negative indexing. Inserting at ``index == len(self)``
        is equivalent to ``insert_last``.

        Raises
        ------
        IndexError
            If ``index < -len(self)`` or ``index > len(self)``.
        """
        if index < 0:
            index += self.__length
        if index < 0 or index > self.__length:
            raise IndexError(
                f"{type(self).__name__} index {index} out of range "
                f"for length {self.__length}"
            )
        if index == 0:
            return self.insert_first(value)
        elif index == self.__length:
            return self.insert_last(value)
        if index <= self.__length // 2:
            current = self.__head
            for _ in range(index):
                current = current.next
        else:
            current = self.__tail
            for _ in range(self.__length - 1 - index):
                current = current.prev
        new_node = Node(value)
        new_node.next = current
        new_node.prev = current.prev
        if current.prev:
            current.prev.next = new_node
        current.prev = new_node
        self.__length += 1

    def remove_first(self) -> Any:
        """Remove and return the first element. O(1).

        Raises
        ------
        Empty
            If the list is empty.
        """
        if self.is_empty():
            raise Empty(self)
        current = self.__head
        self.__head = self.__head.next
        current.next = None
        if self.__head is None:
            self.__tail = None
        else:
            self.__head.prev = None
        self.__length -= 1
        return current.value

    def remove_last(self) -> Any:
        """Remove and return the last element. O(1).

        Raises
        ------
        Empty
            If the list is empty.
        """
        if self.is_empty():
            raise Empty(self)
        if self.__length == 1:
            return self.remove_first()
        current = self.__tail
        self.__tail = self.__tail.prev
        self.__tail.next = None
        current.prev = None
        self.__length -= 1
        return current.value

    def remove_at(self, index: int, /) -> Any:
        """Remove and return the element at the specified index. O(n).

        Raises
        ------
        IndexError
            If the index is out of bounds.
        """
        index = self.__get_index(index)
        if index == 0:
            return self.remove_first()
        elif index == self.__length - 1:
            return self.remove_last()
        if index <= self.__length // 2:
            current = self.__head
            for _ in range(index):
                current = current.next
        else:
            current = self.__tail
            for _ in range(self.__length - 1 - index):
                current = current.prev
        current.next.prev = current.prev
        current.prev.next = current.next
        current.next, current.prev = None, None
        self.__length -= 1
        return current.value

    def remove(self, value: Any, /) -> bool:
        """Remove the first occurrence of value. Return True if found. O(n).

        Raises
        ------
        Empty
            If the list is empty.
        """
        if self.is_empty():
            raise Empty(self)
        if value == self.__head.value:
            self.remove_first()
            return True
        elif value == self.__tail.value:
            self.remove_last()
            return True
        current = self.__head.next
        while current is not None and current is not self.__tail:
            if current.value == value:
                current.next.prev = current.prev
                current.prev.next = current.next
                current.next, current.prev = None, None
                self.__length -= 1
                return True
            current = current.next
        return False


    def index_of(self, value: Any, /) -> int:
        """Return the index of the first occurrence, or -1 if not found. O(n)."""
        for ind, val in enumerate(self):
            if val == value:
                return ind
        return -1

    def count(self, value: Any, /) -> int:
        """Return the number of occurrences of value. O(n)."""
        count = 0
        for val in self:
            if val == value:
                count += 1
        return count

    def reverse(self) -> None:
        """Reverse the list in-place. O(n) time, O(1) space.

        Swaps ``next`` and ``prev`` pointers of each node and
        exchanges the head and tail references.
        """
        if self.__length <= 1:
            return
        current = self.__head
        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev
        self.__head, self.__tail = self.__tail, self.__head

    def copy(self) -> Self:
        """Return a shallow copy of the list. O(n) time, O(n) space."""
        new_list = DoublyList()
        if self.__length == 0:
            return new_list
        for val in self:
            new_list.insert_last(val)
        return new_list

    def clear(self) -> None:
        """Remove all elements from the list. O(1)."""
        self.__head = None
        self.__tail = None
        self.__length = 0

    def has_cycle(self) -> bool:
        """Return True if the list contains a cycle. O(n).

        Uses Floyd's cycle detection algorithm.
        """
        fast = self.__head
        slow = self.__head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                return True
        return False

    def middle(self) -> Any:
        """Return the value of the middle element. O(n).

        If the list has even length, returns a tuple of the two
        central elements ``(left, right)``.

        Raises
        ------
        Empty
            If the list is empty.
        """
        if self.is_empty():
            raise Empty(self)
        index = self.__length // 2
        is_even = self.__length % 2 == 0
        if self.__length % 2 == 0:
            index -= 1
        current = self.__head
        for _ in range(index):
            current = current.next
        if is_even:
            return current.value, current.next.value
        return current.value