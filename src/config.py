"""Command-line configuration for the dependency graph tool."""

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

MAX_DEPTH = 1_000_000


class ConfigError(ValueError):
    """Raised when a command-line configuration value is invalid."""


@dataclass(frozen=True)
class Config:
    """User-provided settings for dependency analysis."""

    package: str
    source: str
    test_mode: bool
    max_depth: int
    package_filter: str

    def as_dict(self) -> dict[str, str | int | bool]:
        """Return configuration as a key-value mapping."""
        return {
            "package": self.package,
            "source": self.source,
            "test_mode": self.test_mode,
            "max_depth": self.max_depth,
            "package_filter": self.package_filter,
        }


def validate_package(value: str) -> str:
    """Validate a Cargo package name."""
    if not value:
        raise ConfigError("Package name must not be empty")

    return value


def validate_source(value: str, test_mode: bool) -> str:
    """Validate a repository URL or a test graph file path."""
    if not value:
        raise ConfigError(
            "Repository URL or test file path is required"
        )

    if test_mode:
        path = Path(value)

        if not path.is_file():
            raise ConfigError(
                f"Test graph file does not exist: {value}"
            )

        return value

    parsed = urlparse(value)

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ConfigError(f"Invalid repository URL: {value}")

    return value


def validate_depth(value: str) -> int:
    """Validate the maximum dependency traversal depth."""
    try:
        depth = int(value)
    except ValueError as error:
        raise ConfigError(
            f"Maximum depth must be an integer: {value}"
        ) from error

    if depth < 1:
        raise ConfigError("Maximum depth must be at least 1")

    if depth > MAX_DEPTH:
        raise ConfigError(
            f"Maximum depth must not exceed {MAX_DEPTH}"
        )

    return depth


def build_config(arguments: list[str]) -> Config:
    """Parse and validate command-line arguments."""
    parser = ArgumentParser(
        prog="cargo-dependency-graph",
        description=(
            "Configure analysis of Cargo package dependencies"
        ),
    )

    parser.add_argument(
        "--package",
        required=True,
        help="Name of the Cargo package to analyze",
    )

    parser.add_argument(
        "--source",
        required=True,
        help=(
            "Cargo repository URL or path to a test graph file"
        ),
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help=(
            "Treat --source as a local test graph file"
        ),
    )

    parser.add_argument(
        "--max-depth",
        required=True,
        help="Maximum dependency traversal depth",
    )

    parser.add_argument(
        "--filter",
        default="",
        help="Substring used to exclude packages",
    )

    try:
        parsed = parser.parse_args(arguments)

        return Config(
            package=validate_package(parsed.package),
            source=validate_source(
                parsed.source,
                parsed.test,
            ),
            test_mode=parsed.test,
            max_depth=validate_depth(
                parsed.max_depth
            ),
            package_filter=parsed.filter,
        )
    except ConfigError as error:
        parser.error(str(error))