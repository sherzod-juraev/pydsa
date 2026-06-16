from collections.abc import Iterator
from typing import TypeVar, cast

from ...exc import EmptyError
from .node import Node

T = TypeVar("T")

class SinglyList[T]:
    """
    A singly linked list with head and tail pointers.

    Each node stores a value and a reference to the next node.
    The list maintains constant-time access to both ends, enabling
    O(1) insertions and removals at the head and tail.

    Time Complexity Summary
    .. csv-table:: Linked List Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 10, 10

       "insert_first", "O(1)", "O(1)"
       "insert_last", "O(1)", "O(1)"
       "insert_at", "O(n)", "O(1)"
       "remove_first", "O(1)", "O(1)"
       "remove_last", "O(n)", "O(1)"
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
    """

    def __init__(self) -> None:

        self.__head: Node[T] | None = None
        self.__tail: Node[T] | None = None
        self.__length: int = 0

    def __len__(self) -> int:
        """Return the number of elements. O(1)."""
        return self.__length

    def __bool__(self) -> bool:
        """Return True if the list is not empty. O(1)."""
        return self.__length > 0

    def __iter__(self) -> Iterator[T]:
        """Yield each value in order from head to tail. O(n)."""
        current = self.__head
        while current:
            yield current.value
            current = current.next

    def __getitem__(self, item: int) -> T:
        """Return the value at the given index. Supports negative indexing. O(n)."""
        item = self.__get_index(item)
        current = cast(Node[T], self.__head)
        for _ in range(item):
            current = cast(Node[T], current.next)
        return current.value

    def __contains__(self, item: T) -> bool:
        """Return True if the value exists in the list. O(n)."""
        return any(val == item for val in self)

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
        return self.__head is None and self.__tail is None

    def get_first(self) -> T:
        """Return the value of the first element. O(1).

        Raises
        ------
        EmptyError
            If the list is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        current = cast(Node[T], self.__head)
        return current.value

    def get_last(self) -> T:
        """Return the value of the last element. O(1).

        Raises
        ------
        EmptyError
            If the list is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        return self[-1]

    def get_at(self, index: int, /) -> T:
        """Return the value at the specified index. O(n).

        Raises
        ------
        IndexError
            If the index is out of bounds.
        """
        return self[index]

    def insert_first(self, value: T, /) -> None:
        """Insert a value at the head of the list. O(1)."""
        new_node = Node(value)
        new_node.next = self.__head
        self.__head = new_node
        if self.__tail is None:
            self.__tail = new_node
        self.__length += 1

    def insert_last(self, value: T, /) -> None:
        """Insert a value at the tail of the list. O(1)."""
        if self.is_empty():
            return self.insert_first(value)
        new_node = Node(value)
        tail = cast(Node[T], self.__tail)
        tail.next = new_node
        self.__tail = new_node
        self.__length += 1

    def insert_at(self, index: int, value: T, /) -> None:
        """Insert a value at the specified index. O(n).

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
        current = cast(Node[T], self.__head)
        for _ in range(index - 1):
            current = cast(Node[T], current.next)
        new_node = Node(value)
        new_node.next = current.next
        current.next = new_node
        self.__length += 1

    def remove_first(self) -> T:
        """Remove and return the first element. O(1).

        Raises
        ------
        EmptyError
            If the list is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        current = cast(Node[T], self.__head)
        self.__head = current.next
        if self.__head is None:
            self.__tail = None
        self.__length -= 1
        return current.value

    def remove_last(self) -> T:
        """Remove and return the last element. O(n).

        Raises
        ------
        EmptyError
            If the list is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        if self.__length == 1:
            return self.remove_first()
        current = cast(Node[T], self.__head)
        while current is not None and current.next != self.__tail:
            current = cast(Node[T], current.next)
        last_node = cast(Node[T], self.__tail)
        current.next = None
        self.__tail = current
        self.__length -= 1
        return last_node.value

    def remove_at(self, index: int, /) -> T:
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
        current = cast(Node[T], self.__head)
        for _ in range(index - 1):
            current = cast(Node[T], current.next)
        remove_node = cast(Node[T], current.next)
        current.next = remove_node.next
        remove_node.next = None
        self.__length -= 1
        return remove_node.value

    def remove(self, value: T, /) -> bool:
        """Remove the first occurrence of value. Return True if found. O(n).

        Raises
        ------
        EmptyError
            If the list is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        head = cast(Node[T], self.__head)
        tail = cast(Node[T], self.__tail)
        if head.value == value:
            self.remove_first()
            return True
        elif tail.value == value:
            self.remove_last()
            return True
        current = head
        while current is not self.__tail:
            current.next = cast(Node[T], current.next)
            if current.next.value == value:
                remove_node = current.next
                current.next = remove_node.next
                remove_node.next = None
                self.__length -= 1
                return True
            current = current.next
        return False

    def index_of(self, value: T, /) -> int:
        """Return the index of the first occurrence, or -1 if not found. O(n)."""
        for ind, val in enumerate(self):
            if value == val:
                return ind
        return -1

    def count(self, value: T, /) -> int:
        """Return the number of occurrences of value. O(n)."""
        count = 0
        for val in self:
            if value == val:
                count += 1
        return count

    def reverse(self) -> None:
        """Reverse the list in-place. O(n) time, O(1) space."""
        old_head = self.__head
        prev = None
        current = self.__head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.__head = prev
        self.__tail = old_head


    def copy(self) -> 'SinglyList[T]':
        """Return a shallow copy of the list. O(n) time, O(n) space."""
        new_list = SinglyList[T]()
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
        """Return True if the list contains a cycle. Uses Floyd's algorithm. O(n)."""
        fast = cast(Node[T], self.__head)
        slow = cast(Node[T], self.__head)
        while fast and fast.next:
            fast = cast(Node[T], fast.next.next)
            slow = cast(Node[T], slow.next)
            if fast == slow:
                return True
        return False

    def middle(self) -> T | tuple[T, T]:
        """Return the value of the middle element.

        If the list has even length, returns a tuple (left, right).
        O(n).

        Raises
        ------
        EmptyError
            If the list is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        index = self.__length // 2
        is_even = self.__length % 2 == 0
        if self.__length % 2 == 0:
            index -= 1
        current = cast(Node[T], self.__head)
        for _ in range(index):
            current = cast(Node[T], current.next)
        if is_even:
            next_node = cast(Node[T], current.next)
            return current.value, next_node.value
        return current.value
