import pytest
from pydsa import Graph


class TestGraphInit:
    """__init__"""

    def test_empty_directed_graph(self):
        g = Graph(directed=True)
        assert len(g) == 0
        assert not g

    def test_empty_undirected_graph(self):
        g = Graph(directed=False)
        assert len(g) == 0
        assert not g


class TestGraphAddVertex:
    """add_vertex"""

    def test_add_single_vertex(self):
        g = Graph()
        g.add_vertex("A")
        assert len(g) == 1
        assert "A" in g

    def test_add_multiple_vertices(self):
        g = Graph()
        for v in ["A", "B", "C"]:
            g.add_vertex(v)
        assert len(g) == 3

    def test_add_duplicate_vertex_noop(self):
        g = Graph()
        g.add_vertex("A")
        g.add_vertex("A")
        assert len(g) == 1

    def test_add_vertex_zero_degree(self):
        g = Graph()
        g.add_vertex("A")
        assert g.degree("A") == 0


class TestGraphAddEdge:
    """add_edge"""

    def test_add_edge_creates_vertices(self):
        g = Graph()
        g.add_edge("A", "B")
        assert len(g) == 2
        assert "A" in g
        assert "B" in g

    def test_add_edge_directed(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        assert list(g.neighbors("A")) == ["B"]
        assert list(g.neighbors("B")) == []

    def test_add_edge_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        assert list(g.neighbors("A")) == ["B"]
        assert list(g.neighbors("B")) == ["A"]

    def test_add_edge_increases_degree(self):
        g = Graph()
        g.add_edge("A", "B")
        assert g.degree("A") == 1

    def test_add_duplicate_edge_noop(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("A", "B")
        assert g.degree("A") == 1

    def test_add_multiple_edges(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        assert g.degree("A") == 2
        assert g.degree("B") == 1
        assert g.degree("C") == 1


class TestGraphRemoveVertex:
    """remove_vertex"""

    def test_remove_vertex(self):
        g = Graph()
        g.add_vertex("A")
        g.remove_vertex("A")
        assert len(g) == 0
        assert "A" not in g

    def test_remove_vertex_removes_edges_directed(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("C", "A")
        g.remove_vertex("A")
        assert g.degree("B") == 0
        assert g.degree("C") == 0

    def test_remove_vertex_removes_edges_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.remove_vertex("A")
        assert g.degree("B") == 0
        assert g.degree("C") == 0

    def test_remove_nonexistent_vertex_raises(self):
        g = Graph()
        with pytest.raises(KeyError):
            g.remove_vertex("X")


class TestGraphRemoveEdge:
    """remove_edge"""

    def test_remove_edge_directed(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.remove_edge("A", "B")
        assert g.degree("A") == 0

    def test_remove_edge_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.remove_edge("A", "B")
        assert g.degree("A") == 0
        assert g.degree("B") == 0

    def test_remove_nonexistent_edge_raises(self):
        g = Graph()
        g.add_vertex("A")
        g.add_vertex("B")
        with pytest.raises(ValueError):
            g.remove_edge("A", "B")

    def test_remove_edge_nonexistent_vertex_raises(self):
        g = Graph()
        with pytest.raises(KeyError):
            g.remove_edge("X", "Y")


class TestGraphVertices:
    """vertices"""

    def test_vertices_empty(self):
        g = Graph()
        assert list(g.vertices()) == []

    def test_vertices_returns_all(self):
        g = Graph()
        g.add_vertex("A")
        g.add_vertex("B")
        assert sorted(g.vertices()) == ["A", "B"]


class TestGraphEdges:
    """edges"""

    def test_edges_empty(self):
        g = Graph()
        assert list(g.edges()) == []

    def test_edges_directed(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        assert sorted(g.edges()) == [("A", "B"), ("B", "C")]

    def test_edges_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        assert sorted(g.edges()) == [("A", "B"), ("B", "A")]


class TestGraphNeighbors:
    """neighbors"""

    def test_neighbors_directed(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        assert sorted(g.neighbors("A")) == ["B", "C"]
        assert list(g.neighbors("B")) == []

    def test_neighbors_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        assert list(g.neighbors("B")) == ["A"]

    def test_neighbors_nonexistent_vertex(self):
        g = Graph()
        assert list(g.neighbors("X")) == []


class TestGraphDegree:
    """degree"""

    def test_degree_out(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        assert g.degree("A") == 2

    def test_degree_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        assert g.degree("A") == 1
        assert g.degree("B") == 1

    def test_degree_nonexistent_raises(self):
        g = Graph()
        with pytest.raises(KeyError):
            g.degree("X")


class TestGraphBFS:
    """bfs"""

    def test_bfs_simple(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        assert list(g.bfs("A")) == ["A", "B", "C"]

    def test_bfs_level_order(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        g.add_edge("C", "E")
        result = list(g.bfs("A"))
        assert result[0] == "A"
        assert set(result[1:3]) == {"B", "C"}
        assert set(result[3:]) == {"D", "E"}

    def test_bfs_nonexistent_start_raises(self):
        g = Graph()
        with pytest.raises(KeyError):
            list(g.bfs("X"))

    def test_bfs_disconnected(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_vertex("C")
        assert list(g.bfs("A")) == ["A", "B"]


class TestGraphDFS:
    """dfs"""

    def test_dfs_simple(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        result = list(g.dfs("A"))
        assert result[0] == "A"
        assert set(result) == {"A", "B", "C"}

    def test_dfs_deep_path(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "D")
        result = list(g.dfs("A"))
        assert result == ["A", "B", "C", "D"]

    def test_dfs_nonexistent_start_raises(self):
        g = Graph()
        with pytest.raises(KeyError):
            list(g.dfs("X"))


class TestGraphHasPath:
    """has_path"""

    def test_has_path_true(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        assert g.has_path("A", "C") is True

    def test_has_path_false(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_vertex("C")
        assert g.has_path("A", "C") is False

    def test_has_path_same_vertex(self):
        g = Graph()
        g.add_vertex("A")
        assert g.has_path("A", "A") is True

    def test_has_path_nonexistent_vertex(self):
        g = Graph()
        assert g.has_path("X", "Y") is False

    def test_has_path_directed_one_way(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        assert g.has_path("A", "B") is True
        assert g.has_path("B", "A") is False


class TestGraphIsConnected:
    """is_connected"""

    def test_empty_graph_connected(self):
        g = Graph()
        assert g.is_connected() is True

    def test_single_vertex_connected(self):
        g = Graph()
        g.add_vertex("A")
        assert g.is_connected() is True

    def test_connected_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        assert g.is_connected() is True

    def test_disconnected_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_vertex("C")
        assert g.is_connected() is False

    def test_connected_directed(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        assert g.is_connected() is True


class TestGraphClear:
    """clear"""

    def test_clear_removes_all(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.clear()
        assert len(g) == 0
        assert not g
        assert list(g.vertices()) == []
        assert list(g.edges()) == []


class TestGraphContains:
    """__contains__"""

    def test_contains_existing(self):
        g = Graph()
        g.add_vertex("A")
        assert "A" in g

    def test_contains_nonexisting(self):
        g = Graph()
        assert "X" not in g


class TestGraphBool:
    """__bool__"""

    def test_nonempty_is_truthy(self):
        g = Graph()
        g.add_vertex("A")
        assert bool(g)

    def test_empty_is_falsy(self):
        g = Graph()
        assert not g


class TestGraphLargeData:
    """Large graph"""

    def test_many_vertices_and_edges(self):
        g = Graph(directed=False)
        n = 100
        for i in range(n):
            g.add_vertex(str(i))
        for i in range(n - 1):
            g.add_edge(str(i), str(i + 1))
        assert len(g) == n
        assert g.has_path("0", str(n - 1)) is True
        assert g.is_connected() is True

    def test_bfs_large_graph(self):
        g = Graph(directed=False)
        n = 200
        for i in range(n - 1):
            g.add_edge(str(i), str(i + 1))
        result = list(g.bfs("0"))
        assert len(result) == n


class TestGraphDirectedSpecific:
    """Directed graph edge cases"""

    def test_self_loop(self):
        g = Graph(directed=True)
        g.add_edge("A", "A")
        assert g.degree("A") == 1
        assert list(g.neighbors("A")) == ["A"]

    def test_cycle_detection_via_path(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "A")
        assert g.has_path("A", "C") is True
        assert g.has_path("C", "A") is True

    def test_in_degree_not_tracked(self):
        g = Graph(directed=True)
        g.add_edge("B", "A")
        g.add_edge("C", "A")
        assert g.degree("A") == 0  # out-degree
        assert list(g.neighbors("A")) == []