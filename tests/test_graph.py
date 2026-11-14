"""Tests for graph traversal."""

from pathlib import Path

from src.graph import (
    build_subgraph,
    load_test_graph,
    recursive_bfs,
)

FIXTURE = (
    Path(__file__).parent
    / "test_graph.txt"
)


def test_recursive_bfs_respects_depth() -> None:
    graph = load_test_graph(str(FIXTURE))

    distances = recursive_bfs(
        graph,
        "A",
        1,
        "",
    )

    assert distances == {
        "A": 0,
        "B": 1,
        "C": 1,
    }


def test_recursive_bfs_handles_cycle() -> None:
    graph = load_test_graph(str(FIXTURE))

    distances = recursive_bfs(
        graph,
        "A",
        10,
        "",
    )

    assert set(distances) == {
        "A",
        "B",
        "C",
        "D",
        "E",
    }


def test_filter_excludes_matching_packages() -> None:
    graph = load_test_graph(str(FIXTURE))

    subgraph = build_subgraph(
        graph,
        "A",
        10,
        "B",
    )

    assert "B" not in subgraph.adjacency


def test_invalid_graph_line_is_rejected(
    tmp_path,
) -> None:
    invalid_file = tmp_path / "invalid.txt"
    invalid_file.write_text(
        "A B\n",
        encoding="utf-8",
    )

    try:
        load_test_graph(str(invalid_file))
    except ValueError as error:
        assert "Invalid graph line" in str(error)
    else:
        raise AssertionError(
            "ValueError was not raised"
        )