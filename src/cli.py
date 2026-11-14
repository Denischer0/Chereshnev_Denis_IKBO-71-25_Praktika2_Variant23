"""Command-line entry point."""

import sys

from src.cargo import (
    Dependency,
    fetch_direct_dependencies,
    print_direct_dependencies,
)
from src.config import build_config
from src.graph import (
    DependencyGraph,
    build_subgraph,
    load_test_graph,
    print_graph,
)
from src.order import (
    load_order,
    print_load_order,
)


def build_cargo_graph(
    package: str,
    dependencies: list[Dependency],
) -> DependencyGraph:
    """Build a graph from direct Cargo dependencies."""
    graph = DependencyGraph()

    for dependency in dependencies:
        graph.add_edge(
            package,
            dependency.name,
        )

    return graph


def main() -> int:
    """Run the command-line application."""
    config = build_config(sys.argv[1:])

    for key, value in config.as_dict().items():
        print(f"{key}={value}")

    print()

    if config.test_mode:
        try:
            graph = load_test_graph(
                config.source
            )
        except (OSError, ValueError) as error:
            print(f"Error: {error}")
            return 1
    else:
        try:
            dependencies = (
                fetch_direct_dependencies(
                    config.package
                )
            )
        except Exception as error:
            print(f"Error: {error}")
            return 1

        print_direct_dependencies(
            config.package,
            dependencies,
        )
        print()

        graph = build_cargo_graph(
            config.package,
            dependencies,
        )

    try:
        subgraph = build_subgraph(
            graph,
            config.package,
            config.max_depth,
            config.package_filter,
        )

        order = load_order(
            subgraph,
            config.package,
        )
    except ValueError as error:
        print(f"Error: {error}")
        return 1

    print_graph(subgraph)
    print()
    print_load_order(order)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())