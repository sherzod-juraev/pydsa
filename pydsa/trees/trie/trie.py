from collections.abc import Iterator

from ...linear import Stack
from .node import Node


class Trie:
    """
    A prefix tree (Trie) for efficient string storage and retrieval.

    Each node represents a single character. Words are stored as
    paths from the root to nodes marked with ``is_end=True``.
    Common prefixes are shared among words, reducing memory usage
    and enabling fast prefix-based queries.

    .. csv-table:: Time & Space Complexity
       :header: "Operation", "Time", "Space"
       :widths: 25, 15, 15

       "insert", "O(L)", "O(L)"
       "searching", "O(L)", "O(1)"
       "starts_with", "O(L)", "O(1)"
       "remove", "O(L)", "O(L)"
       "words_with_prefix", "O(P + L·K)", "O(P + L)"
       "all_words", "O(N·L)", "O(H)"
       "__contains__", "O(L)", "O(1)"
       "__len__", "O(1)", "O(1)"

    *P = length of prefix, K = number of matching words,
    N = total words, H = tree height*

    Notes
    -----
    - This is **not** a binary tree — each node has a dynamic
      number of children stored in a ``dict[str, Node]``.
    - ``words_with_prefix`` returns words in **alphabetical order**
      by iterating children in sorted order.
    - Duplicate insertions are silently ignored.
    - Removal cleans up unreachable branches but stops at nodes
      that are marked as end-of-word or have multiple children.
    """
    def __init__(self) -> None:

        self.__root: Node = Node()
        self.__size: int = 0

    def __len__(self) -> int:
        """Return the number of words. O(1)."""
        return self.__size

    def __bool__(self) -> bool:
        """Return True if there is at least one word. O(1)."""
        return len(self) > 0

    def __contains__(self, item: str) -> bool:
        """Return True if the exact word exists in the trie. O(L)."""
        current: Node = self.__root
        for char in item:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end

    def insert(self, word: str, /) -> None:
        """Insert a word into the trie. O(L).

        Duplicate insertions are silently ignored.

        Parameters
        ----------
        word : str
            The word to insert.
        """
        current: Node = self.__root
        for char in word:
            if char not in current.children:
                current.children[char] = Node()
            current = current.children[char]
        if not current.is_end:
            current.is_end = True
            self.__size += 1

    def search(self, word: str, /) -> bool:
        """Return True if the exact word exists. O(L)."""
        return word in self

    def starts_with(self, prefix: str, /) -> bool:
        """Return True if any word starts with the given prefix. O(L).

        Parameters
        ----------
        prefix : str
            The prefix to check.

        Returns
        -------
        bool
            True if at least one word has this prefix.
        """
        current: Node = self.__root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        return True

    def remove(self, word: str, /) -> bool:
        """Remove a word from the trie. O(L).

        Cleans up nodes that are no longer part of any word.
        Stops when encountering a node that is an end-of-word
        marker or has multiple children.

        Parameters
        ----------
        word : str
            The word to remove.

        Returns
        -------
        bool
            True if the word was found and removed, False otherwise.
        """
        current: Node = self.__root
        stack: Stack[tuple[Node, str]] = Stack()
        for char in word:
            if char not in current.children:
                return False
            stack.push((current, char))
            current = current.children[char]
        if not current.is_end:
            return False
        current.is_end = False
        self.__size -= 1
        if not current:
            while stack:
                node, char = stack.pop()
                if len(node) > 1 or node.is_end:
                    del node.children[char]
                    break
                del node.children[char]
        return True

    def words_with_prefix(self, prefix: str, /) -> Iterator[str]:
        """Yield all words that start with the given prefix. O(P + L·K).

        Words are yielded in alphabetical order.

        Parameters
        ----------
        prefix : str
            The prefix to searching for.

        Yields
        ------
        str
            Words starting with the prefix, in alphabetical order.

        Examples
        --------
        >>> list(trie.words_with_prefix("ca"))
        ['car', 'cat', 'cats']
        """
        current = self.__root
        for char in prefix:
            if char not in current.children:
                return
            current = current.children[char]
        stack: Stack[tuple[Node, str]] = Stack()
        stack.push((current, prefix))
        while stack:
            current, prefix = stack.pop()
            if current.is_end:
                yield prefix
            for char in sorted(current.children.keys(), reverse=True):
                stack.push((current.children[char], prefix + char))

    def all_words(self) -> Iterator[str]:
        """Yield all words in the trie in alphabetical order. O(N·L)."""
        return self.words_with_prefix("")

    def clear(self) -> None:
        """Remove all words from the trie. O(1)."""
        self.__root.children.clear()
        self.__size = 0
