import pytest

from GA_ProjectUtils import Graph
from mst import unionFind, kruskal


def assert_spanning_tree(original_graph: Graph, output_mst: set):
    checking_uf = unionFind(original_graph.numVerts)

    assert len(output_mst) == original_graph.numVerts - 1

    for mst_edge in output_mst:
        _, edge = mst_edge
        checking_uf.union(edge[0], edge[1])
        assert edge in original_graph.edges

    assert_uf_not_disjoint(checking_uf)


def get_mst_weight(output_mst: set) -> float:
    total_weight = 0
    for mst_edge in output_mst:
        edge_weight, _ = mst_edge
        total_weight += edge_weight
    return total_weight


def assert_uf_not_disjoint(input_uf: unionFind):
    for i in range(len(input_uf.pi)):
        assert input_uf.find(i) == input_uf.find(0)


# Graphs have vertices from 0 ... number_of_vertices - 1
# Graphs have a list of edges with weights (weight, u, v)
# This is represented as Graph(number_of_vertices, [(weight, u, v), ...])
# I just manually calculated the expected MST weight for each graph - so they could be wrong.
@pytest.mark.parametrize(
    "graph, expected_mst_weight",
    [
        (Graph(3, [(1, 0, 1), (1, 1, 2), (2, 2, 0)]), 2),
        (Graph(4, [(1, 0, 1), (1, 1, 2), (1, 2, 3), (1, 3, 0)]), 3),
        (Graph(4, [(-3, 0, 1), (-2, 1, 2), (-1, 2, 3), (0, 3, 0)]), -6),
        (
            Graph(
                8,
                [
                    (6, 0, 1),
                    (5, 1, 2),
                    (6, 2, 3),
                    (1, 4, 5),
                    (3, 5, 6),
                    (3, 6, 7),
                    (1, 0, 4),
                    (2, 1, 5),
                    (4, 2, 6),
                    (7, 3, 7),
                    (2, 1, 4),
                    (5, 2, 5),
                    (5, 3, 6),
                ],
            ),
            19,
        ),
        (
            Graph(
                8,
                [
                    (1, 0, 1),
                    (2, 1, 2),
                    (3, 2, 3),
                    (5, 4, 5),
                    (1, 5, 6),
                    (1, 6, 7),
                    (4, 0, 4),
                    (6, 1, 5),
                    (2, 2, 6),
                    (4, 3, 7),
                    (8, 0, 5),
                    (6, 1, 6),
                    (1, 3, 6),
                ],
            ),
            12,
        ),
        (
            Graph(
                9,
                [
                    (6, 0, 1),
                    (1, 0, 2),
                    (10, 0, 3),
                    (2, 1, 2),
                    (2, 3, 2),
                    (4, 1, 4),
                    (1, 1, 5),
                    (20, 2, 5),
                    (5, 3, 6),
                    (2, 4, 5),
                    (6, 5, 6),
                    (5, 4, 7),
                    (10, 5, 7),
                    (4, 6, 8),
                    (12, 7, 8),
                ],
            ),
            22,
        ),
    ],
    ids=[
        "cycle",
        "slighly_larger_cycle",
        "negative_weights",
        "exercise_5_1",
        "exercise_5_2",
        "exercise_7_10",
    ],
)
def test_kruskal(graph: Graph, expected_mst_weight: float):
    output_mst, output_uf = kruskal(graph)
    assert_spanning_tree(graph, output_mst)
    assert_uf_not_disjoint(output_uf)
    assert get_mst_weight(output_mst) == expected_mst_weight