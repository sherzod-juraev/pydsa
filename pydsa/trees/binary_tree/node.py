from typing import Any


class Node:

    def __init__(self, value: Any) -> None:

        self.value = value
        self.left = None
        self.right = None