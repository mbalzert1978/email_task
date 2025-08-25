"""Email Task Library - Unique Pair Sums Application."""

from __future__ import annotations

from email_task.features.find_pairs.handler import FindPairsHandler


def main() -> None:
    """Main application entry point."""
    handler = FindPairsHandler()
    handler.execute()


__all__ = ["main", "FindPairsHandler"]
