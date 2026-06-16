from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Entry[K, V]:
    def __init__(self, key: K, value: V) -> None:

        self.key: K = key
        self.value: V = value
