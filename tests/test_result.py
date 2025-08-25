"""Tests for Result utility functions - as_result, bind, and map."""

from __future__ import annotations

import pytest

from email_task.shared import errors as _errors
from email_task.shared import result as _result


def test_as_result_when_operation_succeeds_should_return_value() -> None:
    """Test as_result with successful operation."""
    error = _errors.ApplicationErrorFactory.generic_error()
    result = _result.as_result(lambda: 42, error, ValueError)

    assert not isinstance(result, _result.Error)
    assert result == 42


def test_as_result_when_value_error_raised_should_return_error() -> None:
    """Test as_result with ValueError."""
    error = _errors.ApplicationErrorFactory.invalid_argument_error()
    result = _result.as_result(lambda: int("abc"), error, ValueError)

    assert isinstance(result, _result.Error)
    assert result.message == _errors.ErrorMessages.INVALID_ARGUMENT_ERROR
    assert result.code == _errors.ErrorCodes.PARSE_ERROR


def test_as_result_when_different_exception_raised_should_propagate() -> None:
    """Test as_result with exception not in catch list."""
    error = _errors.ApplicationErrorFactory.generic_error()

    def divide_by_zero() -> float:
        return 10 / 0

    # ZeroDivisionError not in catch list, should propagate
    with pytest.raises(ZeroDivisionError):
        _result.as_result(divide_by_zero, error, ValueError)


def test_as_result_when_multiple_exception_types_should_catch_any() -> None:
    """Test as_result with multiple exception types."""
    error = _errors.ApplicationErrorFactory.generic_error()

    # Test ValueError
    result1 = _result.as_result(lambda: int("abc"), error, (ValueError, TypeError))
    assert isinstance(result1, _result.Error)

    # Test TypeError
    result2 = _result.as_result(lambda: int(None), error, (ValueError, TypeError))
    assert isinstance(result2, _result.Error)


def test_as_result_when_string_parsing_succeeds_should_return_parsed_value() -> None:
    """Test as_result with successful string parsing."""
    error = _errors.ApplicationErrorFactory.invalid_argument_error()
    result = _result.as_result(lambda: int("123"), error, ValueError)

    assert result == 123
    assert not isinstance(result, _result.Error)


def test_as_result_when_string_parsing_fails_should_return_error() -> None:
    """Test as_result with failed string parsing."""
    error = _errors.ApplicationErrorFactory.invalid_argument_error()
    result = _result.as_result(lambda: int("not_a_number"), error, ValueError)

    assert isinstance(result, _result.Error)
    assert result.message == _errors.ErrorMessages.INVALID_ARGUMENT_ERROR


def test_bind_when_both_operations_succeed_should_return_final_value() -> None:
    """Test bind with successful operation chain."""
    parse_error = _errors.ApplicationErrorFactory.invalid_argument_error()
    multiply_error = _errors.ApplicationErrorFactory.generic_error()

    initial = _result.as_result(lambda: 10, parse_error, ValueError)
    result = _result.bind(
        initial, lambda x: _result.as_result(lambda: x * 2, multiply_error, ValueError)
    )

    assert not isinstance(result, _result.Error)
    assert result == 20


def test_bind_when_initial_operation_fails_should_propagate_error() -> None:
    """Test bind when initial result is an error."""
    parse_error = _errors.ApplicationErrorFactory.invalid_argument_error()
    multiply_error = _errors.ApplicationErrorFactory.generic_error()

    initial = _result.as_result(lambda: int("abc"), parse_error, ValueError)
    result = _result.bind(
        initial, lambda x: _result.as_result(lambda: x * 2, multiply_error, ValueError)
    )

    assert isinstance(result, _result.Error)
    assert result.message == _errors.ErrorMessages.INVALID_ARGUMENT_ERROR
    assert result.code == _errors.ErrorCodes.PARSE_ERROR


