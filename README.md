# Shortest Path API

Dijkstra's shortest-path algorithm exposed through a small FastAPI service, with a standalone Mintlify documentation site.

## Run the API

```bash
uv sync
uv run uvicorn dijkstra_service.api:app --reload
```

The API is available at `http://localhost:8000`. Try it with:

```bash
curl -X POST http://localhost:8000/shortest-path \
  -H 'Content-Type: application/json' \
  -d '{"edges":[{"source":"A","target":"B","weight":4},{"source":"A","target":"C","weight":1},{"source":"C","target":"B","weight":2}],"start":"A","end":"B"}'
```

## Run the docs

Install the [Mintlify CLI](https://www.npmjs.com/package/mint) once, then run:

```bash
cd docs
mint dev
```

The docs site opens at `http://localhost:3000`.
