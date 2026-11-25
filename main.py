"""Deterministic image entrypoint for the 25 November 2026 news poster."""
from pathlib import Path

from build_poster import create

OUTPUT = Path('/output/entry.png')
# The renderer creates the image from local fonts and vector-like line art.
# Output is stable across runs and requires no network access.


def main():
    """Render the complete contest image to the required output path."""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    create(str(OUTPUT))


if __name__ == '__main__':
    main()
