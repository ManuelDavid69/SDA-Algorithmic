# TP 8 — NetworkX and Dijkstra

## Objectives

- discover NetworkX on the Petersen graph (vertices, edges, degrees,
  matrices, induced subgraph, drawing);
- load a weighted graph from a multiline adjacency list;
- implement **Dijkstra's algorithm** by hand, with three variants of the
  visited set;
- compare the running times and explain the differences;
- apply the result to a real street network with OSMnx (optional).

The code lives in `src/sda/tp08_networkx`:

| Module | Contents |
|---|---|
| `fixture.py` | reproducible 20-vertex / 30-edge weighted graph and its file |
| `dijkstra.py` | `dijkstra1` (list), `dijkstra2` (set), `dijkstra_heap` |
| `routing.py` | OSMnx loading, geocoding helpers, route drawing |

Notebooks:

- [`notebooks/tp08_networkx_dijkstra.ipynb`](../notebooks/tp08_networkx_dijkstra.ipynb)
  — NetworkX discovery, graph drawing, all three Dijkstra versions and timing
  (executed, outputs included);
- [`notebooks/tp08_osmnx_routing.ipynb`](../notebooks/tp08_osmnx_routing.ipynb)
  — the Lyon route calculator (not executed: it needs internet access and the
  optional OSMnx package).

---

## 1. First steps with NetworkX

NetworkX stores a graph as a dictionary of dictionaries:
`G[node]` maps each neighbour to its edge data.  Graphs can be created from an
edge list, an adjacency matrix, a generator, a file, or a copy.

Useful calls:

| Call | Result |
|---|---|
| `G.is_directed()` | orientation |
| `G.nodes`, `G.edges` | vertices and edges |
| `G.neighbors(v)`, `G.degree[v]` | neighbourhood and degree |
| `nx.is_regular(G)`, `nx.is_connected(G)` | global properties |
| `nx.to_numpy_array(G)` | adjacency matrix |
| `nx.incidence_matrix(G)` | incidence matrix |
| `G.subgraph(vertices)` | induced subgraph |
| `nx.shortest_path(G, s, t, weight=...)` | reference shortest path |

### Petersen graph checks

- `G.is_directed()` → `False`;
- 10 vertices, 15 edges;
- `neighbors(2)` → `[7, 5, 4]` (order depends on insertion), i.e.
  `{4, 5, 7}`; `degree(9)` → 3;
- `nx.is_regular(G)` → `True`, degree 3;
- connected, not bipartite;
- the adjacency matrix is 10 × 10 and the incidence matrix is 10 × 15, with
  two `1`s per column;
- the induced subgraph on `{6, 3, 7, 8, 1, 5}` has 6 vertices and 6 edges.

The notebook draws the graph with the usual two-pentagon layout and displays
the induced subgraph.

---

## 2. The weighted graph

`data/tp08_graph.txt` follows the multiline adjacency-list format of the
statement and contains 20 vertices, 30 edges, integer weights between 1 and
50.  It is loaded with:

```python
graph = nx.read_multiline_adjlist(path, nodetype=int)
```

The fixture is deterministic (a fixed edge list), so the tests and the
notebook always produce the same shortest path:

```
0 -> 8 -> 6 -> 13 -> 19, length 112
```

---

## 3. Dijkstra by hand

The algorithm maintains:

- `distances[v]`: best known distance from the source;
- `previous[v]`: predecessor on the best path found so far;
- `visited`: vertices whose distance is final.

At each iteration:

1. select the unvisited vertex `u` with the smallest `distances[u]`;
2. mark it visited;
3. for every neighbour `v` of `u`, relax the edge:
   `distances[v] = min(distances[v], distances[u] + w(u, v))`.

When the target is selected, its distance is final; the path is reconstructed
by following `previous` backwards.

### `dijkstra1` — visited list

```python
visited = []
...
if node not in visited:      # O(V)
    ...
```

The membership test is linear.  It is performed for every candidate of the
minimum search and for every neighbour of every selected vertex, hence an
extra `O(V)` factor on sparse graphs.  On the 400-vertex test graph this
version is about **20 times slower** than the set version.

