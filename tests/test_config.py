"""Tests for command-line configuration."""

import pytest

from src.config import build_config


def test_build_config_returns_valid_configuration() -> None:
    config = build_config(
        [
            "--package", "serde",
            "--source", "https://crates.io",
            "--max-depth", "3",
            "--filter", "dev",
        ]
    )

    assert config.package == "serde"
    assert config.source == "https://crates.io"
    assert config.test_mode is False
    assert config.max_depth == 3
    assert config.package_filter == "dev"


def test_empty_package_is_invalid() -> None:
    with pytest.raises(SystemExit):
        build_config(
            [
                "--package", "",
                "--source", "https://crates.io",
                "--max-depth", "3",
            ]
        )


def test_invalid_url_is_rejected() -> None:
    with pytest.raises(SystemExit):
        build_config(
            [
                "--package", "serde",
                "--source", "not-a-url",
                "--max-depth", "3",
            ]
        )


def test_zero_depth_is_rejected() -> None:
    with pytest.raises(SystemExit):
        build_config(
            [
                "--package", "serde",
                "--source", "https://crates.io",
                "--max-depth", "0",
            ]
        )