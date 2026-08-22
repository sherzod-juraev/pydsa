import pytest

from pydsa import Graph


class TestBasics:
    def test_add_vertex(self) -> None:
        g = Graph()
        g.add_vertex("A")
        assert "A" in g
        assert len(g) == 1

    def test_add_vertex_is_idempotent(self) -> None:
        g = Graph()
        g.add_vertex("A")
        g.add_vertex("A")
        assert len(g) == 1

    def test_add_edge_creates_vertices(self) -> None:
        g = Graph()
        g.add_edge("A", "B")
        assert "A" in g
        assert "B" in g

    def test_undirected_edge_is_bidirectional(self) -> None:
        g = Graph(directed=False)
        g.add_edge("A", "B")
        assert list(g.neighbors("A")) == ["B"]
        assert list(g.neighbors("B")) == ["A"]

    def test_directed_edge_is_one_way(self) -> None:
        g = Graph(directed=True)
        g.add_edge("A", "B")
        assert list(g.neighbors("A")) == ["B"]
        assert list(g.neighbors("B")) == []

    def test_neighbors_of_missing_vertex_is_empty(self) -> None:
        g = Graph()
        assert list(g.neighbors("ghost")) == []

    def test_degree_raises_on_missing_vertex(self) -> None:
        g = Graph()
        with pytest.raises(KeyError):
            g.degree("ghost")


class TestRemoveVertex:
    def test_remove_vertex_cleans_incident_edges(self) -> None:
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.remove_vertex("A")
        assert "A" not in g
        assert list(g.neighbors("B")) == []
        assert list(g.neighbors("C")) == []

    def test_remove_missing_vertex_raises(self) -> None:
        g = Graph()
        with pytest.raises(KeyError):
            g.remove_vertex("ghost")

    def test_remove_vertex_with_self_loop_undirected(self) -> None:
        """Regression test: remove_vertex used to mutate the adjacency
        list while iterating over it, which broke on self-loops in
        undirected graphs (A-A edge where a vertex is its own neighbor).
        """
        g = Graph(directed=False)
        g.add_edge("A", "A")  # self-loop
        g.add_edge("A", "B")
        g.remove_vertex("A")
        assert "A" not in g
        assert list(g.neighbors("B")) == []
        assert len(g) == 1

    def test_remove_vertex_self_loop_only(self) -> None:
        g = Graph(directed=False)
        g.add_edge("A", "A")
        g.remove_vertex("A")
        assert "A" not in g
        assert len(g) == 0


class TestRemoveEdge:
    def test_remove_edge(self) -> None:
        g = Graph()
        g.add_edge("A", "B")
        g.remove_edge("A", "B")
        assert list(g.neighbors("A")) == []

    def test_remove_edge_undirected_removes_both_directions(self) -> None:
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.remove_edge("A", "B")
        assert list(g.neighbors("A")) == []
        assert list(g.neighbors("B")) == []

    def test_remove_nonexistent_edge_raises(self) -> None:
        g = Graph()
        g.add_vertex("A")
        g.add_vertex("B")
        with pytest.raises(ValueError):
            g.remove_edge("A", "B")

    def test_remove_edge_missing_vertex_raises(self) -> None:
        g = Graph()
        with pytest.raises(KeyError):
            g.remove_edge("A", "B")


class TestTraversal:
    def test_bfs_order(self) -> None:
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        assert list(g.bfs("A")) == ["A", "B", "C"]

    def test_dfs_visits_all_reachable(self) -> None:
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        assert set(g.dfs("A")) == {"A", "B", "C"}

    def test_bfs_missing_start_raises_keyerror(self) -> None:
        g = Graph()
        with pytest.raises(KeyError):
            list(g.bfs("ghost"))

    def test_dfs_missing_start_raises_keyerror(self) -> None:
        g = Graph()
        with pytest.raises(KeyError):
            list(g.dfs("ghost"))


class TestPathAndConnectivity:
    def test_has_path_true(self) -> None:
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        assert g.has_path("A", "C") is True

    def test_has_path_false_directed(self) -> None:
        g = Graph(directed=True)
        g.add_edge("A", "B")
        assert g.has_path("B", "A") is False

    def test_has_path_missing_vertex_returns_false(self) -> None:
        g = Graph()
        g.add_vertex("A")
        assert g.has_path("A", "ghost") is False

    def test_is_connected_true(self) -> None:
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        assert g.is_connected() is True

    def test_is_connected_false(self) -> None:
        g = Graph(directed=False)
        g.add_vertex("A")
        g.add_vertex("B")  # isolated
        assert g.is_connected() is False

    def test_empty_graph_is_connected(self) -> None:
        assert Graph().is_connected() is True


class TestClearAndDunders:
    def test_clear(self) -> None:
        g = Graph()
        g.add_edge("A", "B")
        g.clear()
        assert len(g) == 0
        assert list(g.vertices()) == []

    def test_bool_empty_and_nonempty(self) -> None:
        g = Graph()
        assert not g
        g.add_vertex("A")
        assert g