"""Cargo package metadata client."""

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

CARGO_API_URL = "https://crates.io/api/v1/crates"
REQUEST_TIMEOUT = 15


class CargoError(RuntimeError):
    """Raised when Cargo metadata cannot be retrieved."""


@dataclass(frozen=True)
class Dependency:
    """A direct dependency of a Cargo package."""

    name: str
    kind: str
    optional: bool


def fetch_json(url: str) -> dict:
    """Fetch and decode a JSON document."""
    request = Request(
        url,
        headers={"Accept": "application/json"},
    )

    try:
        with urlopen(
            request,
            timeout=REQUEST_TIMEOUT,
        ) as response:
            return json.loads(
                response.read().decode("utf-8")
            )
    except HTTPError as error:
        raise CargoError(
            f"Cargo registry returned "
            f"HTTP error: {error.code}"
        ) from error
    except (URLError, TimeoutError) as error:
        raise CargoError(
            f"Unable to connect to "
            f"Cargo registry: {error}"
        ) from error
    except json.JSONDecodeError as error:
        raise CargoError(
            "Cargo registry returned invalid JSON"
        ) from error


def get_latest_version(
    package: str,
) -> str:
    """Return the latest published version of a package."""
    package_url = (
        f"{CARGO_API_URL}/{quote(package)}"
    )
    payload = fetch_json(package_url)
    versions = payload.get("versions", [])

    if not versions:
        raise CargoError(
            f"Package not found: {package}"
        )

    return versions[0]["num"]


def fetch_direct_dependencies(
    package: str,
) -> list[Dependency]:
    """Fetch direct dependencies of a Cargo package."""
    version = get_latest_version(package)

    dependencies_url = (
        f"{CARGO_API_URL}/"
        f"{quote(package)}/"
        f"{quote(version)}/dependencies"
    )

    payload = fetch_json(dependencies_url)
    items = payload.get("dependencies", [])

    return [
        Dependency(
            name=item["crate_id"],
            kind=item.get("kind", "normal"),
            optional=bool(
                item.get("optional", False)
            ),
        )
        for item in items
    ]


def print_direct_dependencies(
    package: str,
    dependencies: list[Dependency],
) -> None:
    """Print direct dependencies of a package."""
    print(
        f"Direct dependencies of {package}:"
    )

    if not dependencies:
        print("  none")
        return

    for dependency in dependencies:
        print(
            f"  {dependency.name} "
            f"[{dependency.kind}]"
        )