def test_bind_when_bound_operation_fails_should_return_bound_error() -> None:
    """Test bind when the bound operation fails."""
    initial_error = _errors.ApplicationErrorFactory.generic_error()
    parse_error = _errors.ApplicationErrorFactory.invalid_argument_error()

    initial = _result.as_result(lambda: 10, initial_error, ValueError)
    result = _result.bind(
        initial,
        lambda x: _result.as_result(lambda: int("abc"), parse_error, ValueError),
    )

    assert isinstance(result, _result.Error)
    assert result.message == _errors.ErrorMessages.INVALID_ARGUMENT_ERROR


def test_bind_when_complex_chain_succeeds_should_return_final_value() -> None:
    """Test bind with multiple chained operations."""
    parse_error = _errors.ApplicationErrorFactory.invalid_argument_error()
    multiply_error = _errors.ApplicationErrorFactory.generic_error()
    add_error = _errors.ApplicationErrorFactory.generic_error()

    initial = _result.as_result(lambda: "42", parse_error, ValueError)

    result = _result.bind(
        initial,
        lambda s: _result.bind(
            _result.as_result(lambda: int(s), parse_error, ValueError),
            lambda i: _result.bind(
                _result.as_result(lambda: i * 2, multiply_error, ValueError),
                lambda doubled: _result.as_result(
                    lambda: doubled + 1, add_error, ValueError
                ),
            ),
        ),
    )

    assert not isinstance(result, _result.Error)
    assert result == 85  # (42 * 2) + 1


def test_bind_when_chain_has_early_error_should_propagate_first_error() -> None:
    """Test that errors propagate through bind chains."""
    initial_error = _errors.ApplicationErrorFactory.invalid_argument_error()
    multiply_error = _errors.ApplicationErrorFactory.generic_error()
    add_error = _errors.ApplicationErrorFactory.generic_error()

    initial = _result.as_result(lambda: int("invalid"), initial_error, ValueError)

    result = _result.bind(
        initial,
        lambda x: _result.bind(
            _result.as_result(lambda: x * 2, multiply_error, ValueError),
            lambda y: _result.as_result(lambda: y + 1, add_error, ValueError),
        ),
    )

    assert isinstance(result, _result.Error)
    assert result.message == _errors.ErrorMessages.INVALID_ARGUMENT_ERROR


def test_map_when_operation_succeeds_should_return_transformed_value() -> None:
    """Test map with successful transformation."""
    error = _errors.ApplicationErrorFactory.generic_error()
    initial = _result.as_result(lambda: 10, error, ValueError)
    result = _result.map(initial, lambda x: x * 2)

    assert not isinstance(result, _result.Error)
    assert result == 20


def test_map_when_initial_is_error_should_propagate_error() -> None:
    """Test map when initial result is an error."""
    error = _errors.ApplicationErrorFactory.invalid_argument_error()
    initial = _result.as_result(lambda: int("abc"), error, ValueError)
    result = _result.map(initial, lambda x: x * 2)

    assert isinstance(result, _result.Error)
    assert result.message == _errors.ErrorMessages.INVALID_ARGUMENT_ERROR


def test_map_when_type_transformation_should_return_new_type() -> None:
    """Test map with type transformation."""
    error = _errors.ApplicationErrorFactory.generic_error()
    initial = _result.as_result(lambda: 42, error, ValueError)
    result = _result.map(initial, lambda x: str(x))

    assert not isinstance(result, _result.Error)
    assert result == "42"
    assert isinstance(result, str)


def test_map_when_chained_should_apply_all_transformations() -> None:
    """Test chaining multiple map operations."""
    error = _errors.ApplicationErrorFactory.generic_error()
    initial = _result.as_result(lambda: 10, error, ValueError)

    result = _result.map(
        _result.map(
            _result.map(initial, lambda x: x * 2),  # 20
            lambda x: x + 5,  # 25
        ),
        lambda x: str(x),  # "25"
    )

    assert not isinstance(result, _result.Error)
    assert result == "25"
    assert isinstance(result, str)


def test_map_when_complex_transformation_should_compute_correctly() -> None:
    """Test map with complex transformation function."""
    error = _errors.ApplicationErrorFactory.generic_error()
    initial = _result.as_result(lambda: [1, 2, 3, 4, 5], error, ValueError)
    result = _result.map(initial, lambda lst: sum(x * x for x in lst))

    assert not isinstance(result, _result.Error)
    assert result == 55  # 1 + 4 + 9 + 16 + 25


