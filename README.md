# SDA Algorithmic

![Python CI](https://github.com/ManuelDavid69/SDA-Algorithmic/actions/workflows/python.yml/badge.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![Tests](https://img.shields.io/badge/tests-333%20passed-brightgreen)
![License MIT](https://img.shields.io/badge/license-MIT-yellow)

Practical work for the **Data Structures and Algorithms** course at
**CPE Lyon** (3IRC, 2025/2026), rewritten from scratch in Python.

The repository follows the eight course sessions: linked lists and stacks,
complexity analysis, recursion and divide and conquer, sorting, trees,
hash tables and AVL trees, graph theory, and finally NetworkX with Dijkstra's
shortest-path algorithm.

> The exercise statements are course material from CPE Lyon. This repository
> contains the implementations, tests, benchmarks and written answers.

---

## Contents

- [Overview](#overview)
- [Highlights](#highlights)
- [Quick start](#quick-start)
- [Repository structure](#repository-structure)
- [The eight sessions](#the-eight-sessions)
- [Tests](#tests)
- [Complexity summary](#complexity-summary)
- [Notebooks](#notebooks)
- [Documentation](#documentation)
- [Credits](#credits)
- [License](#license)

---

## Overview

| # | Session | Main deliverables | Documentation |
|---|---|---|---|
| 1 | **Data structures** | `Node`/`LinkedList` from scratch, train simulation, linked stack, bracket checker that reports line and column | [TP01](docs/TP01-data-structures.md) |
| 2 | **Complexity** | operation counting, 15-function growth ranking, prime benchmark, time/size tables, `Theta` proof | [TP02](docs/TP02-complexity.md) |
| 3 | **Recursion** | three Fibonacci variants, divide-and-conquer maximum, Hanoi, recursive/iterative binary search, Master Theorem | [TP03](docs/TP03-recursion.md) |
| 4 | **Sorting** | selection, merge, two-thirds sort, candy distribution (brute force vs sliding window) | [TP04](docs/TP04-sorting.md) |
| 5 | **Trees** | BST with deletion, ASCII printer, RPN expression trees, nested ternary parser, Akinator with JSON persistence | [TP05](docs/TP05-trees.md) |
| 6 | **Associative arrays** | hash table with `DELETED` tombstones, AVL tree with range queries, two-index vinyl catalogue | [TP06](docs/TP06-associative-arrays.md) |
| 7 | **Graphs** | graph library, Petersen graph, timetable, Eulerian trails, colouring, matchings and covers | [TP07](docs/TP07-graphs.md) |
| 8 | **NetworkX & Dijkstra** | reproducible weighted graph, three Dijkstra implementations, OSMnx routing notebook | [TP08](docs/TP08-networkx-dijkstra.md) |

---

## Highlights

- **333 tests** covering every session, including edge cases and invariants.
- Core algorithms written **without shortcuts**: no `list.sort()` in the
  sorting implementations, no NetworkX shortest-path call inside Dijkstra,
  no `collections.deque` in the linked structures.
- Three Dijkstra variants that make the impact of the visited data structure
  measurable: on a 400-vertex graph, the list version is about **20× slower**
  than the set version, and about **130× slower** than the heap version.
- Complexity answers are checked by code: operation-count formulas are
  compared with instrumented loops, the growth order is encoded as `Theta`
  classes, and the candy algorithm is compared with brute force on random
  instances.
- Executed **Jupyter notebook** for the NetworkX/Dijkstra session, and a
  ready-to-run OSMnx route calculator.

---

## Quick start

Requirements: **Python 3.11+**.

```bash
git clone https://github.com/ManuelDavid69/SDA-Algorithmic.git
cd SDA-Algorithmic

python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

python -m pip install -e ".[dev]"
python -m pytest
```

Run the demonstration of one session:

```bash
python -m sda.tp01_data_structures.demo
python -m sda.tp02_complexity.demo
python -m sda.tp03_recursion.demo
python -m sda.tp04_sorting.demo
python -m sda.tp05_trees.demo
python -m sda.tp06_associative_arrays.demo
python -m sda.tp07_graphs.demo
python -m sda.tp08_networkx.demo
```

Lint the code with Ruff:

```bash
python -m ruff check .
```

---

## Repository structure

```
src/sda/
|-- tp01_data_structures/    linked list, train, stack, bracket analysis
|-- tp02_complexity/         operation counts, growth classes, benchmarks
|-- tp03_recursion/          displays, Fibonacci, Hanoi, binary search
|-- tp04_sorting/            selection, merge, two-thirds, candies
|-- tp05_trees/              BST, printer, expression trees, ternary, Akinator
|-- tp06_associative_arrays/ hash table, AVL tree, vinyl catalogue
|-- tp07_graphs/             graph library, examples, TD answers
`-- tp08_networkx/           fixture, Dijkstra variants, OSMnx helpers

tests/                       333 pytest tests, one file per session
docs/                        one detailed document per session
notebooks/                   NetworkX/Dijkstra and OSMnx notebooks
data/                        weighted graph fixture for TP 8
.github/workflows/python.yml CI on Python 3.11, 3.12 and 3.13
```

---

## The eight sessions

### 1. Linked lists and stacks

- `Node` and `LinkedList` with insertion, deletion, search, access, size and
  a readable `repr`.
- Train simulation: each wagon holds four passengers; a full wagon sends the
  passenger to the next one, with the optional "walk back to the front"
  extension.
- Linked `Stack` and a bracket checker for `()`, `[]`, `{}` and `<>`, with the
  exact line and column of the first error.

### 2. Complexity

- Five instrumented programs with closed-form operation counts.
- The 15 functions of the statement ranked into 12 `Theta` classes.
- Prime testing benchmark, theoretical time table for `n = 10^6`, and the
  inverse table (largest instance in 1 second, 1 minute, ...).
- Proof that `3n^2 - 100n + 6 = Theta(n^2)` from the definition.

### 3. Recursion and divide and conquer

- Naive, memoised and tail-recursive Fibonacci, with measured timings.
- Divide-and-conquer maximum, Towers of Hanoi (moves replayed and checked for
  legality), recursive and iterative binary search.
- Full Master Theorem answers, including the cases where it does not apply.

### 4. Sorting

- Selection sort with its loop invariant, merge sort with three analyses
  (iteration, recursion tree, Master Theorem).
- Two-thirds sort from the 2024 exam, with a correctness proof and its
  `Theta(n^2.71)` complexity.
- Candy distribution: brute force and an `O(n log n)` sliding-window solution,
  cross-checked on random instances.

### 5. Trees

- BST with the three deletion cases, traversals, height and validity check.
- ASCII rendering of any binary tree.
- Expression trees from RPN, infix printing with parentheses, and direct RPN
  evaluation with a stack.
- Recursive-descent parser for nested ternary expressions.
- Akinator that asks questions, learns a new animal and saves its tree as
  JSON.

### 6. Hash tables and AVL trees

- Hash table with linear probing, probe counting and `DELETED` tombstones;
  the deletion counterexample is reproduced in the tests.
- AVL tree with LL/RR/LR/RL rotations, balance factors and `O(log n + k)`
  range queries.
- Vinyl Records Co. catalogue indexed both by reference (hash) and by year
  (AVL), with a comparison of the two structures.

### 7. Graphs

- Adjacency-list graph with matrices, subgraphs, BFS/DFS, components and
  bipartiteness.
- Eulerian circuits/trails (Hierholzer), greedy and exact colouring,
  independent sets, matchings, vertex and edge covers, isomorphism checks.
- Encoded Petersen graph, language timetable and envelope; TD answers computed
  by the library.

### 8. NetworkX and Dijkstra

- NetworkX discovery on the Petersen graph (degrees, matrices, subgraph,
  drawing).
- Dijkstra with a visited **list**, a **set** and a **binary heap**, all
  returning the same route; timing comparison on 20 and 400 vertices.
- OSMnx helpers for Lyon: load the street network, geocode the two addresses,
  find the nearest nodes, compute and draw the route.

---

## Tests

```bash
python -m pytest
```

| Test file | Tests | Coverage |
|---|---:|---|
| `test_tp01_linked_list.py` | 16 | list operations, bounds, equality |
| `test_tp01_train.py` | 12 | capacity, overflow, backtracking |
| `test_tp01_stack.py` | 25 | LIFO, valid/invalid brackets, error positions |
| `test_tp02_complexity.py` | 102 | closed forms, growth classes, benchmarks, tables |
| `test_tp03_recursion.py` | 40 | displays, Fibonacci, Hanoi legality, searches |
| `test_tp04_sorting.py` | 52 | random arrays, invariants, candy vs brute force |
| `test_tp05_trees.py` | 37 | BST deletion, rendering, RPN, ternary, Akinator |
| `test_tp06_associative.py` | 16 | collisions, tombstones, rotations, catalogue |
| `test_tp07_graphs.py` | 15 | matrices, traversals, Euler, colouring, covers |
| `test_tp08_dijkstra.py` | 18 | fixture, three variants, NetworkX comparison |
| **Total** | **333** | |

The suite runs in under a second and is executed by GitHub Actions on Python
3.11, 3.12 and 3.13.

---

## Complexity summary

| Algorithm / structure | Time | Notes |
|---|---|---|
| Linked list access / insert / delete | `O(k)` | `O(1)` at the head |
| Stack push / pop | `O(1)` | linked implementation |
| BST insert / search / delete | `O(h)` | `O(log n)` average, `O(n)` worst |
| AVL insert / search / delete | `O(log n)` | height kept in each node |
| AVL range query | `O(log n + k)` | `k` returned years |
| Hash table (linear probing) | `O(1)` average, `O(n)` worst | `alpha = 0.694` example |
| Selection sort | `Theta(n^2)` | best and worst case |
| Merge sort | `Theta(n log n)` | `T(n) = 2T(n/2) + Theta(n)` |
| Two-thirds sort | `Theta(n^2.71)` | `T(n) = 3T(2n/3) + Theta(1)` |
| Binary search | `O(log n)` | sorted input |
| Dijkstra with visited list | `O(VE)` worst | linear membership test |
| Dijkstra with visited set | `O(V^2 + E)` | linear minimum search |
| Dijkstra with heap | `O((V + E) log V)` | stale entries skipped |

---

## Notebooks

- [`notebooks/tp08_networkx_dijkstra.ipynb`](notebooks/tp08_networkx_dijkstra.ipynb)
  — **executed**, with outputs and figures: Petersen graph drawing, induced
  subgraph, weighted graph, the three Dijkstra versions and timings.
- [`notebooks/tp08_osmnx_routing.ipynb`](notebooks/tp08_osmnx_routing.ipynb)
  — the Lyon route calculator; not executed because it needs internet access
  and the optional `osmnx` package.

To open them:

```bash
python -m jupyter notebook notebooks/
```

To re-execute the main notebook:

```bash
python -m nbconvert --to notebook --execute --inplace notebooks/tp08_networkx_dijkstra.ipynb
```

---

## Documentation

Each session has a detailed write-up with the implementation choices, the
complexity analysis and the written answers:

| Session | Document |
|---|---|
| 1 | [Linked lists and stacks](docs/TP01-data-structures.md) |
| 2 | [Complexity](docs/TP02-complexity.md) |
| 3 | [Recursion and divide and conquer](docs/TP03-recursion.md) |
| 4 | [Sorting](docs/TP04-sorting.md) |
| 5 | [Trees](docs/TP05-trees.md) |
| 6 | [Hash tables and AVL trees](docs/TP06-associative-arrays.md) |
| 7 | [Graphs](docs/TP07-graphs.md) |
| 8 | [NetworkX and Dijkstra](docs/TP08-networkx-dijkstra.md) |

---

## Credits

- **Course and exercise statements**: CPE Lyon, *Structures de données et
  algorithmique*, 3IRC, 2025/2026.
- **Implementations, tests, benchmarks, notebooks and documentation**:
  [Manuel David](https://github.com/ManuelDavid69).

---

## License

MIT — see [LICENSE](LICENSE).
