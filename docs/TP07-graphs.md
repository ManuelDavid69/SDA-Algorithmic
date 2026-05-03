# TP 7 — Graphs: basic notions

## Objectives

- represent a graph with an adjacency list, and build its adjacency and
  incidence matrices;
- compute degrees, neighbourhoods, induced subgraphs and regularity;
- traversals (BFS/DFS), connected components and bipartiteness;
- Eulerian circuits and trails;
- greedy and exact colouring, independent sets, matchings and covers;
- apply these notions to the Petersen graph, a timetable, an envelope, the
  ambassador problem and the museum/castle plans.

The library is in `src/sda/tp07_graphs`:

| Module | Contents |
|---|---|
| `graph.py` | `Graph` and all the algorithms |
| `examples.py` | Petersen graph, envelope, language timetable |
| `analysis.py` | the answers of the TD, computed from the graphs |

The TD is mostly theoretical.  The graphs that are fully specified in the
statement (Petersen, the language timetable, the envelope) are encoded in
`examples.py`; the two picture-only exercises (museum and five rooms) are
solved by the generic algorithms once their plan is encoded as edges.

---

## Exercise 1 — The Petersen graph

### a) Oriented or not?

Undirected.  The edges are symmetric: if `6` is adjacent to `7`, then `7` is
adjacent to `6`; no arrow is drawn.

### b) Vertices and edges

Vertices: `1, 2, ..., 10`.  Edges (15):

```
6-7, 7-8, 8-9, 9-10, 10-6          (outer pentagon)
6-1, 7-2, 8-3, 9-4, 10-5          (spokes)
1-3, 3-5, 5-2, 2-4, 4-1           (inner pentagram)
```

### c) Neighbours of 2, degree of 10

`N(2) = {4, 5, 7}` (spoke `2-7`, star edges `2-4` and `2-5`).

`deg(10) = 3` (neighbours `6`, `9` and `5`).

### d) Regular?

Yes: every vertex has degree 3, so the graph is **3-regular** (cubic).

### e) Matrices

Adjacency matrix (rows/columns `1..10`):

```
0 0 1 1 0 1 0 0 0 0
0 0 0 1 1 0 1 0 0 0
1 0 0 0 1 0 0 1 0 0
1 1 0 0 0 0 0 0 1 0
0 1 1 0 0 0 0 0 0 1
1 0 0 0 0 0 1 0 0 1
0 1 0 0 0 1 0 1 0 0
0 0 1 0 0 0 1 0 1 0
0 0 0 1 0 0 0 1 0 1
0 0 0 0 1 1 0 0 1 0
```

The incidence matrix has 10 rows (vertices) and 15 columns (edges); each
column contains exactly two `1`s, at the endpoints of the edge.  Both
matrices are produced by `graph.adjacency_matrix()` and
`graph.incidence_matrix()` in `petersen_report()`.

### f) Induced subgraph on `{1, 3, 5, 6, 7, 8}`

The induced edges are:

```
1-3, 1-6, 3-5, 3-8, 6-7, 7-8
```

It has 6 vertices and 6 edges: a 5-cycle `1-3-8-7-6-1` with the pendant vertex
`5` attached to `3`.  Degrees: `deg(1)=2`, `deg(3)=3`, `deg(5)=1`,
`deg(6)=2`, `deg(7)=2`, `deg(8)=2`.

### g) Planar?

