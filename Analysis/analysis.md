# Requirements Analysis: Unique Pair Sums in an Unsorted Array

## Problem Context

The task requires finding all unique pairs in an unsorted array that share the same sum. Given that arrays can contain duplicate values and the order is not guaranteed, several interpretation challenges arise that affect the implementation approach.

## Problem Clarification

### 1. What does "unique" mean exactly?

- Does "unique" refer to:
  - Each pair of numbers being used only once (no repeated indices)?
  - Each value combination being used only once (e.g., (4, 12) and (12, 4) are the same)?
  - Or, does it mean each sum is only reported once, regardless of how many pairs produce it?

### 2. Should all pairs with the same sum be output, or only two?

- Is the requirement to:
  - Output all possible unique pairs for each sum?
  - Output only the first two pairs found for each sum?
  - Output only one pair per sum?

### 3. How to handle duplicate values?

- If the array contains duplicate numbers, should:
  - Each occurrence be treated as a distinct element (i.e., indices matter)?
  - Only unique values be considered (i.e., values matter, not positions)?
  - Pairs with the same values but different indices be allowed?

---

## Solution Approaches

### **Version 1: Unique Value Pairs, All Pairs Output**

- **Definition:** Each pair consists of two different values, regardless of their positions. All pairs with the same sum are output, but (a, b) and (b, a) are considered the same.
- **Duplicates:** Ignore duplicate values; each value is used only once per pair.
- **Use Case:** When duplicate values should be treated as one entity and output simplicity is prioritized.
- **Pros:**
  - Simple to implement and understand.
  - Output is concise and avoids redundancy.
  - Clear semantic meaning for business logic.
- **Cons:**
  - May miss valid pairs if the array contains duplicates that should be considered separately.
  - Not suitable if the position of elements matters.
  - Potentially incomplete for mathematical analysis.

---

### **Version 2: Unique Index Pairs, All Pairs Output**

- **Definition:** Each pair consists of two elements at different indices. All pairs with the same sum are output, even if the values are the same.
- **Duplicates:** Each occurrence is treated as distinct; (A[0], A[1]) and (A[2], A[3]) are different even if values are equal.
- **Use Case:** When array positions matter or when working with data where duplicates represent different entities.
- **Pros:**
  - Captures all possible combinations, including those involving duplicates.
  - Mathematically complete and exhaustive.
  - Useful if the position of elements is important.
  - Handles edge cases with duplicate values correctly.
- **Cons:**
  - Output can be large and contain many similar pairs.
  - May be harder to read and interpret.
  - Potentially overwhelming for large datasets.

---

### **Version 3: Limited Pairs per Sum**

- **Definition:** For each sum, output only the first two unique pairs found (by value or index).
- **Duplicates:** Depends on implementation; could use either value or index uniqueness.
- **Use Case:** When output size needs to be controlled or when only examples are needed.
- **Pros:**
  - Output is limited and easy to read.
  - Satisfies requirements if only a sample is needed.
  - Good for demonstration purposes.
- **Cons:**
  - May omit valid pairs.
  - Ambiguous if more than two pairs exist for a sum.
  - Not deterministic without ordering rules.

---

## Analysis of Task Examples

Looking at the provided examples:

- Example 1 shows multiple pairs per sum (e.g., sum 16 has pairs (4,12) and (6,10))
- No duplicate values appear in the test arrays
- Pairs are shown in a consistent format without reversal (e.g., only (4,12), not (12,4))
- All possible pairs for each sum are displayed

This suggests the task expects **all pairs** to be found and displayed, supporting either Version 1 or Version 2 approaches.

## Conclusion

Given the unsorted nature of the array and the possibility of duplicate values in real-world scenarios, **Version 2 (Unique Index Pairs)** is the most robust choice. This approach ensures mathematical completeness by considering every possible pair combination, including cases where duplicate values exist at different positions. While this may result in larger output, it guarantees no valid pairs are missed and provides a foundation that can be filtered or processed further if needed. The comprehensive nature of this approach aligns with the task's requirement for "all unique pairs" and handles edge cases
