from collections.abc import Iterator

from ..linear import Queue, Stack


class Graph:
    """
    A graph data structure supporting both directed and undirected edges.

    Implemented with an adjacency list. Supports adding and removing
    vertices and edges, BFS and DFS traversal, path existence checking,
    and connectivity testing.

    Representation
    --------------
    Adjacency list: ``dict[str, list[str]]``
        Each vertex maps to a list of its neighbors.

    .. csv-table:: Graph Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 30, 20, 20

       "add_vertex", "O(1)", "O(1)"
       "add_edge", "O(1)", "O(1)"
       "remove_vertex", "O(V + E)", "O(1)"
       "remove_edge", "O(V)", "O(1)"
       "vertices", "O(V)", "O(1)"
       "edges", "O(E)", "O(1)"
       "neighbors", "O(1)*", "O(1)"
       "degree", "O(1)", "O(1)"
       "bfs", "O(V + E)", "O(V)"
       "dfs", "O(V + E)", "O(V)"
       "has_path", "O(V + E)", "O(V)"
       "is_connected", "O(V + E)", "O(V)"
       "__contains__", "O(1)", "O(1)"

    *Amortized — yielding each neighbor is O(1) per element.

    Notes
    -----
    - BFS uses a custom ``Queue`` (FIFO); DFS uses a custom ``Stack`` (LIFO).
    - ``is_connected`` uses BFS from the first vertex. For directed graphs,
      this checks reachability from the starting vertex, not strong connectivity.
    - Self-loops and parallel edges are not prevented but the edge count
      tracks each insertion independently.
    """

    def __init__(self, directed: bool = True) -> None:

        self.__directed: bool = directed
        self.__adj: dict[str, list[str]] = {}
        self.__v_size: int = 0
        self.__e_size: int = 0

    def __len__(self) -> int:
        """Return the number of vertices. O(1)."""
        return self.__v_size

    def __bool__(self) -> bool:
        """Return True if the graph has at least one vertex. O(1)."""
        return self.__v_size > 0

    def __contains__(self, item: str) -> bool:
        """Return True if the vertex exists. O(1)."""
        return item in self.__adj

    def add_vertex(self, vertex: str, /) -> None:
        """Add a vertex if it does not already exist. O(1).

        If the vertex already exists, this is a no-op.
        """
        if vertex not in self.__adj:
            self.__adj[vertex] = []
            self.__v_size += 1

    def add_edge(self, u: str, v: str, /) -> None:
        """Add an edge from ``u`` to ``v``. O(1).

        Vertices are created automatically if they do not exist.
        In an undirected graph, the reverse edge is also added.

        Parameters
        ----------
        u : str
            Source vertex.
        v : str
            Target vertex.
        """
        if u not in self.__adj:
            self.add_vertex(u)
        if v not in self.__adj:
            self.add_vertex(v)
        if v not in self.__adj[u]:
            self.__adj[u].append(v)
            self.__e_size += 1
        if u not in self.__adj[v] and not self.__directed:
            self.__adj[v].append(u)
            self.__e_size += 1

    def remove_vertex(self, vertex: str, /) -> None:
        """Remove a vertex and all its incident edges. O(V + E).

        Raises
        ------
        KeyError
            If the vertex does not exist.
        """
        if vertex not in self.__adj:
            raise KeyError(f'Vertex {vertex} not found')

        if self.__directed:
            for edges in self.__adj.values():
                if vertex in edges:
                    edges.remove(vertex)
                    self.__e_size -= 1
        else:
            for v in self.__adj[vertex]:
                self.__adj[v].remove(vertex)
                self.__e_size -= 1
        self.__e_size -= len(self.__adj[vertex])
        self.__v_size -= 1
        del self.__adj[vertex]

    def remove_edge(self, u: str, v: str, /) -> None:
        """Remove an edge from ``u`` to ``v``. O(degree(u)).

        In an undirected graph, the reverse edge is also removed.

        Raises
        ------
        KeyError
            If either vertex does not exist.
        ValueError
            If the edge does not exist.
        """
        if u not in self.__adj:
            raise KeyError(f"Vertex {u} not found")
        if v not in self.__adj:
            raise KeyError(f"Vertex {v} not found")
        if v not in self.__adj[u]:
            raise ValueError(f"Edge {u} -> {v} not found")
        self.__adj[u].remove(v)
        self.__e_size -= 1
        if not self.__directed:
            self.__adj[v].remove(u)
            self.__e_size -= 1

    def vertices(self) -> Iterator[str]:
        """Yield all vertices. O(V)."""
        yield from self.__adj.keys()

    def edges(self) -> Iterator[tuple[str, str]]:
        """Yield all edges as ``(u, v)`` tuples. O(E)."""
        for vertex, edges in self.__adj.items():
            for neighbor in edges:
                yield (vertex, neighbor)

    def neighbors(self, vertex: str, /) -> Iterator[str]:
        """Yield the neighbors of a vertex. O(degree(v)).

        Silently returns nothing if the vertex does not exist.
        """
        if vertex in self.__adj:
            yield from self.__adj[vertex]

    def degree(self, vertex: str, /) -> int:
        """Return the out-degree (or degree in undirected) of a vertex. O(1).

        Raises
        ------
        KeyError
            If the vertex does not exist.
        """
        if vertex not in self.__adj:
            raise KeyError(f"Vertex {vertex} not found")

        return len(self.__adj[vertex])

    def bfs(self, start: str, /) -> Iterator[str]:
        """Yield vertices in breadth-first order from ``start``. O(V + E).

         Uses a custom ``Queue`` (FIFO).

         Raises
         ------
         KeyError
             If the start vertex does not exist.
         """
        if start not in self.__adj:
            raise KeyError(f"Key {start} not found")
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
        """Yield vertices in depth-first order from ``start``. O(V + E).

           Uses a custom ``Stack`` (LIFO).

           Raises
           ------
           KeyError
               If the start vertex does not exist.
           """
        if start not in self.__adj:
            raise KeyError(f"Key {start} not found")
        stack = Stack[str]()
        visited = set()
        stack.push(start)
        visited.add(start)
        while stack:
            vertex: str = stack.pop()
            yield vertex
            for neighbor in self.__adj[vertex]:
                if neighbor not in visited:
                    stack.push(neighbor)
                    visited.add(neighbor)

    def has_path(self, u: str, v: str, /) -> bool:
        """Return True if a path exists from ``u`` to ``v``. O(V + E).

        Uses BFS internally. Returns False if either vertex is
        missing or no path exists.
        """
        if u not in self.__adj or v not in self.__adj:
            return False
        return any(neighbor == v for neighbor in self.bfs(u))

    def is_connected(self) -> bool:
        """Return True if all vertices are reachable from the first vertex. O(V + E).

        An empty graph is considered connected. For directed graphs,
        this checks forward reachability, not strong connectivity.
        """
        if self.__v_size == 0:
            return True
        vertex: str = next(iter(self.__adj))
        count = sum(1 for _ in self.bfs(vertex))
        return self.__v_size == count

    def clear(self) -> None:
        """Remove all vertices and edges. O(1)."""
        self.__adj.clear()
        self.__v_size = 0
        self.__e_size = 0
