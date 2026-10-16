"""Adjacency-list graph.

Provides :class:`Graph`, a directed or undirected graph of string-labelled
vertices with BFS and DFS traversal and reachability queries.
"""

from collections.abc import Iterator

from .core import BaseStructure
from .exc import InvalidValueError, KeyNotFoundError
from .linear import Queue, Stack


class Graph(BaseStructure):
    """A directed or undirected graph stored as an adjacency list.

    Vertices are strings. Each vertex maps to the list of its neighbours in
    insertion order, which makes traversal order deterministic. Parallel edges are
    never stored: adding an existing edge again does nothing.

    Time Complexity Summary

    .. csv-table:: Graph Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 30, 30, 15

       "add_vertex", "O(1)", "O(1)"
       "add_edge", "O(deg(u) + deg(v))", "O(1)"
       "remove_vertex", "O(V + E) directed, O(E) undirected", "O(1)"
       "remove_edge", "O(deg(u) + deg(v))", "O(1)"
       "vertices", "O(V)", "O(1)"
       "edges", "O(V + E)", "O(1)"
       "neighbors", "O(deg(v))", "O(1)"
       "degree", "O(1)", "O(1)"
       "bfs", "O(V + E)", "O(V)"
       "dfs", "O(V + E)", "O(V)"
       "has_path", "O(V + E)", "O(V)"
       "is_connected", "O(V + E)", "O(V)"
       "__contains__", "O(1)", "O(1)"
       "__len__", "O(1)", "O(1)"

    Neighbour lists are plain lists, so checking or removing one edge scans the
    list, which is why edge operations depend on the degree.

    Notes
    -----
    - ``len(graph)`` is the number of vertices, so a graph with vertices but no
      edges is truthy.
    - In an undirected graph an edge is stored in both directions, and
      :meth:`edges` reports it twice. A self-loop is stored and reported once.
    - :meth:`bfs` and :meth:`dfs` are generators: a missing start vertex is
      reported when iteration begins, not when the method is called.
    - :meth:`neighbors` is lenient and yields nothing for an unknown vertex, while
      :meth:`degree` raises.
    - :meth:`is_connected` is defined for undirected graphs only.

    Examples
    --------
    >>> graph = Graph(directed=False)
    >>> graph.add_edge("A", "B")
    >>> graph.add_edge("B", "C")
    >>> len(graph)
    3
    >>> list(graph.bfs("A"))
    ['A', 'B', 'C']
    >>> graph.has_path("A", "C")
    True
    >>> graph.is_connected()
    True
    """

    def __init__(self, directed: bool = True) -> None:
        """Create an empty graph.

        Parameters
        ----------
        directed : bool, optional
            If ``True`` (the default) an edge goes one way only. If ``False`` every
            edge can be followed in both directions.
        """
        self.__directed: bool = directed
        self.__adj: dict[str, list[str]] = {}
        self.__v_size: int = 0

    def __len__(self) -> int:
        """Return the number of vertices. O(1)."""
        return self.__v_size

    def __contains__(self, item: str) -> bool:
        """Return ``True`` if ``item`` is a vertex of the graph. O(1).

        Examples
        --------
        >>> graph = Graph()
        >>> graph.add_vertex("A")
        >>> "A" in graph, "B" in graph
        (True, False)
        """
        return item in self.__adj

    def add_vertex(self, vertex: str, /) -> None:
        """Add ``vertex`` to the graph, or do nothing if it already exists. O(1).

        Parameters
        ----------
        vertex : str
            The vertex to add.
        """
        if vertex not in self.__adj:
            self.__adj[vertex] = []
            self.__v_size += 1

    def add_edge(self, u: str, v: str, /) -> None:
        """Add an edge from ``u`` to ``v``, creating missing endpoints.

        An edge that already exists is ignored. In an undirected graph the edge is
        stored in both directions; a self-loop (``u == v``) is stored once.

        Parameters
        ----------
        u : str
            Source vertex.
        v : str
            Target vertex.

        Examples
        --------
        >>> graph = Graph()
        >>> graph.add_edge("A", "B")
        >>> list(graph.edges())
        [('A', 'B')]
        """
        if u not in self.__adj:
            self.add_vertex(u)
        if v not in self.__adj:
            self.add_vertex(v)
        if v not in self.__adj[u]:
            self.__adj[u].append(v)
        if u not in self.__adj[v] and not self.__directed:
            self.__adj[v].append(u)

    def remove_vertex(self, vertex: str, /) -> None:
        """Remove ``vertex`` together with every edge that touches it.

        Edges pointing at the vertex are removed as well as edges leaving it. O(V + E)
        in a directed graph and O(E) in an undirected one.

        Parameters
        ----------
        vertex : str
            The vertex to remove.

        Raises
        ------
        KeyNotFoundError
            If ``vertex`` is not in the graph.

        Examples
        --------
        >>> graph = Graph()
        >>> graph.add_edge("A", "B")
        >>> graph.add_edge("B", "A")
        >>> graph.remove_vertex("A")
        >>> list(graph.vertices()), list(graph.edges())
        (['B'], [])
        """
        if vertex not in self.__adj:
            raise KeyNotFoundError(f"Vertex {vertex} not found")

        if self.__directed:
            for edges in self.__adj.values():
                if vertex in edges:
                    edges.remove(vertex)
        else:
            for neighbor in list(self.__adj[vertex]):
                self.__adj[neighbor].remove(vertex)

        self.__v_size -= 1
        del self.__adj[vertex]

    def remove_edge(self, u: str, v: str, /) -> None:
        """Remove the edge from ``u`` to ``v``. O(deg(u) + deg(v)).

        In an undirected graph both directions are removed.

        Parameters
        ----------
        u : str
            Source vertex.
        v : str
            Target vertex.

        Raises
        ------
        KeyNotFoundError
            If ``u`` or ``v`` is not in the graph.
        InvalidValueError
            If both vertices exist but there is no edge from ``u`` to ``v``.

        Examples
        --------
        >>> graph = Graph(directed=False)
        >>> graph.add_edge("A", "B")
        >>> graph.remove_edge("A", "B")
        >>> list(graph.edges())
        []
        """
        if u not in self.__adj:
            raise KeyNotFoundError(f"Vertex {u} not found")
        if v not in self.__adj:
            raise KeyNotFoundError(f"Vertex {v} not found")
        if v not in self.__adj[u]:
            raise InvalidValueError(f"Edge {u} -> {v} not found")

        self.__adj[u].remove(v)
        if not self.__directed and u != v:
            self.__adj[v].remove(u)

    def vertices(self) -> Iterator[str]:
        """Iterate over the vertices in insertion order. O(V).

        Yields
        ------
        str
            Each vertex exactly once.
        """
        yield from self.__adj.keys()

    def edges(self) -> Iterator[tuple[str, str]]:
        """Iterate over the edges as ``(source, target)`` pairs. O(V + E).

        An undirected edge appears twice, once for each direction. A self-loop appears
        once.

        Yields
        ------
        tuple of (str, str)
            One pair per stored direction, grouped by source vertex.

        Examples
        --------
        >>> graph = Graph(directed=False)
        >>> graph.add_edge("A", "B")
        >>> list(graph.edges())
        [('A', 'B'), ('B', 'A')]
        """
        for vertex, edges in self.__adj.items():
            for neighbor in edges:
                yield (vertex, neighbor)

    def neighbors(self, vertex: str, /) -> Iterator[str]:
        """Iterate over the vertices reachable from ``vertex`` by one edge.

        Neighbours come in the order their edges were added. An unknown vertex yields
        nothing instead of raising, unlike :meth:`degree`.

        Parameters
        ----------
        vertex : str
            The vertex whose neighbours are listed.

        Yields
        ------
        str
            Each neighbour exactly once.

        Examples
        --------
        >>> graph = Graph()
        >>> graph.add_edge("A", "B")
        >>> graph.add_edge("A", "C")
        >>> list(graph.neighbors("A")), list(graph.neighbors("Z"))
        (['B', 'C'], [])
        """
        if vertex in self.__adj:
            yield from self.__adj[vertex]

    def degree(self, vertex: str, /) -> int:
        """Return the number of edges leaving ``vertex``. O(1).

        This is the out-degree in a directed graph and the number of incident edges in
        an undirected one. A self-loop counts once.

        Parameters
        ----------
        vertex : str
            The vertex to measure.

        Returns
        -------
        int
            The number of neighbours of ``vertex``.

        Raises
        ------
        KeyNotFoundError
            If ``vertex`` is not in the graph.
        """
        if vertex not in self.__adj:
            raise KeyNotFoundError(f"Vertex {vertex} not found")

        return len(self.__adj[vertex])

    def bfs(self, start: str, /) -> Iterator[str]:
        """Traverse breadth-first from ``start``. O(V + E).

        Vertices are produced level by level, and neighbours in insertion order. Only
        vertices reachable from ``start`` are produced, each once.

        Parameters
        ----------
        start : str
            The vertex to start from.

        Yields
        ------
        str
            Vertices in breadth-first order.

        Raises
        ------
        KeyNotFoundError
            If ``start`` is not in the graph. Because this is a generator, the error
            appears when iteration begins, not when the method is called.

        Examples
        --------
        >>> graph = Graph()
        >>> for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]:
        ...     graph.add_edge(u, v)
        >>> list(graph.bfs("A"))
        ['A', 'B', 'C', 'D']
        """
        if start not in self.__adj:
            raise KeyNotFoundError(f"Vertex {start} not found")
        queue = Queue[str]()
        visited = set()
        queue.enqueue(start)
        visited.add(start)
        while queue:
            vertex: str = queue.dequeue()
            yield vertex
            for neighbor in self.__adj[vertex]:
                if neighbor not in visited:
                    queue.enqueue(neighbor)
                    visited.add(neighbor)

    def dfs(self, start: str, /) -> Iterator[str]:
        """Traverse depth-first from ``start`` in preorder. O(V + E).

        The walk follows the first neighbour as deep as it can before backtracking.
        It uses an explicit :class:`~pydsa.linear.Stack`, so deep graphs do not hit the
        recursion limit. Only vertices reachable from ``start`` are produced, each once.

        Parameters
        ----------
        start : str
            The vertex to start from.

        Yields
        ------
        str
            Vertices in depth-first preorder.

        Raises
        ------
        KeyNotFoundError
            If ``start`` is not in the graph. Because this is a generator, the error
            appears when iteration begins, not when the method is called.

        Examples
        --------
        >>> graph = Graph()
        >>> for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]:
        ...     graph.add_edge(u, v)
        >>> list(graph.dfs("A"))
        ['A', 'B', 'D', 'C']
        """
        if start not in self.__adj:
            raise KeyNotFoundError(f"Vertex {start} not found")
        stack = Stack[str]()
        visited = set()
        stack.push(start)
        while stack:
            vertex: str = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            yield vertex
            for neighbor in reversed(self.__adj[vertex]):
                if neighbor not in visited:
                    stack.push(neighbor)

    def has_path(self, u: str, v: str, /) -> bool:
        """Return ``True`` if ``v`` can be reached from ``u``. O(V + E).

        A vertex always has a path to itself. If either vertex is missing the result is
        ``False`` instead of an error. In a directed graph the direction matters.

        Parameters
        ----------
        u : str
            Start vertex.
        v : str
            Target vertex.

        Returns
        -------
        bool
            Whether a path from ``u`` to ``v`` exists.

        Examples
        --------
        >>> graph = Graph()
        >>> graph.add_edge("A", "B")
        >>> graph.has_path("A", "B"), graph.has_path("B", "A")
        (True, False)
        """
        if u not in self.__adj or v not in self.__adj:
            return False
        return any(neighbor == v for neighbor in self.bfs(u))

    def is_connected(self) -> bool:
        """Return ``True`` if every vertex can be reached from any other. O(V + E).

        An empty graph and a graph with a single vertex are connected.

        Returns
        -------
        bool
            Whether the undirected graph is connected.

        Raises
        ------
        InvalidValueError
            If the graph is directed, because connectivity of a directed graph is
            ambiguous (weak or strong).

        Examples
        --------
        >>> graph = Graph(directed=False)
        >>> graph.add_edge("A", "B")
        >>> graph.is_connected()
        True
        >>> graph.add_vertex("C")
        >>> graph.is_connected()
        False
        """
        if self.__directed:
            raise InvalidValueError(
                "is_connected is only for undirected graphs. "
                "Use is_weakly_connected or is_strongly_connected."
            )
        if self.__v_size == 0:
            return True
        vertex: str = next(iter(self.__adj))
        count = sum(1 for _ in self.bfs(vertex))
        return self.__v_size == count

    def clear(self) -> None:
        """Remove all vertices and edges. O(V).

        Whether the graph is directed does not change.

        Examples
        --------
        >>> graph = Graph()
        >>> graph.add_edge("A", "B")
        >>> graph.clear()
        >>> len(graph)
        0
        """
        self.__adj.clear()
        self.__v_size = 0
