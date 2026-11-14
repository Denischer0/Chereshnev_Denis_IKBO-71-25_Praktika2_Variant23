"""Tests for Cargo dependency output."""

from src.cargo import Dependency, print_direct_dependencies


def test_print_direct_dependencies(capsys) -> None:
    dependencies = [
        Dependency(
            name="serde_derive",
            kind="normal",
            optional=False,
        ),
    ]

    print_direct_dependencies(
        "serde",
        dependencies,
    )

    output = capsys.readouterr().out

    assert "Direct dependencies of serde:" in output
    assert "serde_derive [normal]" in output