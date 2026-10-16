import random

import pytest

from pydsa.core import BaseStructure
from pydsa.exc import InvalidValueError, KeyNotFoundError, PydsaError
from pydsa.graph import Graph


def build(edges: list[tuple[str, str]], *, directed: bool = True) -> Graph:
    graph = Graph(directed=directed)
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


# A -> B, A -> C, B -> D, C -> D: the diamond separates BFS from DFS order.
DIAMOND = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]


class TestConstruction:
    def test_new_graph_is_empty(self) -> None:
        graph = Graph()
        assert len(graph) == 0
        assert not graph
        assert list(graph.vertices()) == []
        assert list(graph.edges()) == []

    def test_is_a_base_structure(self) -> None:
        assert isinstance(Graph(), BaseStructure)

    def test_graph_is_directed_by_default(self) -> None:
        graph = build([("A", "B")])
        assert list(graph.neighbors("B")) == []


class TestSizeAndTruthiness:
    def test_len_counts_vertices_not_edges(self) -> None:
        graph = build([("A", "B"), ("B", "C"), ("C", "A")])
        assert len(graph) == 3

    def test_graph_with_vertices_but_no_edges_is_truthy(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        assert graph

    def test_graph_is_falsy_when_last_vertex_is_removed(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        graph.remove_vertex("A")
        assert not graph


class TestAddVertex:
    def test_vertex_is_added(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        assert "A" in graph
        assert len(graph) == 1

    def test_adding_twice_is_idempotent(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("A")
        assert len(graph) == 1

    def test_adding_an_existing_vertex_keeps_its_edges(self) -> None:
        graph = build([("A", "B")])
        graph.add_vertex("A")
        assert list(graph.neighbors("A")) == ["B"]

    def test_vertices_come_back_in_insertion_order(self) -> None:
        graph = Graph()
        for vertex in ("C", "A", "B"):
            graph.add_vertex(vertex)
        assert list(graph.vertices()) == ["C", "A", "B"]

    def test_contains_is_false_for_unknown_vertex(self) -> None:
        assert "A" not in Graph()


class TestAddEdge:
    def test_creates_missing_endpoints(self) -> None:
        graph = Graph()
        graph.add_edge("A", "B")
        assert "A" in graph
        assert "B" in graph
        assert len(graph) == 2

    def test_directed_edge_goes_one_way(self) -> None:
        graph = build([("A", "B")])
        assert list(graph.neighbors("A")) == ["B"]
        assert list(graph.neighbors("B")) == []

    def test_undirected_edge_goes_both_ways(self) -> None:
        graph = build([("A", "B")], directed=False)
        assert list(graph.neighbors("A")) == ["B"]
        assert list(graph.neighbors("B")) == ["A"]

    def test_duplicate_directed_edge_is_ignored(self) -> None:
        graph = build([("A", "B"), ("A", "B")])
        assert list(graph.edges()) == [("A", "B")]
        assert graph.degree("A") == 1

    def test_duplicate_undirected_edge_is_ignored_in_either_order(self) -> None:
        graph = build([("A", "B"), ("A", "B"), ("B", "A")], directed=False)
        assert graph.degree("A") == 1
        assert graph.degree("B") == 1

    def test_opposite_directed_edges_are_distinct(self) -> None:
        graph = build([("A", "B"), ("B", "A")])
        assert sorted(graph.edges()) == [("A", "B"), ("B", "A")]

    def test_directed_self_loop(self) -> None:
        graph = build([("A", "A")])
        assert list(graph.edges()) == [("A", "A")]
        assert len(graph) == 1

    def test_undirected_self_loop_is_stored_once(self) -> None:
        graph = build([("A", "A")], directed=False)
        assert list(graph.edges()) == [("A", "A")]
        assert graph.degree("A") == 1

    def test_neighbours_keep_insertion_order(self) -> None:
        graph = build([("A", "C"), ("A", "B"), ("A", "D")])
        assert list(graph.neighbors("A")) == ["C", "B", "D"]


class TestEdges:
    def test_directed_edges(self) -> None:
        graph = build(DIAMOND)
        assert sorted(graph.edges()) == sorted(DIAMOND)

    def test_undirected_edge_is_reported_in_both_directions(self) -> None:
        graph = build([("A", "B")], directed=False)
        assert sorted(graph.edges()) == [("A", "B"), ("B", "A")]

    def test_isolated_vertices_contribute_no_edges(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        assert list(graph.edges()) == []


class TestNeighboursAndDegree:
    def test_neighbours_of_unknown_vertex_is_empty(self) -> None:
        assert list(Graph().neighbors("Z")) == []

    def test_neighbours_of_isolated_vertex_is_empty(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        assert list(graph.neighbors("A")) == []

    def test_degree_counts_outgoing_edges(self) -> None:
        graph = build(DIAMOND)
        assert graph.degree("A") == 2
        assert graph.degree("D") == 0

    def test_undirected_degree_counts_incident_edges(self) -> None:
        graph = build(DIAMOND, directed=False)
        assert graph.degree("A") == 2
        assert graph.degree("D") == 2

    def test_degree_of_isolated_vertex_is_zero(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        assert graph.degree("A") == 0

    def test_degree_of_unknown_vertex_raises(self) -> None:
        with pytest.raises(KeyNotFoundError, match="Z"):
            Graph().degree("Z")


class TestRemoveVertex:
    def test_removes_the_vertex(self) -> None:
        graph = build([("A", "B")])
        graph.remove_vertex("A")
        assert "A" not in graph
        assert len(graph) == 1

    def test_directed_removal_cleans_incoming_and_outgoing_edges(self) -> None:
        graph = build([("A", "B"), ("B", "C"), ("C", "B"), ("D", "B")])
        graph.remove_vertex("B")
        assert sorted(graph.edges()) == []
        assert sorted(graph.vertices()) == ["A", "C", "D"]

    def test_undirected_removal_cleans_both_sides(self) -> None:
        graph = build([("A", "B"), ("B", "C")], directed=False)
        graph.remove_vertex("B")
        assert list(graph.edges()) == []
        assert graph.degree("A") == 0
        assert graph.degree("C") == 0

    def test_unrelated_edges_survive(self) -> None:
        graph = build([("A", "B"), ("C", "D")])
        graph.remove_vertex("A")
        assert list(graph.edges()) == [("C", "D")]

    def test_directed_self_loop(self) -> None:
        graph = build([("A", "A"), ("A", "B"), ("B", "A")])
        graph.remove_vertex("A")
        assert list(graph.edges()) == []
        assert list(graph.vertices()) == ["B"]

    def test_undirected_self_loop(self) -> None:
        graph = build([("A", "A"), ("A", "B")], directed=False)
        graph.remove_vertex("A")
        assert list(graph.edges()) == []
        assert list(graph.vertices()) == ["B"]

    def test_vertex_with_only_a_self_loop(self) -> None:
        graph = build([("A", "A")], directed=False)
        graph.remove_vertex("A")
        assert len(graph) == 0

    @pytest.mark.parametrize("directed", [True, False])
    def test_readding_a_removed_vertex_has_no_stale_edges(self, directed: bool) -> None:
        graph = build([("A", "B"), ("B", "A")], directed=directed)
        graph.remove_vertex("A")
        graph.add_vertex("A")
        assert list(graph.neighbors("A")) == []
        assert list(graph.neighbors("B")) == []

    def test_unknown_vertex_raises(self) -> None:
        with pytest.raises(KeyNotFoundError, match="Z"):
            Graph().remove_vertex("Z")

    def test_failed_removal_changes_nothing(self) -> None:
        graph = build([("A", "B")])
        with pytest.raises(KeyNotFoundError):
            graph.remove_vertex("Z")
        assert len(graph) == 2
        assert list(graph.edges()) == [("A", "B")]


class TestRemoveEdge:
    def test_directed_removal_removes_one_direction_only(self) -> None:
        graph = build([("A", "B"), ("B", "A")])
        graph.remove_edge("A", "B")
        assert list(graph.edges()) == [("B", "A")]

    def test_undirected_removal_removes_both_directions(self) -> None:
        graph = build([("A", "B")], directed=False)
        graph.remove_edge("A", "B")
        assert list(graph.edges()) == []

    def test_undirected_removal_works_from_either_endpoint(self) -> None:
        graph = build([("A", "B")], directed=False)
        graph.remove_edge("B", "A")
        assert list(graph.edges()) == []

    def test_vertices_stay_after_edge_removal(self) -> None:
        graph = build([("A", "B")])
        graph.remove_edge("A", "B")
        assert len(graph) == 2

    @pytest.mark.parametrize("directed", [True, False])
    def test_self_loop(self, directed: bool) -> None:
        graph = build([("A", "A"), ("A", "B")], directed=directed)
        graph.remove_edge("A", "A")
        assert ("A", "A") not in list(graph.edges())
        assert list(graph.neighbors("A")) == ["B"]

    def test_missing_edge_raises_invalid_value(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        with pytest.raises(InvalidValueError, match="A -> B"):
            graph.remove_edge("A", "B")

    def test_missing_edge_error_is_catchable_as_value_error_and_pydsa_error(self) -> None:
        graph = build([("A", "B")])
        with pytest.raises(ValueError):
            graph.remove_edge("B", "A")
        with pytest.raises(PydsaError):
            graph.remove_edge("B", "A")

    def test_reverse_of_a_directed_edge_does_not_exist(self) -> None:
        graph = build([("A", "B")])
        with pytest.raises(InvalidValueError):
            graph.remove_edge("B", "A")
        assert list(graph.edges()) == [("A", "B")]

    def test_unknown_source_raises_key_not_found(self) -> None:
        graph = Graph()
        graph.add_vertex("B")
        with pytest.raises(KeyNotFoundError, match="Z"):
            graph.remove_edge("Z", "B")

    def test_unknown_target_raises_key_not_found(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        with pytest.raises(KeyNotFoundError, match="Z"):
            graph.remove_edge("A", "Z")

    def test_failed_removal_changes_nothing(self) -> None:
        graph = build([("A", "B")], directed=False)
        with pytest.raises(KeyNotFoundError):
            graph.remove_edge("A", "Z")
        assert sorted(graph.edges()) == [("A", "B"), ("B", "A")]


class TestBfs:
    def test_level_order(self) -> None:
        assert list(build(DIAMOND).bfs("A")) == ["A", "B", "C", "D"]

    def test_visits_each_vertex_once_despite_cycles(self) -> None:
        graph = build([("A", "B"), ("B", "C"), ("C", "A")])
        assert list(graph.bfs("A")) == ["A", "B", "C"]

    def test_unreachable_vertices_are_skipped(self) -> None:
        graph = build([("A", "B")])
        graph.add_vertex("Z")
        assert list(graph.bfs("A")) == ["A", "B"]

    def test_directed_edges_are_followed_one_way(self) -> None:
        graph = build([("A", "B")])
        assert list(graph.bfs("B")) == ["B"]

    def test_single_vertex(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        assert list(graph.bfs("A")) == ["A"]

    def test_undirected_traversal_reaches_everything_in_the_component(self) -> None:
        graph = build([("A", "B"), ("C", "B")], directed=False)
        assert sorted(graph.bfs("A")) == ["A", "B", "C"]

    def test_missing_start_raises_when_iteration_begins(self) -> None:
        iterator = Graph().bfs("Z")  # generator: nothing runs yet
        with pytest.raises(KeyNotFoundError, match="Z"):
            next(iterator)

    def test_traversal_can_be_resumed_lazily(self) -> None:
        iterator = build(DIAMOND).bfs("A")
        assert next(iterator) == "A"
        assert next(iterator) == "B"


class TestDfs:
    def test_preorder_follows_the_first_neighbour_deep(self) -> None:
        assert list(build(DIAMOND).dfs("A")) == ["A", "B", "D", "C"]

    def test_vertex_discovered_through_a_later_neighbour_keeps_dfs_order(self) -> None:
        # A -> B, A -> C, B -> C: C must be reached through B, before A's own C edge.
        graph = build([("A", "B"), ("A", "C"), ("B", "C")])
        assert list(graph.dfs("A")) == ["A", "B", "C"]

    def test_visits_each_vertex_once_despite_cycles(self) -> None:
        graph = build([("A", "B"), ("B", "C"), ("C", "A")])
        assert list(graph.dfs("A")) == ["A", "B", "C"]

    def test_unreachable_vertices_are_skipped(self) -> None:
        graph = build([("A", "B")])
        graph.add_vertex("Z")
        assert list(graph.dfs("A")) == ["A", "B"]

    def test_directed_edges_are_followed_one_way(self) -> None:
        assert list(build([("A", "B")]).dfs("B")) == ["B"]

    def test_self_loop_does_not_repeat_the_vertex(self) -> None:
        graph = build([("A", "A"), ("A", "B")])
        assert list(graph.dfs("A")) == ["A", "B"]

    def test_long_chain_does_not_hit_the_recursion_limit(self) -> None:
        edges = [(str(i), str(i + 1)) for i in range(5000)]
        order = list(build(edges).dfs("0"))
        assert len(order) == 5001
        assert order[-1] == "5000"

    def test_missing_start_raises_when_iteration_begins(self) -> None:
        iterator = Graph().dfs("Z")
        with pytest.raises(KeyNotFoundError, match="Z"):
            next(iterator)

    def test_bfs_and_dfs_reach_the_same_vertices(self) -> None:
        graph = build(DIAMOND + [("E", "A")])
        assert sorted(graph.bfs("A")) == sorted(graph.dfs("A"))


class TestHasPath:
    def test_path_exists(self) -> None:
        assert build(DIAMOND).has_path("A", "D")

    def test_direction_matters_in_directed_graphs(self) -> None:
        graph = build(DIAMOND)
        assert not graph.has_path("D", "A")

    def test_undirected_paths_are_symmetric(self) -> None:
        graph = build(DIAMOND, directed=False)
        assert graph.has_path("D", "A")
        assert graph.has_path("A", "D")

    def test_disconnected_vertices(self) -> None:
        graph = build([("A", "B")])
        graph.add_vertex("Z")
        assert not graph.has_path("A", "Z")

    def test_vertex_has_a_path_to_itself(self) -> None:
        graph = Graph()
        graph.add_vertex("A")
        assert graph.has_path("A", "A")

    def test_unknown_vertices_give_false_not_an_error(self) -> None:
        graph = build([("A", "B")])
        assert graph.has_path("A", "Z") is False
        assert graph.has_path("Z", "A") is False
        assert graph.has_path("Z", "Z") is False

    def test_path_disappears_when_a_vertex_on_it_is_removed(self) -> None:
        graph = build([("A", "B"), ("B", "C")])
        graph.remove_vertex("B")
        assert not graph.has_path("A", "C")


class TestIsConnected:
    def test_empty_graph_is_connected(self) -> None:
        assert Graph(directed=False).is_connected()

    def test_single_vertex_is_connected(self) -> None:
        graph = Graph(directed=False)
        graph.add_vertex("A")
        assert graph.is_connected()

    def test_connected_graph(self) -> None:
        assert build(DIAMOND, directed=False).is_connected()

    def test_isolated_vertex_disconnects_the_graph(self) -> None:
        graph = build([("A", "B")], directed=False)
        graph.add_vertex("C")
        assert not graph.is_connected()

    def test_two_components(self) -> None:
        graph = build([("A", "B"), ("C", "D")], directed=False)
        assert not graph.is_connected()

    def test_removing_a_bridge_vertex_disconnects(self) -> None:
        graph = build([("A", "B"), ("B", "C")], directed=False)
        graph.remove_vertex("B")
        assert not graph.is_connected()

    def test_result_does_not_depend_on_insertion_order(self) -> None:
        forward = build([("A", "B"), ("B", "C")], directed=False)
        backward = build([("C", "B"), ("B", "A")], directed=False)
        assert forward.is_connected() and backward.is_connected()

    def test_directed_graph_is_rejected(self) -> None:
        with pytest.raises(InvalidValueError, match="undirected"):
            build([("A", "B")]).is_connected()

    def test_empty_directed_graph_is_rejected_too(self) -> None:
        with pytest.raises(InvalidValueError):
            Graph().is_connected()


class TestClear:
    def test_clear_empties_the_graph(self) -> None:
        graph = build(DIAMOND)
        graph.clear()
        assert len(graph) == 0
        assert not graph
        assert list(graph.edges()) == []
        assert "A" not in graph

    def test_clear_on_empty_graph_is_harmless(self) -> None:
        graph = Graph()
        graph.clear()
        assert len(graph) == 0

    def test_graph_is_reusable_after_clear(self) -> None:
        graph = build([("A", "B")])
        graph.clear()
        graph.add_edge("B", "C")
        assert list(graph.edges()) == [("B", "C")]

    def test_clear_keeps_directedness(self) -> None:
        undirected = build([("A", "B")], directed=False)
        undirected.clear()
        undirected.add_edge("A", "B")
        assert list(undirected.neighbors("B")) == ["A"]

        directed = build([("A", "B")])
        directed.clear()
        directed.add_edge("A", "B")
        assert list(directed.neighbors("B")) == []


class TestAgainstModel:
    @pytest.mark.parametrize("directed", [True, False])
    @pytest.mark.parametrize("seed", range(10))
    def test_random_operations_match_a_set_model(self, seed: int, directed: bool) -> None:
        rng = random.Random(seed)
        graph = Graph(directed=directed)
        vertices: set[str] = set()
        edges: set[tuple[str, str]] = set()
        names = list("ABCDEF")

        def model_add(u: str, v: str) -> None:
            vertices.update((u, v))
            edges.add((u, v))
            if not directed:
                edges.add((v, u))

        for _ in range(300):
            u, v = rng.choice(names), rng.choice(names)
            action = rng.choice(("edge", "edge", "vertex", "rm_edge", "rm_vertex"))
            if action == "edge":
                graph.add_edge(u, v)
                model_add(u, v)
            elif action == "vertex":
                graph.add_vertex(u)
                vertices.add(u)
            elif action == "rm_edge":
                if u in vertices and v in vertices and (u, v) in edges:
                    graph.remove_edge(u, v)
                    edges.discard((u, v))
                    if not directed:
                        edges.discard((v, u))
            elif u in vertices:
                graph.remove_vertex(u)
                vertices.discard(u)
                edges = {(a, b) for a, b in edges if u not in (a, b)}
            assert set(graph.vertices()) == vertices
            assert len(graph) == len(vertices)
            listed = list(graph.edges())
            assert len(listed) == len(set(listed))
            assert set(listed) == edges
            if not directed:
                assert all((b, a) in edges for a, b in edges)
        for vertex in vertices:
            expected = {b for a, b in edges if a == vertex}
            assert set(graph.neighbors(vertex)) == expected
            assert graph.degree(vertex) == len(expected)
