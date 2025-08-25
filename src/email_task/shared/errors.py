"""Application error types and error factory."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from email_task.shared import result as _result


class ErrorMessages(StrEnum):
    """Error message constants."""

    GENERIC_ERROR = "An unexpected error occurred."
    # Indices Errors
    NEGATIVE_INDEX_ERROR = "Indices must be positive."
    EQUAL_INDICES_ERROR = "Indices must be different."
    INVALID_INDICES_ERROR = "Invalid indices provided."
    # Value Errors
    NULL_VALUE_ERROR = "Values cannot be null."
    NEGATIVE_VALUE_ERROR = "Values must be positive."
    # Sum Group Errors
    MIN_SUM_GROUP_ERROR = "Sum group must contain at least two pairs."
    INVALID_SUM_GROUP_ERROR = "Sum group contains invalid pairs."
    # Parsing Errors
    NO_ARGUMENTS_ERROR = "No array elements provided. Usage: uv run email-task 6 4 12 10 22 54 32 42 21 11"
    MIN_ARGUMENTS_ERROR = "At least two array elements are required to form pairs."
    INVALID_ARGUMENT_ERROR = "Invalid integer received."


class ErrorCodes(StrEnum):
    """Error code constants."""

    DOMAIN_ERROR = "DomainError"
    PARSE_ERROR = "ParseError"
    VALIDATION_ERROR = "ValidationError"
    PROCESSING_ERROR = "ProcessingError"


@dataclass(frozen=True, slots=True)
class ApplicationError:
    """Base error type for application errors."""

    __match_args__ = ("message", "code")

    message: ErrorMessages
    code: ErrorCodes


class ApplicationErrorFactory:
    """Factory for creating application errors."""

    @staticmethod
    def generic_error() -> _result.Error:
        """Create a generic error."""
        return ApplicationError(
            message=ErrorMessages.GENERIC_ERROR, code=ErrorCodes.VALIDATION_ERROR
        )

    @staticmethod
    def negative_index_error() -> _result.Error:
        """Create an error for negative indices."""
        return ApplicationError(
            message=ErrorMessages.NEGATIVE_INDEX_ERROR, code=ErrorCodes.DOMAIN_ERROR
        )

    @staticmethod
    def equal_indices_error() -> _result.Error:
        """Create an error for equal indices."""
        return ApplicationError(
            message=ErrorMessages.EQUAL_INDICES_ERROR, code=ErrorCodes.DOMAIN_ERROR
        )

    @staticmethod
    def invalid_indices_error() -> _result.Error:
        """Create an error for invalid indices."""
        return ApplicationError(
            message=ErrorMessages.INVALID_INDICES_ERROR, code=ErrorCodes.DOMAIN_ERROR
        )

    @staticmethod
    def null_value_error() -> _result.Error:
        """Create an error for null values."""
        return ApplicationError(
            message=ErrorMessages.NULL_VALUE_ERROR, code=ErrorCodes.DOMAIN_ERROR
        )

    @staticmethod
    def negative_value_error() -> _result.Error:
        """Create an error for negative values."""
        return ApplicationError(
            message=ErrorMessages.NEGATIVE_VALUE_ERROR, code=ErrorCodes.DOMAIN_ERROR
        )

    @staticmethod
    def min_sum_group_error() -> _result.Error:
        """Create an error for sum groups with less than two pairs."""
        return ApplicationError(
            message=ErrorMessages.MIN_SUM_GROUP_ERROR, code=ErrorCodes.DOMAIN_ERROR
        )

    @staticmethod
    def invalid_sum_group_error() -> _result.Error:
        """Create an error for invalid sum groups."""
        return ApplicationError(
            message=ErrorMessages.INVALID_SUM_GROUP_ERROR, code=ErrorCodes.DOMAIN_ERROR
        )

    @staticmethod
    def no_arguments_error() -> _result.Error:
        """Create an error for no command line arguments."""
        return ApplicationError(
            message=ErrorMessages.NO_ARGUMENTS_ERROR, code=ErrorCodes.PARSE_ERROR
        )

    @staticmethod
    def min_arg_error() -> _result.Error:
        """Create an error for insufficient command line arguments."""
        return ApplicationError(
            message=ErrorMessages.MIN_ARGUMENTS_ERROR,
            code=ErrorCodes.PARSE_ERROR,
        )

    @staticmethod
    def invalid_argument_error() -> _result.Error:
        """Create an error for invalid command line argument."""
        return ApplicationError(
            message=ErrorMessages.INVALID_ARGUMENT_ERROR,
            code=ErrorCodes.PARSE_ERROR,
        )
