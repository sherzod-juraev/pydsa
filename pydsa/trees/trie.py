"""Trie (prefix tree) implementation.

Provides :class:`Trie`, a prefix tree for efficient string storage, exact-match
search and prefix queries.
"""

from collections.abc import Iterator

from ..core import BaseStructure
from ..linear import Stack


class _TrieNode:
    """A trie node holding child references and an end-of-word marker.

    Attributes
    ----------
    children : dict
        The child nodes, keyed by the character that leads to them.
    is_end : bool
        True if the path from the root to this node spells a stored word.
    """

    def __init__(self) -> None:
        """Initialize a node with no children that does not end a word."""
        self.children: dict[str, _TrieNode] = {}
        self.is_end: bool = False


class Trie(BaseStructure):
    """A prefix tree (Trie) for efficient string storage and retrieval.

    Each node represents a single character. Words are stored as paths from the
    root to nodes marked as the end of a word. Common prefixes are shared among
    words, which reduces memory usage and makes prefix queries fast.

    Time Complexity Summary

    .. csv-table:: Time & Space Complexity
       :header: "Operation", "Time", "Space"
       :widths: 25, 15, 15

       "insert", "O(L)", "O(L)"
       "search", "O(L)", "O(1)"
       "starts_with", "O(L)", "O(1)"
       "remove", "O(L)", "O(L)"
       "words_with_prefix", "O(P + L·K)", "O(P + L)"
       "all_words", "O(N·L)", "O(H)"
       "__contains__", "O(L)", "O(1)"
       "__len__", "O(1)", "O(1)"

    *L = length of the word, P = length of the prefix, K = number of matching
    words, N = total words, H = tree height*

    Notes
    -----
    - This is **not** a binary tree: each node has a dynamic number of children,
      stored in a ``dict`` keyed by character.
    - ``words_with_prefix`` and ``all_words`` return words in **alphabetical
      order** (by code point) by visiting the children in sorted order.
    - Duplicate insertions are silently ignored.
    - The empty string is a valid word. It is stored at the root.
    - Removal deletes the branch that no word uses any more, and stops at the
      first node that ends another word or has other children.
    """

    def __init__(self) -> None:
        """Initialize an empty trie."""
        self._root: _TrieNode = _TrieNode()
        self._size: int = 0

    def __len__(self) -> int:
        """Return the number of words. O(1)."""
        return self._size

    def __contains__(self, item: str) -> bool:
        """Return True if the exact word exists in the trie. O(L)."""
        current = self._root
        for char in item:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end

    def clear(self) -> None:
        """Remove all words from the trie. O(1)."""
        self._root = _TrieNode()
        self._size = 0

    def insert(self, word: str, /) -> None:
        """Insert a word into the trie. O(L).

        Duplicate insertions are silently ignored.

        Parameters
        ----------
        word : str
            The word to insert.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("cat")
        >>> "cat" in trie
        True
        """
        current = self._root
        for char in word:
            if char not in current.children:
                current.children[char] = _TrieNode()
            current = current.children[char]
        if not current.is_end:
            current.is_end = True
            self._size += 1

    def search(self, word: str, /) -> bool:
        """Return True if the exact word exists. O(L).

        Parameters
        ----------
        word : str
            The word to look for.

        Returns
        -------
        bool
            True if the word was inserted, False otherwise. A prefix of a stored
            word is not a word itself.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("cat")
        >>> trie.search("cat")
        True
        >>> trie.search("ca")
        False
        """
        return word in self

    def starts_with(self, prefix: str, /) -> bool:
        """Return True if any word starts with the given prefix. O(L).

        Every word starts with the empty prefix, so it matches exactly when the
        trie is not empty.

        Parameters
        ----------
        prefix : str
            The prefix to check.

        Returns
        -------
        bool
            True if at least one word has this prefix.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("cat")
        >>> trie.starts_with("ca")
        True
        >>> trie.starts_with("dog")
        False
        """
        current = self._root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end or bool(current.children)

    def remove(self, word: str, /) -> bool:
        """Remove a word from the trie. O(L).

        Cleans up the nodes that no word uses any more. The cleanup stops at the
        first node that ends another word or has other children, so words that
        share a prefix with the removed one are kept.

        Parameters
        ----------
        word : str
            The word to remove.

        Returns
        -------
        bool
            True if the word was found and removed, False otherwise. A prefix of
            a stored word is not a word and is not removed.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("cat")
        >>> trie.remove("cat")
        True
        >>> "cat" in trie
        False
        """
        current = self._root
        path: Stack[tuple[_TrieNode, str]] = Stack()
        for char in word:
            if char not in current.children:
                return False
            path.push((current, char))
            current = current.children[char]
        if not current.is_end:
            return False
        current.is_end = False
        self._size -= 1
        if not current.children:
            while path:
                parent, char = path.pop()
                del parent.children[char]
                if parent.children or parent.is_end:
                    break
        return True

    def words_with_prefix(self, prefix: str, /) -> Iterator[str]:
        """Yield all words that start with the given prefix. O(P + L·K).

        Words are yielded in alphabetical order. The prefix itself comes first if
        it is a word. Changing the trie while iterating gives undefined results.

        Parameters
        ----------
        prefix : str
            The prefix to search for.

        Yields
        ------
        str
            Words starting with the prefix, in alphabetical order.

        Examples
        --------
        >>> trie = Trie()
        >>> for w in ["car", "cat", "cats", "dog"]:
        ...     trie.insert(w)
        >>> list(trie.words_with_prefix("ca"))
        ['car', 'cat', 'cats']
        """
        start = self._root
        for char in prefix:
            if char not in start.children:
                return
            start = start.children[char]
        pending: Stack[tuple[_TrieNode, str]] = Stack()
        pending.push((start, prefix))
        while pending:
            node, word = pending.pop()
            if node.is_end:
                yield word
            for char in sorted(node.children, reverse=True):
                pending.push((node.children[char], word + char))

    def all_words(self) -> Iterator[str]:
        """Yield all words in the trie in alphabetical order. O(N·L).

        Returns
        -------
        Iterator
            Every stored word, in alphabetical order.
        """
        return self.words_with_prefix("")
