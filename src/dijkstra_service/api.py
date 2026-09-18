"""HTTP API for Dijkstra's shortest-path algorithm."""

from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .algorithm import shortest_path

app = FastAPI(
    title="Shortest Path API",
    version="1.0.0",
    description="Find a minimum-cost route through a non-negatively weighted graph.",
)


class Edge(BaseModel):
    source: Annotated[str, Field(min_length=1)]
    target: Annotated[str, Field(min_length=1)]
    weight: Annotated[float, Field(ge=0)]


class PathRequest(BaseModel):
    edges: Annotated[list[Edge], Field(max_length=20_000)]
    start: Annotated[str, Field(min_length=1)]
    end: Annotated[str, Field(min_length=1)]
    directed: bool = False


class PathResponse(BaseModel):
    reachable: bool
    distance: float | None
    path: list[str]


@app.get("/health", tags=["System"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/shortest-path", response_model=PathResponse, tags=["Paths"])
def find_shortest_path(request: PathRequest) -> PathResponse:
    graph: dict[str, list[tuple[str, float]]] = {
        request.start: [],
        request.end: [],
    }
    for edge in request.edges:
        graph.setdefault(edge.source, []).append((edge.target, edge.weight))
        graph.setdefault(edge.target, [])
        if not request.directed:
            graph[edge.target].append((edge.source, edge.weight))

    result = shortest_path(graph, request.start, request.end)
    if result is None:
        return PathResponse(reachable=False, distance=None, path=[])

    distance, path = result
    return PathResponse(reachable=True, distance=distance, path=path)
