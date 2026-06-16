from typing import TypeVar

T = TypeVar("T")

class Node[T]:

    def __init__(self, value: T) -> None:

        self.value: T = value
        self.next: Node[T] | None = None
        self.prev: Node[T] | None = None
