"""Complete find pairs feature handler."""

from __future__ import annotations

from email_task.features.find_pairs import formatter as _formatter
from email_task.features.find_pairs import parser as _parser
from email_task.features.find_pairs import strategies as _strategies
from email_task.shared import result as _result


class FindPairsHandler:
    """Handler for the complete find pairs feature."""

    def __init__(
        self,
        parser: _parser.CommandLineParser | None = None,
        strategy: _strategies.IndexBasedStrategy | None = None,
        formatter: _formatter.ConsoleFormatter | None = None,
    ) -> None:
        """Initialize with optional dependencies for testing."""
        self._parser = parser or _parser.CommandLineParser()
        self._strategy = strategy or _strategies.IndexBasedStrategy()
        self._formatter = formatter or _formatter.ConsoleFormatter()

    def execute(self) -> None:
        """Execute the complete find pairs workflow."""
        # Monadic pipeline: parse -> find_pairs -> output
        self._formatter.write_pairs_result(
            _result.bind(
                self._parser.parse_integer_sequence(),
                self._strategy.collect_sum_pairs,
            )
        )
