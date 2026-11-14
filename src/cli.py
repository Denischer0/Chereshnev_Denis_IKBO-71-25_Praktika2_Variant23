"""Command-line entry point."""

import sys

from src.config import build_config


def main() -> int:
    """Run the command-line application."""
    config = build_config(sys.argv[1:])

    for key, value in config.as_dict().items():
        print(f"{key}={value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())