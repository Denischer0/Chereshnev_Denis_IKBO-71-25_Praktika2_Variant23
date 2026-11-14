"""Tests for dependency installation order."""

import pytest

from src.graph import DependencyGraph
from src.order import load_order


def test_load_order_places_dependencies_first() -> None:
    graph = DependencyGraph()

    graph.add_edge("A", "B")
    graph.add_edge("B", "C")

    order = load_order(graph, "A")

    assert order.index("C") < order.index("B")
    assert order.index("B") < order.index("A")
    assert order[-1] == "A"


def test_load_order_handles_multiple_dependencies() -> None:
    graph = DependencyGraph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")

    order = load_order(graph, "A")

    assert order.index("D") < order.index("B")
    assert order.index("D") < order.index("C")
    assert order.index("B") < order.index("A")
    assert order.index("C") < order.index("A")


def test_cycle_is_detected() -> None:
    graph = DependencyGraph()

    graph.add_edge("A", "B")
    graph.add_edge("B", "A")

    with pytest.raises(ValueError):
        load_order(graph, "A")


def test_unknown_package_is_rejected() -> None:
    graph = DependencyGraph()
    graph.add_edge("A", "B")

    with pytest.raises(ValueError):
        load_order(graph, "X")