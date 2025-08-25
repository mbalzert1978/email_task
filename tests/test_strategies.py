"""Tests for IndexBasedStrategy pair finding implementation."""

from __future__ import annotations

from email_task.features.find_pairs import strategies as _strategies
from email_task.shared import domain as _domain
from email_task.shared import result as _result


def test_collect_sum_pairs_when_example_array_should_return_correct_sum_groups() -> (
    None
):
    """Test IndexBasedStrategy with the example from the task."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [6, 4, 12, 10, 22, 54, 32, 42, 21, 11]

    # Expected pairs for sum 16 (from task specification)
    pair1 = _domain.PairFactory.create(6, 10, 0, 3)
    pair2 = _domain.PairFactory.create(4, 12, 1, 2)
    expected_pairs_for_sum_16 = (pair1, pair2)

    # Expected pairs for sum 32 (from task specification)
    pair3 = _domain.PairFactory.create(10, 22, 3, 4)
    pair4 = _domain.PairFactory.create(21, 11, 8, 9)
    expected_pairs_for_sum_32 = (pair3, pair4)

    # Expected pairs for sum 33 (from task specification)
    pair5 = _domain.PairFactory.create(12, 21, 2, 8)
    pair6 = _domain.PairFactory.create(22, 11, 4, 9)
    expected_pairs_for_sum_33 = (pair5, pair6)

    # Expected pairs for sum 43 (from task specification)
    pair7 = _domain.PairFactory.create(22, 21, 4, 8)
    pair8 = _domain.PairFactory.create(32, 11, 6, 9)
    expected_pairs_for_sum_43 = (pair7, pair8)

    # Expected pairs for sum 53 (from task specification)
    pair9 = _domain.PairFactory.create(32, 21, 6, 8)
    pair10 = _domain.PairFactory.create(42, 11, 7, 9)
    expected_pairs_for_sum_53 = (pair9, pair10)

    # Expected pairs for sum 54 (from task specification)
    pair11 = _domain.PairFactory.create(12, 42, 2, 7)
    pair12 = _domain.PairFactory.create(22, 32, 4, 6)
    expected_pairs_for_sum_54 = (pair11, pair12)

    # Expected pairs for sum 64 (from task specification)
    pair13 = _domain.PairFactory.create(10, 54, 3, 5)
    pair14 = _domain.PairFactory.create(22, 42, 4, 7)
    expected_pairs_for_sum_64 = (pair13, pair14)

    sum_group_16 = _domain.SumGroupFactory.create(16, expected_pairs_for_sum_16)
    sum_group_32 = _domain.SumGroupFactory.create(32, expected_pairs_for_sum_32)
    sum_group_33 = _domain.SumGroupFactory.create(33, expected_pairs_for_sum_33)
    sum_group_43 = _domain.SumGroupFactory.create(43, expected_pairs_for_sum_43)
    sum_group_53 = _domain.SumGroupFactory.create(53, expected_pairs_for_sum_53)
    sum_group_54 = _domain.SumGroupFactory.create(54, expected_pairs_for_sum_54)
    sum_group_64 = _domain.SumGroupFactory.create(64, expected_pairs_for_sum_64)

    # These are exactly the 7 sum groups from the task specification
    expected = (
        sum_group_16,
        sum_group_32,
        sum_group_33,
        sum_group_43,
        sum_group_53,
        sum_group_54,
        sum_group_64,
    )

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_simple_array_should_return_one_sum_group() -> None:
    """Test IndexBasedStrategy with simple array having one sum group."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [1, 3, 2, 4]

    # All possible pairs and their sums:
    # 1 + 3 = 4 (indices 0,1)
    # 1 + 2 = 3 (indices 0,2)
    # 1 + 4 = 5 (indices 0,3)
    # 3 + 2 = 5 (indices 1,2)
    # 3 + 4 = 7 (indices 1,3)
    # 2 + 4 = 6 (indices 2,3)

    # Sum groups with at least 2 pairs:
    # Sum 5: (1,4) and (3,2)
    pair1 = _domain.PairFactory.create(1, 4, 0, 3)
    pair2 = _domain.PairFactory.create(3, 2, 1, 2)
    expected_pairs = (pair1, pair2)
    sum_group = _domain.SumGroupFactory.create(5, expected_pairs)
    expected = (sum_group,)

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_no_matching_sums_should_return_empty_sequence() -> None:
    """Test IndexBasedStrategy with array having no matching sums."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [1, 2, 4, 8]
    expected = ()

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_duplicate_values_should_treat_indices_separately() -> (
    None
):
    """Test IndexBasedStrategy treats duplicate values as separate by index."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [2, 2, 2, 2]

    pair1 = _domain.PairFactory.create(2, 2, 0, 1)
    pair2 = _domain.PairFactory.create(2, 2, 0, 2)
    pair3 = _domain.PairFactory.create(2, 2, 0, 3)
    pair4 = _domain.PairFactory.create(2, 2, 1, 2)
    pair5 = _domain.PairFactory.create(2, 2, 1, 3)
    pair6 = _domain.PairFactory.create(2, 2, 2, 3)
    expected_pairs = (pair1, pair2, pair3, pair4, pair5, pair6)
    sum_group = _domain.SumGroupFactory.create(4, expected_pairs)
    expected = (sum_group,)

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_two_elements_should_return_empty_for_no_groups() -> (
    None
):
    """Test IndexBasedStrategy with two elements that don't form groups."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [1, 2]
    expected = ()

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_multiple_sum_groups_should_return_sorted_by_sum() -> (
    None
):
    """Test IndexBasedStrategy returns sum groups sorted by sum value."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [1, 5, 2, 4, 3, 3]

    # All possible pairs and their sums:
    # 1 + 5 = 6 (indices 0,1)
    # 1 + 2 = 3 (indices 0,2)
    # 1 + 4 = 5 (indices 0,3)
    # 1 + 3 = 4 (indices 0,4)
    # 1 + 3 = 4 (indices 0,5)
    # 5 + 2 = 7 (indices 1,2)
    # 5 + 4 = 9 (indices 1,3)
    # 5 + 3 = 8 (indices 1,4)
    # 5 + 3 = 8 (indices 1,5)
    # 2 + 4 = 6 (indices 2,3)
    # 2 + 3 = 5 (indices 2,4)
    # 2 + 3 = 5 (indices 2,5)
    # 4 + 3 = 7 (indices 3,4)
    # 4 + 3 = 7 (indices 3,5)
    # 3 + 3 = 6 (indices 4,5)

    # Sum groups with at least 2 pairs:
    # Sum 4: (1,3) and (1,3) - indices (0,4) and (0,5)
    # Sum 5: (1,4), (2,3), (2,3) - indices (0,3), (2,4), (2,5)
    # Sum 6: (1,5), (2,4), (3,3) - indices (0,1), (2,3), (4,5)
    # Sum 7: (5,2), (4,3), (4,3) - indices (1,2), (3,4), (3,5)
    # Sum 8: (5,3), (5,3) - indices (1,4), (1,5)

    # Sum 4 group
    pair1_sum4 = _domain.PairFactory.create(1, 3, 0, 4)
    pair2_sum4 = _domain.PairFactory.create(1, 3, 0, 5)
    expected_pairs_sum4 = (pair1_sum4, pair2_sum4)
    sum_group_4 = _domain.SumGroupFactory.create(4, expected_pairs_sum4)

    # Sum 5 group
    pair1_sum5 = _domain.PairFactory.create(1, 4, 0, 3)
    pair2_sum5 = _domain.PairFactory.create(2, 3, 2, 4)
    pair3_sum5 = _domain.PairFactory.create(2, 3, 2, 5)
    expected_pairs_sum5 = (pair1_sum5, pair2_sum5, pair3_sum5)
    sum_group_5 = _domain.SumGroupFactory.create(5, expected_pairs_sum5)

    # Sum 6 group
    pair1_sum6 = _domain.PairFactory.create(1, 5, 0, 1)
    pair2_sum6 = _domain.PairFactory.create(2, 4, 2, 3)
    pair3_sum6 = _domain.PairFactory.create(3, 3, 4, 5)
    expected_pairs_sum6 = (pair1_sum6, pair2_sum6, pair3_sum6)
    sum_group_6 = _domain.SumGroupFactory.create(6, expected_pairs_sum6)

    # Sum 7 group
    pair1_sum7 = _domain.PairFactory.create(5, 2, 1, 2)
    pair2_sum7 = _domain.PairFactory.create(4, 3, 3, 4)
    pair3_sum7 = _domain.PairFactory.create(4, 3, 3, 5)
    expected_pairs_sum7 = (pair1_sum7, pair2_sum7, pair3_sum7)
    sum_group_7 = _domain.SumGroupFactory.create(7, expected_pairs_sum7)

    # Sum 8 group
    pair1_sum8 = _domain.PairFactory.create(5, 3, 1, 4)
    pair2_sum8 = _domain.PairFactory.create(5, 3, 1, 5)
    expected_pairs_sum8 = (pair1_sum8, pair2_sum8)
    sum_group_8 = _domain.SumGroupFactory.create(8, expected_pairs_sum8)

    expected = (sum_group_4, sum_group_5, sum_group_6, sum_group_7, sum_group_8)

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_large_numbers_should_handle_correctly() -> None:
    """Test IndexBasedStrategy with large numbers."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [100, 200, 150, 250]

    pair1 = _domain.PairFactory.create(100, 250, 0, 3)
    pair2 = _domain.PairFactory.create(200, 150, 1, 2)
    expected_pairs = (pair1, pair2)
    sum_group = _domain.SumGroupFactory.create(350, expected_pairs)
    expected = (sum_group,)

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_negative_numbers_should_handle_correctly() -> None:
    """Test IndexBasedStrategy with negative numbers."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [-1, 3, 1, 1]

    # All possible pairs and their sums:
    # -1 + 3 = 2 (indices 0,1)
    # -1 + 1 = 0 (indices 0,2)
    # -1 + 1 = 0 (indices 0,3)
    # 3 + 1 = 4 (indices 1,2)
    # 3 + 1 = 4 (indices 1,3)
    # 1 + 1 = 2 (indices 2,3)

    # Sum groups with at least 2 pairs:
    # Sum 0: (-1,1) and (-1,1) - indices (0,2) and (0,3)
    # Sum 2: (-1,3) and (1,1) - indices (0,1) and (2,3)
    # Sum 4: (3,1) and (3,1) - indices (1,2) and (1,3)

    # Sum 0 group
    pair1_sum0 = _domain.PairFactory.create(-1, 1, 0, 2)
    pair2_sum0 = _domain.PairFactory.create(-1, 1, 0, 3)
    expected_pairs_sum0 = (pair1_sum0, pair2_sum0)
    sum_group_0 = _domain.SumGroupFactory.create(0, expected_pairs_sum0)

    # Sum 2 group
    pair1_sum2 = _domain.PairFactory.create(-1, 3, 0, 1)
    pair2_sum2 = _domain.PairFactory.create(1, 1, 2, 3)
    expected_pairs_sum2 = (pair1_sum2, pair2_sum2)
    sum_group_2 = _domain.SumGroupFactory.create(2, expected_pairs_sum2)

    # Sum 4 group
    pair1_sum4 = _domain.PairFactory.create(3, 1, 1, 2)
    pair2_sum4 = _domain.PairFactory.create(3, 1, 1, 3)
    expected_pairs_sum4 = (pair1_sum4, pair2_sum4)
    sum_group_4 = _domain.SumGroupFactory.create(4, expected_pairs_sum4)

    expected = (sum_group_0, sum_group_2, sum_group_4)

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_mixed_positive_negative_should_return_correct_groups() -> (
    None
):
    """Test IndexBasedStrategy with mixed positive and negative numbers."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [-2, 4, 2, 0]

    pair1 = _domain.PairFactory.create(-2, 4, 0, 1)
    pair2 = _domain.PairFactory.create(2, 0, 2, 3)
    expected_pairs = (pair1, pair2)
    sum_group = _domain.SumGroupFactory.create(2, expected_pairs)
    expected = (sum_group,)

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_zero_values_should_handle_correctly() -> None:
    """Test IndexBasedStrategy with zero values."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [0, 0, 1, -1]

    # All possible pairs and their sums:
    # 0 + 0 = 0 (indices 0,1)
    # 0 + 1 = 1 (indices 0,2)
    # 0 + (-1) = -1 (indices 0,3)
    # 0 + 1 = 1 (indices 1,2)
    # 0 + (-1) = -1 (indices 1,3)
    # 1 + (-1) = 0 (indices 2,3)

    # Sum groups with at least 2 pairs:
    # Sum 0: (0,0) and (1,-1) - indices (0,1) and (2,3)
    # Sum 1: (0,1) and (0,1) - indices (0,2) and (1,2)

    # Sum 0 group (note: cannot have negative sum in SumGroupFactory)
    pair1_sum0 = _domain.PairFactory.create(0, 0, 0, 1)
    pair2_sum0 = _domain.PairFactory.create(1, -1, 2, 3)
    expected_pairs_sum0 = (pair1_sum0, pair2_sum0)
    sum_group_0 = _domain.SumGroupFactory.create(0, expected_pairs_sum0)

    # Sum 1 group
    pair1_sum1 = _domain.PairFactory.create(0, 1, 0, 2)
    pair2_sum1 = _domain.PairFactory.create(0, 1, 1, 2)
    expected_pairs_sum1 = (pair1_sum1, pair2_sum1)
    sum_group_1 = _domain.SumGroupFactory.create(1, expected_pairs_sum1)

    expected = (sum_group_0, sum_group_1)

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_three_elements_same_sum_should_return_one_group() -> (
    None
):
    """Test IndexBasedStrategy with three pairs having the same sum."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [1, 2, 0, 3]

    pair1 = _domain.PairFactory.create(1, 2, 0, 1)
    pair2 = _domain.PairFactory.create(0, 3, 2, 3)
    expected_pairs = (pair1, pair2)
    sum_group = _domain.SumGroupFactory.create(3, expected_pairs)
    expected = (sum_group,)

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_six_elements_multiple_groups_should_return_all_groups() -> (
    None
):
    """Test IndexBasedStrategy with six elements forming multiple groups."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [1, 4, 2, 3, 0, 5]

    # All possible pairs and their sums:
    # 1 + 4 = 5 (indices 0,1)
    # 1 + 2 = 3 (indices 0,2)
    # 1 + 3 = 4 (indices 0,3)
    # 1 + 0 = 1 (indices 0,4)
    # 1 + 5 = 6 (indices 0,5)
    # 4 + 2 = 6 (indices 1,2)
    # 4 + 3 = 7 (indices 1,3)
    # 4 + 0 = 4 (indices 1,4)
    # 4 + 5 = 9 (indices 1,5)
    # 2 + 3 = 5 (indices 2,3)
    # 2 + 0 = 2 (indices 2,4)
    # 2 + 5 = 7 (indices 2,5)
    # 3 + 0 = 3 (indices 3,4)
    # 3 + 5 = 8 (indices 3,5)
    # 0 + 5 = 5 (indices 4,5)

    # Sum groups with at least 2 pairs:
    # Sum 3: (1,2) and (3,0) - indices (0,2) and (3,4)
    # Sum 4: (1,3) and (4,0) - indices (0,3) and (1,4)
    # Sum 5: (1,4), (2,3), (0,5) - indices (0,1), (2,3), (4,5)
    # Sum 6: (1,5) and (4,2) - indices (0,5) and (1,2)
    # Sum 7: (4,3) and (2,5) - indices (1,3) and (2,5)

    # Sum 3 group
    pair1_sum3 = _domain.PairFactory.create(1, 2, 0, 2)
    pair2_sum3 = _domain.PairFactory.create(3, 0, 3, 4)
    expected_pairs_sum3 = (pair1_sum3, pair2_sum3)
    sum_group_3 = _domain.SumGroupFactory.create(3, expected_pairs_sum3)

    # Sum 4 group
    pair1_sum4 = _domain.PairFactory.create(1, 3, 0, 3)
    pair2_sum4 = _domain.PairFactory.create(4, 0, 1, 4)
    expected_pairs_sum4 = (pair1_sum4, pair2_sum4)
    sum_group_4 = _domain.SumGroupFactory.create(4, expected_pairs_sum4)

    # Sum 5 group
    pair1_sum5 = _domain.PairFactory.create(1, 4, 0, 1)
    pair2_sum5 = _domain.PairFactory.create(2, 3, 2, 3)
    pair3_sum5 = _domain.PairFactory.create(0, 5, 4, 5)
    expected_pairs_sum5 = (pair1_sum5, pair2_sum5, pair3_sum5)
    sum_group_5 = _domain.SumGroupFactory.create(5, expected_pairs_sum5)

    # Sum 6 group
    pair1_sum6 = _domain.PairFactory.create(1, 5, 0, 5)
    pair2_sum6 = _domain.PairFactory.create(4, 2, 1, 2)
    expected_pairs_sum6 = (pair1_sum6, pair2_sum6)
    sum_group_6 = _domain.SumGroupFactory.create(6, expected_pairs_sum6)

    # Sum 7 group
    pair1_sum7 = _domain.PairFactory.create(4, 3, 1, 3)
    pair2_sum7 = _domain.PairFactory.create(2, 5, 2, 5)
    expected_pairs_sum7 = (pair1_sum7, pair2_sum7)
    sum_group_7 = _domain.SumGroupFactory.create(7, expected_pairs_sum7)

    expected = (sum_group_3, sum_group_4, sum_group_5, sum_group_6, sum_group_7)

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_empty_array_should_return_empty_sequence() -> None:
    """Test IndexBasedStrategy with empty array."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = []
    expected = ()

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected


def test_collect_sum_pairs_when_single_element_should_return_empty_sequence() -> None:
    """Test IndexBasedStrategy with single element array."""
    # Arrange
    strategy = _strategies.IndexBasedStrategy()
    array = [42]
    expected = ()

    # Act
    result = strategy.collect_sum_pairs(array)

    # Assert
    assert not isinstance(result, _result.Error)
    assert result == expected