def test_bind_and_map_when_combined_should_work_together() -> None:
    """Test combining bind and map operations."""
    parse_error = _errors.ApplicationErrorFactory.invalid_argument_error()
    convert_error = _errors.ApplicationErrorFactory.generic_error()

    initial = _result.as_result(lambda: "10", parse_error, ValueError)

    result = _result.bind(
        initial,
        lambda s: _result.map(
            _result.as_result(lambda: int(s), convert_error, ValueError),
            lambda i: i * 2,
        ),
    )

    assert not isinstance(result, _result.Error)
    assert result == 20


def test_complex_workflow_when_all_succeed_should_return_formatted_result() -> None:
    """Test a complex workflow combining all operations."""
    parse_error = _errors.ApplicationErrorFactory.invalid_argument_error()
    calc_error = _errors.ApplicationErrorFactory.generic_error()

    args = ["10", "20", "30"]

    def parse_args(args_list: list[str]) -> list[int]:
        return [int(arg) for arg in args_list]

    def calculate_average(numbers: list[int]) -> float:
        return sum(numbers) / len(numbers)

    result = _result.bind(
        _result.as_result(lambda: parse_args(args), parse_error, ValueError),
        lambda numbers: _result.map(
            _result.as_result(
                lambda: calculate_average(numbers), calc_error, ValueError
            ),
            lambda avg: f"Average: {avg:.2f}",
        ),
    )

    assert not isinstance(result, _result.Error)
    assert result == "Average: 20.00"


def test_complex_workflow_when_parsing_fails_should_return_parse_error() -> None:
    """Test error handling in complex workflow."""
    parse_error = _errors.ApplicationErrorFactory.invalid_argument_error()
    calc_error = _errors.ApplicationErrorFactory.generic_error()

    args = ["10", "invalid", "30"]

    def parse_args(args_list: list[str]) -> list[int]:
        return [int(arg) for arg in args_list]

    result = _result.bind(
        _result.as_result(lambda: parse_args(args), parse_error, ValueError),
        lambda numbers: _result.map(
            _result.as_result(
                lambda: sum(numbers) / len(numbers), calc_error, ValueError
            ),
            lambda avg: f"Average: {avg:.2f}",
        ),
    )

    assert isinstance(result, _result.Error)
    assert result.message == _errors.ErrorMessages.INVALID_ARGUMENT_ERROR
    assert result.code == _errors.ErrorCodes.PARSE_ERROR


def test_as_result_when_different_types_should_preserve_type() -> None:
    """Test that as_result works with different types."""
    error = _errors.ApplicationErrorFactory.generic_error()

    # String result
    str_result = _result.as_result(lambda: "hello", error, ValueError)
    assert str_result == "hello"

    # List result
    list_result = _result.as_result(lambda: [1, 2, 3], error, ValueError)
    assert list_result == [1, 2, 3]

    # Dict result
    dict_result = _result.as_result(lambda: {"key": "value"}, error, ValueError)
    assert dict_result == {"key": "value"}


def test_bind_when_type_transformations_should_transform_correctly() -> None:
    """Test bind with type transformations."""
    error = _errors.ApplicationErrorFactory.generic_error()

    # int -> str -> list
    result = _result.bind(
        _result.as_result(lambda: 42, error, ValueError),
        lambda x: _result.bind(
            _result.as_result(lambda: str(x), error, ValueError),
            lambda s: _result.as_result(lambda: list(s), error, ValueError),
        ),
    )

    assert not isinstance(result, _result.Error)
    assert result == ["4", "2"]


def test_error_match_args_when_pattern_matching_should_destructure() -> None:
    """Test that errors support structural pattern matching."""
    error = _errors.ApplicationErrorFactory.invalid_argument_error()
    result = _result.as_result(lambda: int("abc"), error, ValueError)

    match result:
        case _result.Error(msg, code):
            assert msg == str(_errors.ErrorMessages.INVALID_ARGUMENT_ERROR)
            assert code == str(_errors.ErrorCodes.PARSE_ERROR)
        case _:
            pytest.fail("Expected Error but got success value")
