"""Dijkstra's shortest-path algorithm."""

from collections.abc import Mapping, Sequence
from heapq import heappop, heappush
from math import inf

Graph = Mapping[str, Sequence[tuple[str, float]]]


def shortest_path(graph: Graph, start: str, end: str) -> tuple[float, list[str]] | None:
    """Return the minimum distance and path, or ``None`` when end is unreachable."""
    if start == end:
        return 0.0, [start]

    distances: dict[str, float] = {start: 0.0}
    previous: dict[str, str] = {}
    queue: list[tuple[float, str]] = [(0.0, start)]

    while queue:
        distance, node = heappop(queue)
        if distance > distances.get(node, inf):
            continue
        if node == end:
            break

        for neighbor, weight in graph.get(node, ()):
            if weight < 0:
                raise ValueError("Dijkstra's algorithm requires non-negative weights")

            candidate = distance + weight
            if candidate < distances.get(neighbor, inf):
                distances[neighbor] = candidate
                previous[neighbor] = node
                heappush(queue, (candidate, neighbor))

    if end not in distances:
        return None

    path = [end]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return distances[end], path
