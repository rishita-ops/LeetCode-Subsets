# LeetCode — Subsets

A focused Python implementation of **LeetCode's Subsets (Medium)** that **generates every possible subset (the power set) of an array** using recursive backtracking. Clean, minimal, and correct — this solution is the entry point to understanding the **choose → explore → un-choose** template, the role of the `index` pointer in avoiding duplicates, and the important detail of **copying the path before storing it**. Backtracking over a "choose or skip" decision is one of the most reused patterns in combinations, permutations, and constraint-search problems.

🔗 **Problem link:** [leetcode.com/problems/subsets](https://leetcode.com/problems/subsets/)

---

## Problem Statement

Given an integer array `nums` of **unique** elements, return **all possible subsets** (the power set).

The solution set **must not contain duplicate subsets**. Return the solution in **any order**.

**Example 1:**

```
Input:  nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

**Example 2:**

```
Input:  nums = [0]
Output: [[],[0]]
```

**Official Constraints:**

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All the numbers of `nums` are **unique**

---

## The Code

```python
"""
Subsets :
Given an integer array nums of unique elements, return all possible subsets (the power set).
The solution set must not contain duplicate subsets. Return the solution in any order.
Example:
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
"""
class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        result = []

        def backtrack(index, current_path):
            # Append a copy of the current subset to the result
            result.append(list(current_path))

            for i in range(index, len(nums)):
                # Include the element
                current_path.append(nums[i])
                # Move to the next element
                backtrack(i + 1, current_path)
                # Exclude the element (backtrack)
                current_path.pop()

        backtrack(0, [])
        return result
```

---

## The Critical Idea — Every Node in the Recursion Is a Subset

This is the most important thing to understand about this solution.

The recursion builds a **tree**. The root is the empty subset. From any node, you may add **any element that comes later in the array** (that is what `range(index, len(nums))` allows). Every node you reach is a valid subset, so **every call records its current path** before exploring further.

```
nums = [1, 2, 3]

                       []
          ┌─────────────┼─────────────┐
         [1]           [2]           [3]
       ┌───┴───┐        │
    [1,2]    [1,3]    [2,3]
       │
   [1,2,3]
```

That tree has exactly **8 nodes = 2³ subsets**, grouped by size as 1 + 3 + 3 + 1.

Why each subset appears **exactly once**: elements are only ever added in **increasing index order**. The subset `{1, 3}` can be built only as `[1] → [1,3]`, never as `[3] → [3,1]`, because after choosing `3` the next index is `3`, past the end of the array.

| Technique                           | What it controls                                                           |
| ----------------------------------- | -------------------------------------------------------------------------- |
| `result.append(list(current_path))` | Records the subset at **every** node, including the empty one              |
| `range(index, len(nums))`           | Only elements **after** the last chosen one — no duplicates, no reordering |
| `backtrack(i + 1, ...)`             | Moves the start past the chosen element — it is never used twice           |
| `current_path.pop()`                | **Un-choose** — restores the path so the next sibling starts clean         |

---

## How the Recursion Works

```python
def backtrack(index, current_path):
    result.append(list(current_path))

    for i in range(index, len(nums)):
        current_path.append(nums[i])      # choose
        backtrack(i + 1, current_path)    # explore
        current_path.pop()                # un-choose
```

- **Record:** every call first saves a **copy** of `current_path` — each call is one subset
- **Loop:** tries each remaining element `nums[i]` for `i ≥ index` as the next addition
- **Choose:** `append(nums[i])` adds it to the path
- **Explore:** `backtrack(i + 1, ...)` recurses with the start index moved just past it
- **Un-choose:** `pop()` removes it, restoring the path before trying the next element
- **Base case:** there is no explicit one — when `index == len(nums)`, the loop is empty and the call returns on its own

> **The copy matters:** `list(current_path)` is **not** optional. `current_path` is one single list that is mutated throughout the recursion. Appending it directly would store **references to the same list** eight times, and by the end every entry would be empty `[]` because of the final pops. The `list(...)` call stores a snapshot.

---

## Algorithm (Pseudocode)

```
result = []

backtrack(index, path):
    add a copy of path to result
    for i from index to n-1:
        path.append(nums[i])
        backtrack(i + 1, path)
        path.pop()

backtrack(0, [])
return result
```

---

## Dry Run

**Input:** `nums = [1, 2, 3]`

| Step | Call                                   | `current_path` | Action                               |
| ---- | -------------------------------------- | -------------- | ------------------------------------ |
| 1    | `backtrack(0)`                         | `[]`           | record `[]`                          |
| 2    | choose `1` → `backtrack(1)`            | `[1]`          | record `[1]`                         |
| 3    | choose `2` → `backtrack(2)`            | `[1,2]`        | record `[1,2]`                       |
| 4    | choose `3` → `backtrack(3)`            | `[1,2,3]`      | record `[1,2,3]`, loop empty, return |
| 5    | pop `3`, loop at index 2 ends, pop `2` | `[1]`          | back in step 2's loop                |
| 6    | choose `3` → `backtrack(3)`            | `[1,3]`        | record `[1,3]`, return               |
| 7    | pop `3`, loop ends, pop `1`            | `[]`           | back at the root                     |
| 8    | choose `2` → `backtrack(2)`            | `[2]`          | record `[2]`                         |
| 9    | choose `3` → `backtrack(3)`            | `[2,3]`        | record `[2,3]`, return               |
| 10   | pop `3`, pop `2`                       | `[]`           | back at the root                     |
| 11   | choose `3` → `backtrack(3)`            | `[3]`          | record `[3]`, return                 |
| 12   | pop `3`, root loop ends                | `[]`           | done                                 |

**Output:** `[[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]` ✅

All 8 subsets are present. The order differs from the example, which is allowed because the problem accepts **any order**.

---

## Complexity Analysis

| Metric            | Complexity                                                                                                       |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| Time              | **O(n · 2ⁿ)** — there are `2ⁿ` subsets (one per recursive call), and copying each into `result` costs up to O(n) |
| Space (auxiliary) | **O(n)** — recursion depth is at most `n`, and `current_path` holds at most `n` elements                         |
| Space (output)    | **O(n · 2ⁿ)** — the returned subsets themselves                                                                  |

For the maximum input `n = 10`, that is only `2¹⁰ = 1024` subsets, so the solution runs instantly.

---

## Edge Cases

| Scenario                      | Behavior                                                                                     |
| ----------------------------- | -------------------------------------------------------------------------------------------- |
| Single element `[0]`          | Records `[]`, then `[0]` — returns `[[], [0]]` ✅                                            |
| Two elements `[1, 2]`         | Returns `[[], [1], [1,2], [2]]` — all 4 subsets ✅                                           |
| Negative numbers `[-1, 0, 5]` | Values are never compared, only collected — works unchanged ✅                               |
| Maximum size `n = 10`         | 1024 subsets generated quickly ✅                                                            |
| Empty array `[]`              | Records `[]`, loop is empty — returns `[[]]` ✅ (the problem guarantees `n >= 1`)            |
| Output order                  | Depth-first order, not sorted by size — acceptable because any order is allowed ✅           |
| Input array                   | Never modified ✅                                                                            |
| Duplicate values `[1, 2, 2]`  | Produces duplicate subsets such as `[1,2]` twice ⚠️ (the problem guarantees unique elements) |

---

## Code-Quality Notes

**This is a valid LeetCode submission.** The class name `Solution`, the method name `subsets`, and the parameter and return types match what LeetCode expects, so the code can be pasted into the editor directly (without the docstring if you prefer).

**Type hints need Python 3.9+.** `list[int]` and `list[list[int]]` use built-in generics. On older versions, use `from typing import List` and write `List[int]` and `List[List[int]]`.

**Nested function.** `backtrack` is defined inside `subsets` so it can read `nums` and write to `result` without passing them as parameters. This keeps the recursive signature small: only `index` and `current_path` change between calls.

**Running it locally.** The file only defines the class. To see output, add a small test at the bottom:

```python
print(Solution().subsets([1, 2, 3]))
```

---

## The Natural Extension — Subsets With Duplicates

When the input **may contain duplicates**, the same template produces repeated subsets. The fix is two small changes: **sort** the array, and **skip** an element if it equals the previous one _at the same level of the loop_.

```python
def subsets_with_dup(nums):
    nums.sort()
    result = []

    def backtrack(index, current_path):
        result.append(list(current_path))

        for i in range(index, len(nums)):
            if i > index and nums[i] == nums[i - 1]:
                continue                      # skip duplicate at this level
            current_path.append(nums[i])
            backtrack(i + 1, current_path)
            current_path.pop()

    backtrack(0, [])
    return result
```

**Result for `[1, 2, 2]`:** `[[], [1], [1,2], [1,2,2], [2], [2,2]]` ✅ — six distinct subsets, no repeats.

| Property    | This code (unique elements) | With-duplicates version              |
| ----------- | --------------------------- | ------------------------------------ |
| Sorts input | ❌ No                       | ✅ Yes                               |
| Skip rule   | None needed                 | `i > index and nums[i] == nums[i-1]` |
| Time        | O(n · 2ⁿ)                   | O(n · 2ⁿ) (plus O(n log n) to sort)  |
| Output      | All `2ⁿ` subsets            | Only distinct subsets                |

**An iterative alternative — bitmask.** Each number from `0` to `2ⁿ − 1` encodes one subset: bit `j` set means `nums[j]` is included.

```python
def subsets_bitmask(nums):
    n = len(nums)
    return [[nums[j] for j in range(n) if (mask >> j) & 1] for mask in range(1 << n)]
```

It has the same O(n · 2ⁿ) time, needs no recursion, and is a good way to see why the answer size is exactly `2ⁿ`.

---

## Repository Structure

```
LeetCode-Subsets/
│
├── subsets.py        # Main Python implementation
└── README.md         # Project documentation
```

---

## How to Compile and Run

**Prerequisites:** Python 3.9+

Add this line at the bottom of `subsets.py` to see the result:

```python
print(Solution().subsets([1, 2, 3]))
```

```bash
# Clone the repository
git clone https://github.com/rishita-ops/LeetCode-Subsets.git
cd LeetCode-Subsets

# Run
python3 subsets.py
```

**On Windows:**

```bash
python subsets.py
```

**Expected output:**

```
[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
```

---

## Key Concepts Covered

- **Power set** — a set of `n` elements has exactly `2ⁿ` subsets
- **Backtracking** — build a candidate step by step, undo the last step, try the next option
- **Choose → explore → un-choose** — the three-line template used throughout backtracking
- **Start index (`index`, `i + 1`)** — only move forward, so each subset is generated once
- **Copying the path** — `list(current_path)` stores a snapshot, not a reference
- **Implicit base case** — an empty loop ends the recursion with no explicit `if`
- **O(n · 2ⁿ) time** — the output size is the lower bound on the work
- **Duplicate handling** — sort plus a same-level skip rule for inputs with repeats

---

## Why This Problem Matters in DSA

The choose → explore → un-choose pattern appears across a broad family of problems:

| Problem / Concept                           | Connection                                                     |
| ------------------------------------------- | -------------------------------------------------------------- |
| **Subsets II** (LeetCode #90)               | Same template with sorting and the duplicate-skip rule         |
| **Combinations** (LeetCode #77)             | Same loop, but only record paths of exactly length `k`         |
| **Combination Sum** (LeetCode #39)          | Same loop, but an element may be reused (`backtrack(i, ...)`)  |
| **Permutations** (LeetCode #46)             | Choose from _all_ unused elements, not only later ones         |
| **Letter Case Permutation** (LeetCode #784) | A binary choice at each character — the "include or skip" idea |
| **Palindrome Partitioning** (LeetCode #131) | Backtracking over cut positions, validating each piece         |
| **Word Search** (LeetCode #79)              | Backtracking on a grid with a visited mark and un-mark         |
| **Generate Parentheses** (LeetCode #22)     | Backtracking with pruning rules instead of a fixed loop        |

Every problem that asks for "all combinations", "all arrangements", or "all valid configurations" traces back to the tree of choices introduced here.

---

## Contributing

Contributions are welcome. Consider adding:

- The **duplicate-aware** version as a separate, submittable file
- The **bitmask** version for side-by-side comparison
- An **iterative** version that builds subsets by extending earlier results
- A version that **prints the recursion tree** while it runs
- Type hints using `typing.List` for Python versions before 3.9
- Implementations in C++, Java, or JavaScript

```bash
git checkout -b feature/your-feature
git commit -m "Add: your feature description"
git push origin feature/your-feature
# Then open a Pull Request
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

_Part of a structured LeetCode practice series — fundamentals, done right._
