"""A small graph library used by the graph practical work (TP 7)."""

from __future__ import annotations

from collections import deque
from typing import Hashable, Iterable, Iterator

Vertex = Hashable


class Graph:
    """Adjacency-list graph, undirected by default.

    Vertices can be any hashable value (integers, strings, ...).  Edges carry
    an optional weight, although most exercises only use the topology.
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self._adj: dict[Vertex, dict[Vertex, float]] = {}

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    @classmethod
    def from_edges(
        cls, edges: Iterable[tuple[Vertex, Vertex]], directed: bool = False
    ) -> Graph:
        graph = cls(directed=directed)
        for source, target in edges:
            graph.add_edge(source, target)
        return graph

    def add_vertex(self, vertex: Vertex) -> None:
        self._adj.setdefault(vertex, {})

    def add_vertices(self, vertices: Iterable[Vertex]) -> None:
        for vertex in vertices:
            self.add_vertex(vertex)

    def add_edge(self, source: Vertex, target: Vertex, weight: float = 1) -> None:
        self.add_vertex(source)
        self.add_vertex(target)
        self._adj[source][target] = weight
        if not self.directed:
            self._adj[target][source] = weight

    def remove_edge(self, source: Vertex, target: Vertex) -> None:
        del self._adj[source][target]
        if not self.directed:
            del self._adj[target][source]

    def remove_vertex(self, vertex: Vertex) -> None:
        del self._adj[vertex]
        for neighbours in self._adj.values():
            neighbours.pop(vertex, None)

    # ------------------------------------------------------------------
    # Basic queries
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._adj)

    def __iter__(self) -> Iterator[Vertex]:
        return iter(self._adj)

    def __contains__(self, vertex: Vertex) -> bool:
        return vertex in self._adj

    def __repr__(self) -> str:
        kind = "directed" if self.directed else "undirected"
        return f"Graph({kind}, vertices={self.order}, edges={self.size})"

    @property
    def vertices(self) -> list[Vertex]:
        return list(self._adj)

    @property
    def order(self) -> int:
        return len(self._adj)

    @property
    def size(self) -> int:
        if self.directed:
            return sum(len(neighbours) for neighbours in self._adj.values())
        return sum(len(neighbours) for neighbours in self._adj.values()) // 2

    def edges(self) -> list[tuple[Vertex, Vertex]]:
        result: list[tuple[Vertex, Vertex]] = []
        seen: set[frozenset[Vertex]] = set()
        for source, neighbours in self._adj.items():
            for target in neighbours:
                if self.directed:
                    result.append((source, target))
                else:
                    edge = frozenset((source, target))
                    if edge not in seen:
                        seen.add(edge)
                        result.append((source, target))
        return result

    def weighted_edges(self) -> list[tuple[Vertex, Vertex, float]]:
        return [
            (source, target, self._adj[source][target]) for source, target in self.edges()
        ]

    def neighbours(self, vertex: Vertex) -> list[Vertex]:
        if vertex not in self._adj:
            raise KeyError(vertex)
        return list(self._adj[vertex])

    # Alias with the American spelling used by most libraries.
    neighbors = neighbours

    def _undirected_neighbours(self, vertex: Vertex) -> set[Vertex]:
        result = set(self._adj[vertex])
        for source, neighbours in self._adj.items():
            if vertex in neighbours:
                result.add(source)
        return result

    def degree(self, vertex: Vertex) -> int:
        if vertex not in self._adj:
            raise KeyError(vertex)
        if not self.directed:
            return len(self._adj[vertex])
        return len(self._adj[vertex]) + self.in_degree(vertex)

    def in_degree(self, vertex: Vertex) -> int:
        return sum(1 for neighbours in self._adj.values() if vertex in neighbours)

    def out_degree(self, vertex: Vertex) -> int:
        return len(self._adj[vertex])

    def is_regular(self) -> bool:
        degrees = {self.degree(vertex) for vertex in self._adj}
        return len(degrees) <= 1

    def regularity(self) -> int | None:
        degrees = {self.degree(vertex) for vertex in self._adj}
        return next(iter(degrees)) if len(degrees) == 1 else None

    # ------------------------------------------------------------------
    # Matrices and subgraphs
    # ------------------------------------------------------------------
    def adjacency_matrix(self, vertices: list[Vertex] | None = None) -> list[list[int]]:
        vertices = vertices or self.vertices
        index = {vertex: position for position, vertex in enumerate(vertices)}
        matrix = [[0] * len(vertices) for _ in vertices]
        for source, target in self.edges():
            if source in index and target in index:
                matrix[index[source]][index[target]] = 1
                if not self.directed:
                    matrix[index[target]][index[source]] = 1
        return matrix

    def incidence_matrix(
        self,
        vertices: list[Vertex] | None = None,
        edges: list[tuple[Vertex, Vertex]] | None = None,
    ) -> list[list[int]]:
        vertices = vertices or self.vertices
        edges = edges or self.edges()
        index = {vertex: position for position, vertex in enumerate(vertices)}
        matrix = [[0] * len(edges) for _ in vertices]
        for column, (source, target) in enumerate(edges):
            if source in index and target in index:
                if self.directed:
                    matrix[index[source]][column] = -1
                    matrix[index[target]][column] = 1
                else:
                    matrix[index[source]][column] = 1
                    matrix[index[target]][column] = 1
        return matrix

    def subgraph(self, vertices: Iterable[Vertex]) -> Graph:
        selected = set(vertices)
        graph = Graph(directed=self.directed)
        for vertex in self._adj:
            if vertex in selected:
                graph.add_vertex(vertex)
        for source, target in self.edges():
            if source in selected and target in selected:
                graph.add_edge(source, target, self._adj[source][target])
        return graph

    def complement(self) -> Graph:
        if self.directed:
            raise ValueError("complement is only implemented for undirected graphs")
        graph = Graph()
        graph.add_vertices(self._adj)
        for position, source in enumerate(self.vertices):
            for target in self.vertices[position + 1 :]:
                if target not in self._adj[source]:
                    graph.add_edge(source, target)
        return graph

    # ------------------------------------------------------------------
    # Traversals and connectivity
    # ------------------------------------------------------------------
    def bfs(self, start: Vertex) -> list[Vertex]:
        if start not in self._adj:
            raise KeyError(start)
        visited = {start}
        order = [start]
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbour in self.neighbours(vertex):
                if neighbour not in visited:
                    visited.add(neighbour)
                    order.append(neighbour)
                    queue.append(neighbour)
        return order

    def dfs(self, start: Vertex) -> list[Vertex]:
        if start not in self._adj:
            raise KeyError(start)
        visited: set[Vertex] = set()
        order: list[Vertex] = []

        def visit(vertex: Vertex) -> None:
            visited.add(vertex)
            order.append(vertex)
            for neighbour in self.neighbours(vertex):
                if neighbour not in visited:
                    visit(neighbour)

        visit(start)
        return order

    def connected_components(self) -> list[set[Vertex]]:
        remaining = set(self._adj)
        components: list[set[Vertex]] = []
        while remaining:
            start = remaining.pop()
            component = {start}
            stack = [start]
            while stack:
                vertex = stack.pop()
                for neighbour in self._undirected_neighbours(vertex):
                    if neighbour in remaining:
                        remaining.remove(neighbour)
                        component.add(neighbour)
                        stack.append(neighbour)
            components.append(component)
        return components

    def is_connected(self) -> bool:
        if not self._adj:
            return True
        return len(self.connected_components()) == 1

    def distances(self, start: Vertex) -> dict[Vertex, int]:
        distances = {start: 0}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbour in self.neighbours(vertex):
                if neighbour not in distances:
                    distances[neighbour] = distances[vertex] + 1
                    queue.append(neighbour)
        return distances

    def is_bipartite(self) -> tuple[bool, dict[Vertex, int]]:
        colors: dict[Vertex, int] = {}
        for start in self._adj:
            if start in colors:
                continue
            colors[start] = 0
            queue = deque([start])
            while queue:
                vertex = queue.popleft()
                for neighbour in self._undirected_neighbours(vertex):
                    if neighbour not in colors:
                        colors[neighbour] = 1 - colors[vertex]
                        queue.append(neighbour)
                    elif colors[neighbour] == colors[vertex]:
                        return False, colors
        return True, colors

    def has_cycle(self) -> bool:
        if self.directed:
            visiting: set[Vertex] = set()
            visited: set[Vertex] = set()

            def visit(vertex: Vertex) -> bool:
                visiting.add(vertex)
                for neighbour in self.neighbours(vertex):
                    if neighbour in visiting:
                        return True
                    if neighbour not in visited and visit(neighbour):
                        return True
                visiting.remove(vertex)
                visited.add(vertex)
                return False

            return any(vertex not in visited and visit(vertex) for vertex in self._adj)

        visited: set[Vertex] = set()

        def visit(vertex: Vertex, parent: Vertex | None) -> bool:
            visited.add(vertex)
            for neighbour in self.neighbours(vertex):
                if neighbour == parent:
                    continue
                if neighbour in visited or visit(neighbour, vertex):
                    return True
            return False

        return any(vertex not in visited and visit(vertex, None) for vertex in self._adj)

    # ------------------------------------------------------------------
    # Eulerian trails
    # ------------------------------------------------------------------
    def _non_isolated(self) -> list[Vertex]:
        return [vertex for vertex in self._adj if self.degree(vertex) > 0]

    def eulerian_circuit(self, start: Vertex | None = None) -> list[Vertex] | None:
        non_isolated = self._non_isolated()
        if not non_isolated:
            return []
        if self.subgraph(non_isolated).is_connected() is False:
            return None
        if self.directed:
            if any(
                self.in_degree(vertex) != self.out_degree(vertex)
                for vertex in non_isolated
            ):
                return None
        elif any(self.degree(vertex) % 2 for vertex in non_isolated):
            return None
        start = start or non_isolated[0]
        trail = self._hierholzer(start)
        if len(trail) != self.size + 1:
            return None
        return trail

    def eulerian_path(self, start: Vertex | None = None) -> list[Vertex] | None:
        circuit = self.eulerian_circuit(start)
        if circuit is not None:
            return circuit
        non_isolated = self._non_isolated()
        if not non_isolated:
            return []
        if self.subgraph(non_isolated).is_connected() is False:
            return None

        if self.directed:
            starts = [
                vertex
                for vertex in non_isolated
                if self.out_degree(vertex) - self.in_degree(vertex) == 1
            ]
            ends = [
                vertex
                for vertex in non_isolated
                if self.in_degree(vertex) - self.out_degree(vertex) == 1
            ]
            balanced = [
                vertex
                for vertex in non_isolated
                if self.in_degree(vertex) == self.out_degree(vertex)
            ]
            if len(starts) != 1 or len(ends) != 1 or len(balanced) != len(non_isolated) - 2:
                return None
            start = start or starts[0]
        else:
            odd = [vertex for vertex in non_isolated if self.degree(vertex) % 2]
            if len(odd) != 2:
                return None
            start = start or odd[0]

        trail = self._hierholzer(start)
        if len(trail) != self.size + 1:
            return None
        return trail

    def _hierholzer(self, start: Vertex) -> list[Vertex]:
        adjacency = {
            vertex: dict(neighbours) for vertex, neighbours in self._adj.items()
        }
        stack = [start]
        circuit: list[Vertex] = []
        while stack:
            vertex = stack[-1]
            if adjacency.get(vertex):
                neighbour = next(iter(adjacency[vertex]))
                del adjacency[vertex][neighbour]
                if not self.directed:
                    del adjacency[neighbour][vertex]
                stack.append(neighbour)
            else:
                circuit.append(stack.pop())
        circuit.reverse()
        return circuit

    # ------------------------------------------------------------------
    # Colouring, independent sets, covers, matching
    # ------------------------------------------------------------------
    def greedy_coloring(self) -> dict[Vertex, int]:
        colors: dict[Vertex, int] = {}
        for vertex in sorted(self._adj, key=self.degree, reverse=True):
            used = {colors[neighbour] for neighbour in self.neighbours(vertex) if neighbour in colors}
            color = 0
            while color in used:
                color += 1
            colors[vertex] = color
        return colors

    def chromatic_number(self) -> int:
        if not self._adj:
            return 0
        vertices = sorted(self._adj, key=self.degree, reverse=True)
        colors: dict[Vertex, int] = {}

        def can_color(vertex: Vertex, color: int) -> bool:
            return all(
                colors.get(neighbour) != color for neighbour in self.neighbours(vertex)
            )

        def search(position: int, limit: int) -> bool:
            if position == len(vertices):
                return True
            vertex = vertices[position]
            for color in range(limit):
                if can_color(vertex, color):
                    colors[vertex] = color
                    if search(position + 1, limit):
                        return True
                    del colors[vertex]
            return False

        for limit in range(1, len(vertices) + 1):
            colors.clear()
            if search(0, limit):
                return limit
        return len(vertices)

    def max_independent_set(self) -> list[Vertex]:
        best: set[Vertex] = set()

        def expand(candidates: set[Vertex], current: set[Vertex]) -> None:
            nonlocal best
            if len(current) + len(candidates) <= len(best):
                return
            if not candidates:
                if len(current) > len(best):
                    best = set(current)
                return
            vertex = max(
                candidates, key=lambda item: len(set(self.neighbours(item)) & candidates)
            )
            expand(candidates - {vertex} - set(self.neighbours(vertex)), current | {vertex})
            expand(candidates - {vertex}, current)

        expand(set(self._adj), set())
        return sorted(best, key=repr)

    def max_matching(self) -> list[tuple[Vertex, Vertex]]:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def matching(remaining: frozenset[Vertex]) -> tuple[tuple[Vertex, Vertex], ...]:
            if not remaining:
                return ()
            vertex = min(remaining, key=repr)
            best = matching(remaining - {vertex})
            for neighbour in self.neighbours(vertex):
                if neighbour not in remaining:
                    continue
                candidate = ((vertex, neighbour),) + matching(
                    remaining - {vertex, neighbour}
                )
                if len(candidate) > len(best):
                    best = candidate
            return best

        return list(matching(frozenset(self._adj)))

    def min_vertex_cover(self) -> list[Vertex]:
        independent = set(self.max_independent_set())
        return [vertex for vertex in self._adj if vertex not in independent]

    def min_edge_cover(self) -> list[tuple[Vertex, Vertex]] | None:
        if any(not self._adj[vertex] for vertex in self._adj):
            return None
        matching = self.max_matching()
        covered = {vertex for edge in matching for vertex in edge}
        cover = list(matching)
        for vertex in self._adj:
            if vertex not in covered:
                neighbour = self.neighbours(vertex)[0]
                cover.append((vertex, neighbour))
                covered.update((vertex, neighbour))
        return cover

    # ------------------------------------------------------------------
    # Isomorphism (small graphs)
    # ------------------------------------------------------------------
    def is_isomorphic(self, other: Graph) -> bool:
        if self.directed != other.directed:
            return False
        if self.order != other.order or self.size != other.size:
            return False
        if sorted(self.degree(vertex) for vertex in self._adj) != sorted(
            other.degree(vertex) for vertex in other._adj
        ):
            return False

        left = sorted(self._adj, key=self.degree, reverse=True)
        right = sorted(other._adj, key=other.degree, reverse=True)
        mapping: dict[Vertex, Vertex] = {}
        used: set[Vertex] = set()

        def compatible(vertex: Vertex, candidate: Vertex) -> bool:
            if self.degree(vertex) != other.degree(candidate):
                return False
            for mapped, image in mapping.items():
                if (mapped in self._adj[vertex]) != (image in other._adj[candidate]):
                    return False
            return True

        def search(position: int) -> bool:
            if position == len(left):
                return True
            vertex = left[position]
            for candidate in right:
                if candidate in used or not compatible(vertex, candidate):
                    continue
                mapping[vertex] = candidate
                used.add(candidate)
                if search(position + 1):
                    return True
                used.remove(candidate)
                del mapping[vertex]
            return False

        return search(0)
