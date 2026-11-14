"""Topological ordering for dependency installation."""

from collections import deque

from src.graph import DependencyGraph


def load_order(
    graph: DependencyGraph,
    start: str,
) -> list[str]:
    """Return dependencies in installation order."""
    if start not in graph.adjacency:
        raise ValueError(
            f"Package not found in graph: {start}"
        )

    indegree: dict[str, int] = {
        package: 0
        for package in graph.adjacency
    }

    for dependencies in graph.adjacency.values():
        for dependency in dependencies:
            indegree[dependency] = (
                indegree.get(dependency, 0) + 1
            )

    ready = deque(
        sorted(
            package
            for package, degree in indegree.items()
            if degree == 0
            and package != start
        )
    )

    order: list[str] = []

    while ready:
        package = ready.popleft()
        order.append(package)

        for dependency in graph.dependencies(
            package
        ):
            indegree[dependency] -= 1

            if (
                indegree[dependency] == 0
                and dependency != start
            ):
                ready.append(dependency)

    if len(order) != len(indegree) - 1:
        raise ValueError(
            "Dependency graph contains a cycle"
        )

    order.append(start)

    return order


def print_load_order(
    order: list[str],
) -> None:
    """Print dependency installation order."""
    print("Load order:")

    for position, package in enumerate(
        order,
        start=1,
    ):
        print(f"  {position}. {package}")