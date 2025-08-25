"""Command line input parser implementation."""

from __future__ import annotations

import sys
from typing import Sequence

from email_task.shared import errors as _errors
from email_task.shared import result as _result


class CommandLineParser:
    """Parser for command line arguments."""

    def parse_integer_sequence(self) -> _result.Result[Sequence[int]]:
        """Parse command line arguments into integer sequence.

        Returns:
            Result containing ParsedArguments or validation/parse error.

        Raises:
            Any exception other than ValueError and TypeError will propagate.
        """
        match sys.argv:
            case [_, *args]:
                return _result.bind(
                    _result.as_result(
                        lambda: tuple(int(arg) for arg in args),
                        _errors.ApplicationErrorFactory.invalid_argument_error(),
                        (ValueError, TypeError),
                    ),
                    lambda values: values
                    if len(values) >= 2
                    else _errors.ApplicationErrorFactory.min_arg_error(),
                )
            case [_]:
                return _errors.ApplicationErrorFactory.no_arguments_error()
            case _:
                return _errors.ApplicationErrorFactory.min_arg_error()
