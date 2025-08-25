"""Console output formatter implementation."""

from __future__ import annotations

from collections.abc import Sequence

from email_task.shared import domain as _domain
from email_task.shared import result as _result


class ConsoleFormatter:
    """Formatter for console output in the required format."""

    def write_pairs_result(
        self, result: _result.Result[Sequence[_domain.SumGroup]]
    ) -> None:
        """Write the pairs result to console output.

        Args:
            result: Result containing sequence of SumGroups or error.
        """
        self._print_result(_result.map(result, self._create_output_message))

    def _create_output_message(self, sum_groups: Sequence[_domain.SumGroup]) -> str:
        """Create output message from sum groups.

        Args:
            sum_groups: Sequence of SumGroups to format.

        Returns:
            Formatted output string.
        """
        match sum_groups:
            case []:
                return "No pairs with the same sum found."
            case sequence:
                return "\n".join(
                    self._format_sum_group(sum_group) for sum_group in sequence
                )

    def _format_sum_group(self, sum_group: _domain.SumGroup) -> str:
        """Format a single sum group to string.

        Args:
            sum_group: SumGroup containing pairs with same sum value.

        Returns:
            Formatted string representation of the sum group.
        """
        pairs_str = " ".join(f"({pair.left}, {pair.right})" for pair in sum_group.pairs)
        return f"Pairs : {pairs_str} have sum : {sum_group.sum_value}"

    def _print_result(self, result: _result.Result[str]) -> None:
        """Print the formatted result or error message.

        Args:
            result: Result containing formatted string or error.
        """
        match result:
            case _result.Error(message, _):
                print(f"Error: {message}")
            case output:
                print(output)
