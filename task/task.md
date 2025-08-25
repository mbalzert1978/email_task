# Email Task - Unique Pair Sums

A console application that finds all unique pairs in an unsorted array that have the same sum.

## Architecture

This project implements a **Vertical Slice Architecture** with the following key design principles:

- **Monadic Error Handling**: Uses `Result[T] = T | IError` for safe error handling without exceptions
- **Protocol-Based Interfaces**: All components implement protocols for maximum extensibility
- **Feature-Oriented Structure**: Each feature is a complete vertical slice
- **Index-Based Strategy**: Version 2 implementation that treats each array position as distinct

## Project Structure

```text
src/
└── email_task/                   # Main library package
    ├── __init__.py              # Package entry point with main()
    ├── __main__.py              # Module execution entry point
    ├── core/
    │   └── types.py             # Core protocols and result types
    ├── shared/
    │   └── domain.py            # Domain entities and error types
    └── features/
        └── find_pairs/          # Complete find pairs feature
            ├── strategies.py    # Pair finding algorithms
            ├── parser.py        # Input parsing
            ├── formatter.py     # Output formatting
            └── handler.py       # Feature orchestration
```

## Development with uv

This project uses [uv](https://docs.astral.sh/uv/) as the package manager for fast dependency management and virtual environment handling.

### Quick Start

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone <repository-url>
cd email_task

# Setup project with uv (creates venv and installs dependencies)
uv sync

# Run the application
uv run email-task 6 4 12 10 22 54 32 42 21 11

# Run tests
uv run pytest tests/ -v

# Add new dependencies
uv add <package-name>

# Add development dependencies  
uv add --dev <package-name>
```

## Usage

### Running the Application

```bash
# Using the installed script command (recommended)
uv run email-task 6 4 12 10 22 54 32 42 21 11

# Using module execution
uv run python -m src.email_task 6 4 12 10 22 54 32 42 21 11

# Direct module execution
uv run -m src.email_task 4 23 65 67 24 12 86
```

### Expected Output

**Example 1:**

```
Pairs : (6, 10) (4, 12) have sum : 16
Pairs : (10, 22) (21, 11) have sum : 32
Pairs : (12, 21) (22, 11) have sum : 33
Pairs : (22, 21) (32, 11) have sum : 43
Pairs : (32, 21) (42, 11) have sum : 53
Pairs : (12, 42) (22, 32) have sum : 54
Pairs : (10, 54) (22, 42) have sum : 64
```

**Example 2:**

```
Pairs : (4, 86) (23, 67) have sum : 90
```

## Error Handling

The application uses monadic error handling with detailed error messages:

```bash
# No arguments
uv run email-task
# Error: No array elements provided. Usage: python main.py 6 4 12 10 22 54

# Invalid input
uv run email-task 5 abc
# Error: Invalid integer at position 2: 'abc'

# Too few elements
uv run email-task 5
# Error: Array must contain at least 2 elements to form pairs
```

## Development

### Running Tests

```bash
uv run pytest tests/ -v
```

### Installing for Development

```bash
# Clone and setup with uv
cd email_task
uv sync

# Run tests
uv run pytest tests/ -v

# Run the application
uv run email-task 6 4 12 10 22 54 32 42 21 11
```

## Algorithm Details

### Index-Based Strategy (Version 2)

- **Approach**: Treats each array position as distinct, even for duplicate values
- **Pairs**: All combinations of different indices: `(i, j)` where `i < j`
- **Grouping**: Groups pairs by their sum value
- **Output**: Only sums with 2+ pairs are displayed
- **Ordering**: Results sorted by sum value for consistency

### Complexity

- **Time**: O(n²) for generating all pairs + O(k log k) for sorting groups
- **Space**: O(n²) for storing all pairs in the worst case

## Extensibility

The architecture supports easy extension:

1. **New Input Sources**: Implement `IInputReader` protocol
2. **New Output Formats**: Implement `IOutputWriter` protocol  
3. **New Algorithms**: Implement `IPairFindingStrategy` protocol
4. **New Features**: Add vertical slices under `features/`

## Requirements

- Python 3.13+
- uv (package manager)
- pytest (for testing, installed via uv)

---

## Original Problem Statement

Given an unsorted array `A[]`, print all unique pairs in the array that have the same sum.

### Requirements

- Output each group of pairs that share the same sum.
- Format the output as shown in the examples below.

---

## Examples

### Example 1

**Input:**

```A[] = {6, 4, 12, 10, 22, 54, 32, 42, 21, 11}```

**Output:**

- Pairs : (4, 12) (6, 10) have sum : 16
- Pairs : (10, 22) (21, 11) have sum : 32
- Pairs : (12, 21) (22, 11) have sum : 33
- Pairs : (22, 21) (32, 11) have sum : 43
- Pairs : (32, 21) (42, 11) have sum : 53
- Pairs : (12, 42) (22, 32) have sum : 54
- Pairs : (10, 54) (22, 42) have sum : 64

---

### Example 2

**Input:**

```A[] = {4, 23, 65, 67, 24, 12, 86}```

**Output:**

- Pairs : (4, 86) (23, 67) have sum : 90
