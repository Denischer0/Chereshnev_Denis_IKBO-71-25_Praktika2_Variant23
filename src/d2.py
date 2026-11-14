"""D2 diagram generation."""

from src.graph import DependencyGraph


def render_d2(graph: DependencyGraph) -> str:
    """Render a dependency graph as D2 source code."""
    if not graph.adjacency:
        return "direction: right\n"

    lines = ["direction: right"]

    for source, targets in sorted(graph.adjacency.items()):
        if not targets:
            lines.append(f"{source}")
            continue

        for target in sorted(targets):
            lines.append(f"{source} -> {target}")

    return "\n".join(lines) + "\n"


def print_graph(graph: DependencyGraph) -> None:
    """Print the D2 representation to stdout."""
    print(render_d2(graph))