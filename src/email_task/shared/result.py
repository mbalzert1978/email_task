"""Utility functions for safe operation handling with Result types."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, runtime_checkable

type Result[T] = T | Error
"""Monadic result type representing success (T) or failure (Error)."""


@runtime_checkable
class Error(Protocol):
    """Protocol for error types with structural pattern matching support."""

    __match_args__ = ("message", "code")

    @property
    def message(self) -> str:
        """Get the human-readable error message."""
        ...

    @property
    def code(self) -> str:
        """Get the machine-readable error code for programmatic handling."""
        ...


def as_result[T](
    operation: Callable[[], T],
    err: Error,
    exc: type[Exception] | tuple[type[Exception], ...],
) -> Result[T]:
    """Execute operation safely and wrap specified exceptions in Result type.

    Executes the given operation and catches the specified exception type,
    returning either the successful result or the provided error instance.

    Args:
        operation: Zero-argument callable that returns a value of type T.
        err: Error instance to return if the specified exception is raised.
        exc: Exception type or tuple of types to catch and convert to error.

    Returns:
        Either the operation result (T) or the provided error instance.

    Raises:
        Any exception other than the specified type will propagate.

    Example:
        >>> from email_task.shared import errors as _errors
        >>> error = _errors.ApplicationErrorFactory.parse_error("Invalid number")
        >>> result = as_result(lambda: int("42"), error, ValueError)
        >>> isinstance(result, int)
        True
        >>> result = as_result(lambda: int("abc"), error, ValueError)
        >>> isinstance(result, Error)
        True
        >>> match result:
        ...     case Error(msg, code):
        ...         print(f"Error: {msg} ({code})")
        ...     case int() as value:
        ...         print(f"Success: {value}")
    """
    try:
        return operation()
    except exc:
        return err


def bind[T, U](result: Result[T], operation: Callable[[T], Result[U]]) -> Result[U]:
    """Chain Result-returning operations in monadic bind pattern.

    If the input result contains a value, applies the operation to that value.
    If the input result contains an error, propagates the error without
    executing the operation.

    Args:
        result: Result containing either a value of type T or an error.
        operation: Function that takes T and returns Result[U].

    Returns:
        Result containing either the operation result or the original error.

    Example:
        >>> from email_task.shared import errors as _errors
        >>> parse_err = _errors.ApplicationErrorFactory.parse_error("Invalid")
        >>> add_err = _errors.ApplicationErrorFactory.processing_error("Add failed")
        >>> r1 = as_result(lambda: int("42"), parse_err, ValueError)
        >>> r2 = bind(r1, lambda x: as_result(lambda: x + 1, add_err, ValueError))
        >>> isinstance(r2, int)
        True
        >>> match r2:
        ...     case Error(msg, code):
        ...         print(f"Error: {msg}")
        ...     case int() as value:
        ...         print(f"Result: {value}")
    """
    match result:
        case Error():
            return result
        case value:
            return operation(value)


def map[T, U](result: Result[T], operation: Callable[[T], U]) -> Result[U]:
    """Transform the value inside a Result using monadic map pattern.

    If the input result contains a value, applies the transformation function.
    If the input result contains an error, propagates the error without
    executing the transformation.

    Args:
        result: Result containing either a value of type T or an error.
        operation: Pure function that transforms T to U.

    Returns:
        Result containing either the transformed value or the original error.

    Example:
        >>> from email_task.shared import errors as _errors
        >>> error = _errors.ApplicationErrorFactory.parse_error("Invalid")
        >>> r1 = as_result(lambda: int("42"), error, ValueError)
        >>> r2 = map(r1, lambda x: x * 2)
        >>> isinstance(r2, int)
        True
        >>> match r2:
        ...     case Error(msg, code):
        ...         print(f"Error: {msg}")
        ...     case int() as value:
        ...         print(f"Result: {value}")
    """
    match result:
        case Error():
            return result
        case value:
            return operation(value)
