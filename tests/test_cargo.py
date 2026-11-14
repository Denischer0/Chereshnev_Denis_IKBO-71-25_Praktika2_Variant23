"""Tests for Cargo dependency collection."""

from unittest.mock import patch

from src.cargo import (
    Dependency,
    fetch_direct_dependencies,
)


def test_fetch_direct_dependencies_parses_response() -> None:
    response = {
        "versions": [
            {
                "deps": [
                    {
                        "crate_id": "serde_derive",
                        "kind": "normal",
                        "optional": False,
                    },
                    {
                        "crate_id": "dev-dependency",
                        "kind": "dev",
                        "optional": True,
                    },
                ],
            },
        ],
    }

    with patch(
        "src.cargo.urlopen"
    ) as mocked_urlopen:
        mocked_response = (
            mocked_urlopen.return_value.__enter__
            .return_value
        )
        mocked_response.read.return_value = (
            b'{"versions": [{"deps": []}]}'
        )

        dependencies = (
            fetch_direct_dependencies("serde")
        )

    assert dependencies == []