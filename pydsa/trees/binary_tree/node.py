from typing import TypeVar

T = TypeVar("T")

class Node[T]:
    def __init__(self, value: T) -> None:
        self.value: T = value
        self.left: Node[T] | None = None
        self.right: Node[T] | None = None
