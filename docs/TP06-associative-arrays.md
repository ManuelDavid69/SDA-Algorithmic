# TP 6 — Associative arrays: hash tables and AVL trees

## Context

Vinyl Records Co. wants to query its catalogue in two ways:

- **point queries**: the price of the record with reference
  `9782070360024`;
- **range queries**: all records published between 1965 and 1975.

Two indexes are built:

| Index | Structure | Query |
|---|---|---|
| reference | hash table, `m = 1009`, linear probing | exact key |
| year | AVL tree, each node holds a list of references | range |

The implementation lives in `src/sda/tp06_associative_arrays`:

| Module | Contents |
|---|---|
| `hash_table.py` | `HashTable` with linear probing and `DELETED` tombstones |
| `avl.py` | `AVLTree` with the four rotations and range queries |
| `catalogue.py` | `VinylRecord`, `Catalogue` (both indexes) |

---

## Exercise 1 — Hash tables

### Question 1 — Insertions

With `h(k) = k mod 1009` and linear probing:

| Reference `k` | `h(k)` | Collision? | Extra probes | Final slot |
|---|---|---|---|---|
| 9782010000000 | 335 | no | 0 | 335 |
| 9782210000000 | 391 | no | 0 | 391 |
| 9782210000137 | 528 | no | 0 | 528 |
| 9782010138233 | 335 | yes (335) | 1 | 336 |
| 9782210000274 | 665 | no | 0 | 665 |
| 9782010276466 | 335 | yes (335, 336) | 2 | 337 |

The statement mentions "the 4 keys" but its table contains six references;
all six are handled above and in the test suite.

### Question 2 — Load factor and probing cost

With 700 elements in a table of size 1009:

```
alpha = 700 / 1009 = 0.6938
E[probes] = 1/2 * (1 + 1 / (1 - alpha)^2)
          = 1/2 * (1 + 1 / 0.3062^2)
          = 1/2 * (1 + 10.664)
          = 5.83
```

An **unsuccessful** search costs about **5.8 probes** on average.  This is
high for an unsuccessful search: at a load factor of about 0.7, linear
probing creates long clusters, and the cost grows quickly as `alpha`
approaches 1.  Practical implementations keep `alpha` below 0.5-0.7, resize
the table, or use a better collision strategy (double hashing, chaining).
Successful searches are cheaper (about
`1/2 * (1 + 1/(1 - alpha)) ≈ 2.13` probes with the usual approximation).

### Question 3 — Deletion with `None`

Counterexample with a table of size 7 and the keys `1, 8, 15` (all hash to
slot 1):

```
insert 1  -> slot 1
insert 8  -> slot 2   (collision, one probe)
insert 15 -> slot 3   (collision, two probes)
```

If `8` is deleted by writing `None` in slot 2:

```
slot 1: 1
slot 2: None
slot 3: 15
```

Searching `15` starts at slot 1, sees a key different from 15, then sees
`None` and concludes that 15 is absent.  This is wrong: the `None` broke the
probe chain.

The standard solution is a **tombstone** `DELETED`:

- a search treats `DELETED` as "occupied but not matching" and keeps probing;
- an insertion may reuse a `DELETED` slot, but only after checking that the
  key is not already stored later in the chain;
- the table is full only when every slot is a real key (a tombstone can
  always be reused).

`HashTable` implements exactly this strategy; `test_hash_deletion_leaves_a_tombstone`
checks that `15` remains reachable and that `22` reuses the tombstone.

### Question 4 — Range queries with the hash table

A hash table destroys the order of the keys: all records published between
1965 and 1975 can hash anywhere.  The only correct strategy is to **scan all
`m` slots** and test the year of every occupied slot:

```
O(m) = O(n)   (with m proportional to n)
```

A naive scan of the catalogue is also `O(n)`, so the hash table brings no
asymptotic improvement for this query (and adds hashing overhead).  The AVL
tree, on the other hand, keeps the years sorted and answers a range query in
`O(log n + k)`, where `k` is the number of matching records.

