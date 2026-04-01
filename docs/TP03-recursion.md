# TP 3 — Recursion and divide and conquer

## Objectives

- write simple recursive functions (increasing/decreasing displays);
- compare three Fibonacci implementations (naive, memoised, tail recursive);
- apply divide and conquer to the maximum of a list;
- solve the Towers of Hanoi;
- implement binary search, then analyse it with the iteration method and the
  Master Theorem.

---

## 1. Recursive displays

`numbers_ascending(n)` follows the definition directly:

```python
if n == 0:
    return []
return numbers_ascending(n - 1) + [n]
```

`numbers_descending(n)` puts the current value before the recursive call. The
`print_*` variants call a configurable output function, which keeps them easy
to test. Both versions use `O(n)` calls and `O(n)` total space for the result
(or for the call stack when printing).

---

## 2. Fibonacci

With the convention of the statement, `F(0) = F(1) = 1`.

### `fibonacci1` — naive recursion

```python
if n <= 1:
    return 1
return fibonacci1(n - 1) + fibonacci1(n - 2)
```

The recurrence is `T(n) = T(n-1) + T(n-2) + 1`, so `T(n) = Theta(phi^n)` with
`phi = (1 + sqrt(5)) / 2 ≈ 1.618`. The call tree contains many identical
subproblems: computing `F(30)` already performs more than a million calls.

### `fibonacci2` — memoisation

A dictionary stores the values that have already been computed. Each index is
computed once, so the time complexity drops to `O(n)` and the space complexity
is `O(n)`.

### `fibonacci3` — terminal recursion

From `F(k) = a + b`, the next pair is `(b, a + b)`. The helper carries the two
accumulators and makes a single recursive call:

```python
def fib(k, a, b):
    if k == 0:
        return a
    return fib(k - 1, b, a + b)

return fib(n, 1, 1)
```

The arithmetic work is `O(n)` and only two integers are carried, so the
algorithm uses `O(1)` extra arithmetic state. Python does not perform tail-call
optimisation, so the call stack still grows to `O(n)` frames; in a language
with proper tail calls the stack would be constant.

### Measured behaviour

`python -m sda.tp03_recursion.demo` prints timings for `n = 5, 10, 15, 20, 25,
30`. The naive version grows roughly by a factor of `phi` at each step, while
the two others stay in the microsecond range.

---

## 3. Divide-and-conquer maximum

`max_list` splits the list in two halves, computes the maximum of each half
recursively, and returns the larger one:

```
T(n) = 2 T(n/2) + O(1)
```

The Master Theorem (case 1, `a = b = 2`) gives `T(n) = Theta(n)`. This is the
same asymptotic cost as a linear scan, with a larger constant and `O(log n)`
stack frames; the exercise is about the method, not about beating `max()`.

---

## 4. Towers of Hanoi

```python
solve(n - 1, source, auxiliary, target)
move(source, target)
solve(n - 1, auxiliary, target, source)
```

The recurrence is `T(n) = 2 T(n-1) + 1` with `T(0) = 0`, hence `T(n) = 2^n - 1`
moves. The test suite replays the moves on three stacks and checks that no
disk is ever placed on a smaller one.

---

## 5. Sequential and binary search

### Sequential search

- best case: the first element matches, `O(1)`;
- worst case: the element is absent (or last), `O(n)`;
- average case: `O(n)` (about `n/2` comparisons).

### Binary search

The list must be sorted. At each step the algorithm compares the middle
element with the target and discards one half:

```
T(n) = T(n/2) + O(1)
```

The iteration method gives `T(n) = O(log n)`. The Master Theorem applies with
`a = 1`, `b = 2`, `f(n) = O(1)`: `log_b(a) = 0`, so case 2 gives
`Theta(log n)`. Both the recursive and the iterative versions are
implemented; `dicho` is an alias of the recursive one, as in the statement.

---

## 6. Master Theorem

### 1. Applying the theorem

| Recurrence | Parameters | Case | Result |
|---|---|---|---|
| `T(n) = 8 T(n/2) + 1000 n^3` | `a=8, b=2, log_b a=3` | 2 | `Theta(n^3 log n)` |
| `T(n) = 2 T(n/2) + 10 n` | `a=2, b=2, log_b a=1` | 2 | `Theta(n log n)` |
| `T(n) = 2 T(n/2) + n^2` | `a=2, b=2, log_b a=1` | 3 | `Theta(n^2)` |
| `T(n) = 9 T(n/3) + n^2 log n` | `a=9, b=3, log_b a=2` | extended 2 | `Theta(n^2 log^2 n)` |

For the last one, `f(n) = n^2 log n` is larger than `n^2` but not
polynomially larger, so the standard case 3 does not apply; the extended case
2 gives the extra logarithm.

### 2. Why the theorem does not apply

| Recurrence | Reason |
|---|---|
| `T(n) = 2n T(n/2) + n` | the number of subproblems `a = 2n` depends on `n`; `a` must be a constant |
| `T(n) = (1/2) T(n/2) + n` | `a = 1/2 < 1`: the subproblem is smaller than the original one in a way that does not define a divide-and-conquer recurrence |
| `T(n) = 64 T(n/8) - n^2 log n` | the "toll" is negative; the theorem requires a positive `f(n)` |
| `T(n) = T(n/2) + n(2 - cos n)` | `f(n)` oscillates and does not satisfy the regularity condition `a f(n/b) <= c f(n)` |

### 3. Change of variable

For `T(n) = 2 T(sqrt(n)) + log2 n`, set `m = log2 n` and
`S(m) = T(2^m)`. Since `sqrt(n) = 2^(m/2)`:

```
S(m) = 2 S(m/2) + m
```

The Master Theorem gives `S(m) = Theta(m log m)` (case 2 with `a = b = 2`).
Going back to `n`:

```
T(n) = Theta(log n * log log n)
```

---

## Run it

```bash
python -m sda.tp03_recursion.demo
python -m pytest tests/test_tp03_recursion.py
```
