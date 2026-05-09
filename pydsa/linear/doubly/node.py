from typing import Any


class Node:

    def __init__(self, value: Any) -> None:

        self.value = value
        self.next = None
        self.prev = None