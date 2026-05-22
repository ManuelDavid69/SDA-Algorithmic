# Documentation

One document per practical session.  Each one follows the same structure:

1. objectives and link with the course;
2. implementation choices;
3. complexity analysis;
4. written answers to the theoretical questions;
5. how to run the code and the tests.

| Session | Topic | Document |
|---|---|---|
| 1 | Linked lists, train simulation, stacks, brackets | [TP01-data-structures.md](TP01-data-structures.md) |
| 2 | Complexity, growth classes, benchmarks | [TP02-complexity.md](TP02-complexity.md) |
| 3 | Recursion, divide and conquer, Hanoi, search | [TP03-recursion.md](TP03-recursion.md) |
| 4 | Selection, merge, two-thirds sort, candies | [TP04-sorting.md](TP04-sorting.md) |
| 5 | BST, expression trees, ternary trees, Akinator | [TP05-trees.md](TP05-trees.md) |
| 6 | Hash tables, AVL trees, vinyl catalogue | [TP06-associative-arrays.md](TP06-associative-arrays.md) |
| 7 | Graphs, Euler, colouring, covers | [TP07-graphs.md](TP07-graphs.md) |
| 8 | NetworkX, Dijkstra, OSMnx routing | [TP08-networkx-dijkstra.md](TP08-networkx-dijkstra.md) |

The notebooks are in [`../notebooks`](../notebooks):

- `tp08_networkx_dijkstra.ipynb` — executed, with outputs and figures;
- `tp08_osmnx_routing.ipynb` — code for the optional real-world routing part.

## Conventions

- Code comments, identifiers and tests are in English; the course statements
  and the written answers keep the original French terminology in mind
  (e.g. *tas*, *parcours*, *complexité*).
- Positions are 0-based in the code and are documented when the statement
  itself uses another convention.
- Every complexity claim in these documents is either proved or illustrated
  by a benchmark in the corresponding module.