### `dijkstra2` — visited set

```python
visited = set()
...
if node not in visited:      # O(1)
```

The membership test becomes constant time.  The minimum search is still a
linear scan over the unvisited vertices, so the total complexity is
`O(V^2 + E)`: the algorithm is correct and much faster on sparse graphs, but
still quadratic.

### `dijkstra_heap` — binary heap

```python
queue = [(0.0, start)]
...
heapq.heappush(queue, (candidate, neighbour))
```

A heap returns the minimum in `O(log V)`.  Python's `heapq` has no
decrease-key, so an improved distance pushes a new pair and stale pairs are
ignored when popped.  The total cost is `O((V + E) log V)`, the best of the
three for large sparse graphs.

### Measured times

On the 20-vertex course fixture:

| Version | Time |
|---|---|
| `dijkstra1` (list) | ≈ 145 µs |
| `dijkstra2` (set) | ≈ 104 µs |
| `dijkstra_heap` | ≈ 72 µs |

On a 400-vertex / 900-edge random graph (same machine):

| Version | Time |
|---|---|
| `dijkstra1` (list) | ≈ 205 ms |
| `dijkstra2` (set) | ≈ 9.4 ms |
| `dijkstra_heap` | ≈ 1.6 ms |

The exact numbers depend on the machine; the orders of magnitude and the
ranking are stable.  All three versions return the same path and the same
length as `networkx.shortest_path`.

---

## 4. OSMnx route calculator

Install the optional dependencies:

```bash
pip install -e ".[routing]"
```

### Load the network

```python
import osmnx as ox
G = ox.graph_from_place("Lyon, France", network_type="drive")
```

The result is a `MultiDiGraph`: an edge is a dictionary of parallel arcs, each
with attributes such as `length`, `highway`, `name`, `speed_kph` and a
geometry.  For example:

```python
G.get_edge_data(u, v)
# {0: {"length": 42.3, "highway": "residential", ...}}
```

`edge_weight` in `dijkstra.py` handles this nested form by reading
`data[0]["length"]` when necessary.

### Display and inspect

- `ox.plot_graph(G, node_size=0, edge_color="yellow")` draws the network;
- `nodes, edges = ox.graph_to_gdfs(G)` converts it to GeoDataFrames, which can
  be explored interactively;
- `G.number_of_nodes()` and `G.number_of_edges()` give the size.

### Renumber the vertices

OSMnx identifiers are large and sparse.  Relabel them before using an
array-based algorithm:

```python
mapping = {node: index for index, node in enumerate(G.nodes)}
H = nx.relabel_nodes(G, mapping)
```

### Addresses and nearest nodes

The two addresses of the statement are:

- **start**: 6 Rue Plasson et Chaize;
- **destination**: 21 Rue Thénard.

Geocode them, then find the closest graph nodes:

```python
lat, lon = ox.geocode("6 Rue Plasson et Chaize, Lyon, France")
origin = ox.distance.nearest_nodes(H, X=lon, Y=lat)
```

`nearest_nodes` expects `X = longitude` and `Y = latitude`.

### Route and map

```python
distance, route = dijkstra_heap(H, origin, destination)
ox.plot_graph_route(H, route, route_color="red", node_size=0)
```

`routing.shortest_route` wraps this call; `routing.plot_route` draws the
result.  The route length is in metres, because OSMnx stores lengths in
metres.

The OSMnx notebook contains the complete code.  It is not executed in the
repository: the result depends on the OpenStreetMap data at download time and
requires an internet connection.

---

## 5. What the TP demonstrates

- the difference between a **correct** algorithm and an **efficient**
  implementation of it;
- why the choice of a data structure (list vs set vs heap) changes the
  complexity by orders of magnitude;
- how the same code runs on a synthetic graph and on a real street network;
- how NetworkX represents graphs, attributes and matrices.

---

## Run it

```bash
python -m sda.tp08_networkx.demo
python -m pytest tests/test_tp08_dijkstra.py
python -m nbconvert --to notebook --execute --inplace notebooks/tp08_networkx_dijkstra.ipynb
```
