# Unique Pair Sums in an Unsorted Array

## Problem Statement

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
