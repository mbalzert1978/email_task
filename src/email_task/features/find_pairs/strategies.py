"""Pair finding strategies implementation."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from itertools import combinations

from email_task.shared import domain as _domain
from email_task.shared import result as _result


class IndexBasedStrategy:
    """Version 2: Index-based pair finding strategy following SOLID principles."""

    def collect_sum_pairs(
        self, array: Sequence[int]
    ) -> _result.Result[Sequence[_domain.SumGroup]]:
        """Find all pairs with the same sum using index-based approach.

        Args:
            array: Sequence of integers to find pairs in.

        Returns:
            Result containing Sequence of SumGroups or validation/processing error.
        """
        return _result.bind(
            self._generate_all_pairs(array),
            lambda pairs: _result.bind(
                self._group_by_sum(pairs), self._filter_valid_groups
            ),
        )

    def _generate_all_pairs(
        self, array: Sequence[int]
    ) -> _result.Result[Sequence[_domain.Pair]]:
        """Generate all possible pairs from array indices.

        Single Responsibility: Only pair generation logic.
        """
        pairs: list[_domain.Pair] = []

        for (i, val1), (j, val2) in combinations(enumerate(array), 2):
            match _domain.PairFactory.create(val1, val2, i, j):
                case _domain.Pair() as pair:
                    pairs.append(pair)
                case error:
                    return error

        return tuple(pairs)

    def _group_by_sum(
        self, pairs: Sequence[_domain.Pair]
    ) -> _result.Result[dict[int, Sequence[_domain.Pair]]]:
        """Group pairs by their sum values.

        Single Responsibility: Only grouping logic.
        """

        sum_groups: dict[int, list[_domain.Pair]] = defaultdict(list)

        for pair in pairs:
            sum_groups[pair.sum].append(pair)

        return {sum_val: tuple(pair_list) for sum_val, pair_list in sum_groups.items()}

    def _filter_valid_groups(
        self, grouped_pairs: dict[int, Sequence[_domain.Pair]]
    ) -> _result.Result[Sequence[_domain.SumGroup]]:
        """Create valid SumGroups from grouped pairs.

        Single Responsibility: Only SumGroup creation and filtering.
        """
        valid_groups: list[_domain.SumGroup] = []

        for sum_value, pairs in grouped_pairs.items():
            match _domain.SumGroupFactory.create(sum_value, pairs):
                case _domain.SumGroup() as sum_group:
                    valid_groups.append(sum_group)
                case _result.Error():
                    # Skip invalid groups (e.g., < 2 pairs) - this is expected behavior
                    continue

        # Sort for consistent output (could be extracted to a separate concern)
        sorted_groups = sorted(valid_groups, key=lambda group: group.sum_value)
        return tuple(sorted_groups)