---

## Exercise 2 — AVL trees

### Question 1 — Insertion sequence

Insert `66, 72, 69, 58, 80, 75`:

1. `66` becomes the root.
2. `72` goes to the right of `66`.
3. `69` goes to the left of `72`.  Node `66` has a balance factor of `-2`
   and its right child `72` is left-heavy: this is an **RL** case.  A right
   rotation on `72`, then a left rotation on `66`, makes `69` the root:

   ```
        69
       /  \
     66    72
   ```

4. `58` goes to the left of `66`; no rotation.
5. `80` goes to the right of `72`; no rotation.

   ```
        69
       /  \
     66    72
     /       \
    58       80
   ```

6. `75` goes to the left of `80`.  Node `72` now has a balance factor of
   `-2`, and its right child `80` is left-heavy: another **RL** case.
   Right rotation on `80`, left rotation on `72`:

   ```
         69
        /  \
      66    75
      /    /  \
     58   72   80
   ```

The only rotations are the two **RL** double rotations (insertions of `69`
and `75`).

### Question 2 — Height and balance factors

The tree has **3 levels** (2 edges on the longest path, from `69` to `58` or
to `72`/`80`).

| Node | `h(left)` | `h(right)` | Balance | Balanced? |
|---|---|---|---|---|
| 69 | 2 | 2 | 0 | yes |
| 66 | 1 | 0 | +1 | yes |
| 58 | 0 | 0 | 0 | yes |
| 75 | 1 | 1 | 0 | yes |
| 72 | 0 | 0 | 0 | yes |
| 80 | 0 | 0 | 0 | yes |

Every balance factor is in `{-1, 0, +1}`, so the AVL condition holds.

### Question 3 — Range query

The AVL tree is ordered by year.  For an interval `[a, b]`, the recursive
query:

- goes left only if `node.key > a`;
- outputs the node if `a <= node.key <= b`;
- goes right only if `node.key < b`.

Subtrees entirely below `a` or above `b` are pruned.  The cost is
`O(log n + k)` for `n` nodes and `k` returned years (plus the cost of
collecting the references stored in each node).  A hash table cannot do
this, because it has no order to exploit.

### Question 4 — Comparison

| Operation | Hash table | AVL tree | Winner |
|---|---|---|---|
| Insertion | `O(1)` average, `O(n)` worst | `O(log n)` | hash table |
| Exact-key search | `O(1)` average, `O(n)` worst | `O(log n)` | hash table |
| Range search | `O(n)` | `O(log n + k)` | AVL tree |
| Memory | `O(m)` slots, `m ≈ n` | `O(n)` nodes + pointers | hash table (slightly) |
| Ordered traversal | `O(n log n)` (collect then sort) | `O(n)` in-order | AVL tree |

The hash table is the better **dictionary**; the AVL tree is the better
**ordered index**.  The catalogue uses both, one per query family.

### Exercise 3 — AVL vs red-black trees

Both guarantee `O(log n)` operations, but:

- an **AVL** tree is more strictly balanced (height at most about
  `1.44 log2 n`, versus `2 log2 n` for a red-black tree), so lookups are
  slightly faster;
- a **red-black** tree performs fewer rotations on insertion/deletion,
  because its balance condition is looser, so updates are cheaper;
- memory overhead is comparable (one colour bit versus a height field).

The catalogue is built once and then mostly read, which favours the AVL tree.
A red-black tree would be preferable for a write-heavy workload.

### Exercise 4 — Implementation

`HashTable` uses `EMPTY` and `DELETED` sentinels and counts the probes for
each insertion.  `AVLTree` stores `(year, list of references)` in each node,
performs the LL/RR/LR/RL rotations, and keeps the height in every node so
that the balance factor is `O(1)`.

---

## Run it

```bash
python -m sda.tp06_associative_arrays.demo
python -m pytest tests/test_tp06_associative.py
```
