# TP 4 — Sorting algorithms

## Objectives

- implement selection sort and prove its loop invariant;
- analyse merge sort with the iteration method, a recursion tree and the
  Master Theorem;
- implement the two-thirds sort from the 2024 exam and prove its correctness;
- solve the candy distribution problem, first by brute force and then with an
  efficient `O(n log n)` algorithm.

---

## 1. Selection sort

```python
for i in range(n):
    minimum = i
    for j in range(i + 1, n):
        if items[j] < items[minimum]:
            minimum = j
    swap(items[i], items[minimum])
```

### Loop invariant

Before iteration `i`:

- `items[:i]` is sorted;
- `items[:i]` contains the `i` smallest elements of the whole list.

Initially `i = 0` and the prefix is empty, so the invariant holds.  At
iteration `i`, the inner loop finds the smallest element of `items[i:]` and
swaps it to position `i`.  The prefix becomes `items[:i+1]`, still sorted, and
contains the `i+1` smallest elements.  At the end, `i = n` and the whole list
is sorted.

### Complexity

The inner loop performs `n - 1 - i` comparisons, so the total is

```
(n-1) + (n-2) + ... + 1 = n(n-1)/2 = Theta(n^2)
```

in the best case, the worst case and the average case.  The number of swaps
is at most `n - 1`, but it does not change the asymptotic cost.

---

## 2. Merge sort

### Recurrence

```
T(1) = Theta(1)
T(n) = 2 T(n/2) + Theta(n)   for n > 1
```

The `Theta(n)` term is the merge of the two sorted halves.

### Iteration method

```
T(n) = 2 T(n/2) + n
     = 4 T(n/4) + 2n
     = 8 T(n/8) + 3n
     ...
     = 2^k T(n/2^k) + kn
```

With `k = log2 n`, `T(n) = n T(1) + n log2 n = Theta(n log n)`.

### Recursion tree

Each level contains total work `n` (the merges partition the input), and the
tree has `log2 n + 1` levels, hence `Theta(n log n)`.

### Master Theorem

`a = 2`, `b = 2`, `log_b a = 1`, and `f(n) = Theta(n)`.  This is case 2, so
`T(n) = Theta(n log n)`.  All three methods agree.

---

## 3. Two-thirds sort (2024 exam)

```
sort(first two thirds)
sort(last two thirds)
sort(first two thirds)
```

Let `k = ceil(2n/3)`, `A = items[0:k]` (first two thirds) and
`B = items[n-k:n]` (last two thirds).  Their overlap is
`O = items[n-k:k]`; the prefix `A \ B` is the first `n-k` elements and the
suffix `B \ A` is the last `n-k` elements.

### Correctness

1. After the first sort, `A` is sorted; in particular every element of
   `A \ B` is at most every element of `O`.
2. During the second sort, `B` is sorted.  Since `O` is a prefix of `B`, the
   `|O|` smallest elements of `B` end up in `O`, so every element of `O` is at
   most every element of `B \ A`.
3. Therefore `A \ B <= O <= B \ A`, and both `A` and `B` are internally
   sorted.
4. The third sort sorts `A` again.  This restores order inside the overlap
   `O` while preserving the separation between `A \ B`, `O` and `B \ A`.
   The whole array is sorted.

The base case `n <= 2` sorts the two elements directly.  This base case is
necessary: for `n = 2`, the "first two thirds" is the whole array and the
recursion would not shrink.

### Recurrence and complexity

The three recursive calls have size `ceil(2n/3)` and the work outside the
calls is `Theta(1)`:

```
T(n) = 3 T(2n/3) + Theta(1)
```

With `a = 3`, `b = 3/2`, `log_b a = ln 3 / ln 1.5 ≈ 2.7095`.  Since
`f(n) = Theta(1) = O(n^(2.7095 - epsilon))`, case 1 of the Master Theorem
gives:

```
T(n) = Theta(n^(log_(3/2)(3))) = Theta(n^2.71)
```

This is **worse** than insertion sort (`Theta(n^2)`) and much worse than merge
sort (`Theta(n log n)`).  The algorithm is interesting as an exercise, not as
a practical sorting method.

---

## 4. Candy distribution

### Question 1 — brute force

Enumerate every subset of `m` packets among `n`, evaluate its spread
`max - min`, and keep the best one.  There are `C(n, m)` subsets and each
evaluation costs `O(m)`, so the complexity is `O(C(n, m) * m)`, which is
exponential in `n`.

### Question 2 — efficient algorithm

1. sort the packets: `O(n log n)`;
2. slide a window of exactly `m` consecutive packets over the sorted list and
   keep the window with the smallest `last - first`: `O(n)`.

Why is a consecutive window enough?  Take an optimal subset, let `a` be its
smallest element and `b` its largest.  In the sorted list, the window that
starts at `a` and contains `m` consecutive packets ends at an element `b' <=
b`, so its spread is at most `b - a`.  Replacing the optimal subset by this
window therefore cannot increase the difference.  Some optimal solution is
thus a consecutive window.

Total complexity: `O(n log n)` time, `O(n)` extra space for the sorted copy.

The test suite compares the efficient result with the brute-force result on
random small instances.

---

## Run it

```bash
python -m sda.tp04_sorting.demo
python -m pytest tests/test_tp04_sorting.py
```
