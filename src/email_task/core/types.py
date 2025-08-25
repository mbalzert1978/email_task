"""Common type definitions and result types."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from email_task.shared import domain as _domain
from email_task.shared import result as _result


class InputReader(Protocol):
    """Protocol for reading input data."""

    def parse_integer_sequence(self) -> _result.Result[Sequence[int]]:
        """Read an array of integers from input source.

        Returns:
            Result containing ParsedArguments or validation/parse error.
        """
        ...


class OutputWriter(Protocol):
    """Protocol for writing output data."""

    def write_pairs_result(
        self, result: _result.Result[Sequence[_domain.SumGroup]]
    ) -> None:
        """Write the pairs result to output destination.

        Args:
            result: Result containing sequence of SumGroups or error.
        """
        ...


class PairFindingStrategy(Protocol):
    """Protocol for pair finding strategies."""

    def collect_sum_pairs(
        self, numbers: Sequence[int]
    ) -> _result.Result[Sequence[_domain.SumGroup]]:
        """Find all pairs with the same sum in the given array.

        Args:
            numbers: Sequence of integers to find pairs in.

        Returns:
            Result containing sequence of SumGroups, where each group contains
            pairs with the same sum value.
        """
        ...
