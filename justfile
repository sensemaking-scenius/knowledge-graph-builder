# justfile
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

PY := "uv run python"

default: status

status:
  @echo "Repo: knowledge-graph-builder"
  @uv run python -V
  @echo "Store:"
  @ls -la data/store 2>/dev/null || true
  @echo "RDF:"
  @ls -la data/rdf 2>/dev/null || true
  @echo "Graph:"
  @ls -la data/graph 2>/dev/null || true
  @echo "Raw:"
  @ls -la data/raw 2>/dev/null || true

extract:
  {{PY}} -m builder.extract

transform:
  {{PY}} -m builder.transform

serialize:
  {{PY}} -m builder.serialize

load:
  {{PY}} -m builder.load

build: transform serialize load

run-all: extract build

serve:
  oxigraph serve --location data/store --bind localhost:7878

query:
  curl -s -X POST http://localhost:7878/query \
    -H "Content-Type: application/sparql-query" \
    --data 'SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }'

gen-model:
  uv run gen-python schemas/sioc.yaml > src/builder/models.py

validate:
  uv run linkml validate schemas/sioc.yaml

typecheck:
  uv run pyright

clean:
  @echo "Removing generated data files..."
  @rm -rf data/raw/*.jsonl data/raw/*.json
  @rm -rf data/graph/*.json
  @rm -rf data/rdf/*.ttl
  @rm -rf data/store/*
  @echo "Clean complete. Directories preserved."
