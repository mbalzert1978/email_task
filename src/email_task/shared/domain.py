"""Shared domain entities and error types."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from email_task.shared import errors as _errors
from email_task.shared import result as _result


@dataclass(frozen=True, slots=True)
class Indices:
    """Represents a pair of indices in an array."""

    left_index: int
    right_index: int


class IndicesFactory:
    """Factory for creating Indices."""

    @staticmethod
    def create(left_index: int, right_index: int) -> _result.Result[Indices]:
        """Create indices with validation.

        Args:
            left_index: Index of the left element in the array.
            right_index: Index of the right element in the array.

        Returns:
            Result containing Indices or validation error.
        """
        match (left_index, right_index):
            case (left, right) if left < 0 or right < 0:
                return _errors.ApplicationErrorFactory.negative_index_error()
            case (left, right) if left == right:
                return _errors.ApplicationErrorFactory.equal_indices_error()
            case (left, right):
                return Indices(left_index=left, right_index=right)


@dataclass(frozen=True, slots=True)
class Pair:
    """Represents a pair of values from array indices."""

    left: int
    right: int
    indices: Indices

    @property
    def sum(self) -> int:
        """Calculate the sum of the pair values."""
        return self.left + self.right


class PairFactory:
    """Factory for creating pairs."""

    @staticmethod
    def create(
        left: int, right: int, left_index: int, right_index: int
    ) -> _result.Result[Pair]:
        """Create a pair with validation.

        Args:
            left: Value of the left element.
            right: Value of the right element.
            left_index: Index of the left element in the array.
            right_index: Index of the right element in the array.

        Returns:
            Result containing Pair or validation error.
        """
        match (left, right):
            case (None, _) | (_, None):
                return _errors.ApplicationErrorFactory.null_value_error()
            case (left_val, right_val):
                return _result.bind(
                    IndicesFactory.create(left_index, right_index),
                    lambda indices: Pair(
                        left=left_val, right=right_val, indices=indices
                    ),
                )


@dataclass(frozen=True, slots=True)
class SumGroup:
    """Represents a group of pairs that have the same sum."""

    sum_value: int
    pairs: Sequence[Pair]


class SumGroupFactory:
    """Factory for creating sum groups."""

    @staticmethod
    def create(sum_value: int, pairs: Sequence[Pair]) -> _result.Result[SumGroup]:
        """Create a sum group with validation.

        Args:
            sum_value: The sum value that all pairs must have.
            pairs: Sequence of pairs with the same sum.

        Returns:
            Result containing SumGroup or validation error.
        """
        match (sum_value, pairs):
            case (None, _):
                return _errors.ApplicationErrorFactory.null_value_error()
            case (value, _) if value < 0:
                return _errors.ApplicationErrorFactory.negative_value_error()
            case (_, pairs_seq) if len(pairs_seq) < 2:
                return _errors.ApplicationErrorFactory.min_sum_group_error()
            case (value, pairs_seq) if any(pair.sum != value for pair in pairs_seq):
                return _errors.ApplicationErrorFactory.invalid_sum_group_error()
            case (value, pairs_seq):
                return SumGroup(sum_value=value, pairs=pairs_seq)