No.  The Petersen graph is the classical example of a non-planar graph: it
contains a subdivision of `K3,3` (Kuratowski's theorem).  It is also the
smallest bridgeless cubic non-planar graph.

### Bonus

| Quantity | Value |
|---|---|
| Chromatic number | 3 |
| Independence number | 4 |
| Maximum matching | 5 |
| Minimum vertex cover | 6 |

---

## Exercise 2 — Language timetable

Data:

| Student | Courses |
|---|---|
| Axel | anglais, espagnol |
| Béatrice | russe, grec |
| Corentin | anglais, italien |
| Dylan | russe, espagnol |
| Emilie | anglais, russe |

### a) Graph and nature

The natural representation is a **bipartite graph**: students on one side,
courses on the other, and an edge `(student, course)` when the student takes
the course.  No edge joins two students or two courses, so the graph is
bipartite by construction.

A second useful graph is the **student graph**: two students are adjacent
when they share at least one course.  It is not bipartite (for example
`Axel - Corentin - Emilie - Axel` is a triangle).

### b) Possible pairs

Two students form a pair when they share at least one course.  The seven
pairs are:

```
Axel-Corentin, Axel-Dylan, Axel-Emilie,
Béatrice-Dylan, Béatrice-Emilie,
Corentin-Emilie, Dylan-Emilie
```

### c) Largest group with no common course

At most **2**.  Example: `{Axel, Béatrice}` (Axel takes anglais/espagnol,
Béatrice russe/grec); `{Corentin, Dylan}` is another.  There is no independent
set of size 3 in the student graph.

### d) Message diffusion

Yes.  The bipartite student-course graph is connected.  For example:

```
grec -- Béatrice -- russe -- Dylan -- espagnol
                      |
                    Emilie -- anglais -- Corentin -- italien
```

The message can therefore travel from any course to any other course through
students.

### e) Timetable

Build the **course conflict graph**: two courses are adjacent when at least
one student takes both.  Its edges are:

```
anglais-espagnol, anglais-italien, anglais-russe,
russe-espagnol, russe-grec
```

It is 3-colourable, and 3 colours are necessary (the triangle
`anglais-espagnol-russe`).  So:

- at most **3 courses** can be placed in the same slot;
- **3 slots** are necessary and sufficient.

One valid assignment:

| Slot | Courses |
|---|---|
| 1 | anglais, grec |
| 2 | russe, italien |
| 3 | espagnol |

Check: anglais and grec share no student; russe and italien share none.

---

## Exercise 3 — The envelope

The five intersection points are the vertices `T` (top), `UL`, `UR`, `LL`,
`LR`.  The graph has 8 edges and the following degrees:

| Vertex | T | UL | UR | LL | LR |
|---|---|---|---|---|---|
| Degree | 2 | 4 | 4 | 3 | 3 |

### a) Ending at the starting point?

No.  An Eulerian **circuit** requires every vertex to have even degree; `LL`
and `LR` are odd.

### b) Without necessarily ending at the start?

Yes.  There are exactly two odd vertices, which is the necessary and
sufficient condition for an Eulerian **trail**.  One must start at one odd
vertex and finish at the other.  For example:

```
LL -> UL -> T -> UR -> UL -> LR -> UR -> LL -> LR
```

This uses each of the 8 edges exactly once; the reverse path is also valid.

---

## Exercise 4 — Isomorphic graphs

Both drawings have 10 vertices and are 3-regular, like the Petersen graph, so
the degree sequence alone cannot decide.  The right-hand drawing is the usual
Petersen embedding (outer pentagon, inner pentagram, five spokes).  To decide
for the left-hand drawing, encode its edge list and call:

```python
left = Graph.from_edges([...])
left.is_isomorphic(petersen_graph())
```

`Graph.is_isomorphic` checks the degree sequence, then searches for a
bijection that preserves adjacency (small graphs only).  A quicker
hand-written invariant is the **girth**: Petersen has girth 5; a drawing that
contains a triangle or a 4-cycle cannot be isomorphic to it.

---

## Exercise 5 — Reception at the embassy

The handshake lemma says that the sum of all degrees is twice the number of
edges, hence **even**.

### a) 48 ambassadors?

If the 48 people present each know exactly 11 others, the degree sum is
`48 * 11 = 528`, which is even: parity does not rule it out, and an
11-regular graph on 48 vertices exists, so the claim is possible.

If the host is a 49th participant (the wording "48 homologues" suggests this),
the sum is `49 * 11 = 539`, which is odd: impossible.  The rest of the
exercise (47 homologues) indicates that the intended total is 48 people; the
ambiguity is worth mentioning.

### b) One guest absent

With 48 people, the sum is even; with 47 people it is `47 * 11 = 517`, odd, so
the claim is **impossible**.  This is the parity argument the exercise is
after.

### c) Handshakes

With 48 ambassadors, each greets the other 47, and each handshake is counted
twice:

```
C(48, 2) = 48 * 47 / 2 = 1128
```

`ambassadors_report()` returns these checks; `ambassadors_possible(n, 11)`
implements the parity test.

---

## Exercise 6 — A night at the museum

Encode each room as a vertex and each corridor as an edge.

- A guard placed **in a corridor** covers the two rooms at its endpoints.
  The set of chosen corridors must touch every vertex: this is a **minimum
  edge cover**.  For a graph without isolated vertices,
  `|edge cover| = n - |maximum matching|`.
- A guard placed **in a room** covers all corridors incident to that room.
  The set of chosen rooms must touch every edge: this is a **minimum vertex
  cover**.  By complementarity with independent sets,
  `|vertex cover| = n - |maximum independent set|`.

Once the plan is encoded:

```python
museum = Graph.from_edges([...])
len(museum.min_edge_cover())   # guards in corridors
len(museum.min_vertex_cover()) # guards in rooms
```

The two numbers generally differ: an edge cover can be smaller because one
corridor covers two rooms at once, while a room-guard covers several
corridors.

---

## Exercise 7 — The five rooms

Model the five rooms **and the outside garden** as vertices, and each door as
an edge between the two places it connects.  The question "pass exactly once
through each door" is exactly an **Eulerian trail** problem:

- if every vertex has even degree, an Eulerian circuit exists (start anywhere);
- if exactly two vertices have odd degree, an Eulerian trail exists (start at
  one odd vertex and finish at the other);
- if there are more than two odd vertices, no such walk exists.

`Graph.eulerian_circuit()` and `Graph.eulerian_path()` implement the test and
the Hierholzer construction.  The printed plan only has to be encoded as an
edge list; the degree parity immediately gives the answer.

---

## Implementation notes

- `Graph` uses an adjacency dictionary `vertex -> {neighbour: weight}`;
  undirected edges are stored in both directions.
- `edges()` returns each undirected edge once, `adjacency_matrix()` is
  symmetric and `incidence_matrix()` puts two `1`s per undirected edge.
- BFS/DFS and connected components are `O(V + E)`.
- Eulerian trails use Hierholzer's algorithm in `O(V + E)` after the degree
  check.
- Colouring is exponential in the worst case (backtracking), but the graphs
  of the TD are tiny.  `greedy_coloring()` gives an upper bound quickly.
- Matchings and independent sets use branch-and-bound/backtracking, suitable
  for the 10-vertex graphs of the exercises.

---

## Run it

```bash
python -m sda.tp07_graphs.demo
python -m pytest tests/test_tp07_graphs.py
```
