"""Dependency graph construction and traversal."""

from collections import deque
from dataclasses import dataclass, field


@dataclass
class DependencyGraph:
    """Directed dependency graph."""

    adjacency: dict[str, list[str]] = field(
        default_factory=dict
    )

    def add_edge(
        self,
        source: str,
        target: str,
    ) -> None:
        """Add a directed dependency edge."""
        self.adjacency.setdefault(
            source,
            [],
        )

        if target not in self.adjacency[source]:
            self.adjacency[source].append(
                target
            )

        self.adjacency.setdefault(
            target,
            [],
        )

    def dependencies(
        self,
        package: str,
    ) -> list[str]:
        """Return direct dependencies of a package."""
        return self.adjacency.get(
            package,
            [],
        )


def load_test_graph(
    path: str,
) -> DependencyGraph:
    """Load a test graph from a text file."""
    graph = DependencyGraph()

    with open(
        path,
        encoding="utf-8",
    ) as graph_file:
        for line_number, raw_line in enumerate(
            graph_file,
            start=1,
        ):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            parts = [
                part.strip()
                for part in line.split("->")
            ]

            if len(parts) != 2 or not all(parts):
                raise ValueError(
                    f"Invalid graph line "
                    f"{line_number}: "
                    f"{raw_line.rstrip()}"
                )

            graph.add_edge(
                parts[0],
                parts[1],
            )

    return graph


def recursive_bfs(
    graph: DependencyGraph,
    start: str,
    max_depth: int,
    package_filter: str,
) -> dict[str, int]:
    """Traverse dependencies using recursive BFS."""
    if max_depth < 1:
        raise ValueError(
            "Maximum depth must be at least 1"
        )

    distances: dict[str, int] = {
        start: 0,
    }
    queue: deque[str] = deque([start])

    def visit(
        current: str,
        depth: int,
    ) -> None:
        if depth >= max_depth:
            return

        for dependency in graph.dependencies(
            current
        ):
            if package_filter and package_filter in dependency:
                continue

            if dependency in distances:
                continue

            distances[dependency] = depth + 1
            queue.append(dependency)
            visit(
                dependency,
                depth + 1,
            )

    visit(
        start,
        0,
    )

    return distances


def build_subgraph(
    graph: DependencyGraph,
    start: str,
    max_depth: int,
    package_filter: str,
) -> DependencyGraph:
    """Build a filtered transitive dependency subgraph."""
    distances = recursive_bfs(
        graph,
        start,
        max_depth,
        package_filter,
    )

    result = DependencyGraph()

    for package in distances:
        for dependency in graph.dependencies(
            package
        ):
            if package_filter and package_filter in dependency:
                continue

            if dependency in distances:
                result.add_edge(
                    package,
                    dependency,
                )

    return result


def print_graph(
    graph: DependencyGraph,
) -> None:
    """Print graph edges to the terminal."""
    print("Dependency graph:")

    edges = []

    for source, targets in graph.adjacency.items():
        for target in targets:
            edges.append(
                f"  {source} -> {target}"
            )

    if not edges:
        print("  none")
        return

    for edge in sorted(edges):
        print(edge)