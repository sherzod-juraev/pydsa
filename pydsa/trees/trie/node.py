class Node:

    def __init__(self) -> None:

        self.children: dict[str, Node] = {}
        self.is_end: bool = False

    def __len__(self) -> int:

        return len(self.children)

    def __bool__(self) -> bool:

        return len(self) > 0
