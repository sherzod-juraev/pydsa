from typing import Any


class Node:

    def __init__(self, value: Any) -> None:

        self.value: Any = value
        self.left: Node | None = None
        self.right: Node | None = None
        self.height: int = 1