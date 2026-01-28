# justfile
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

PY := "uv run python"

default: status

status:
  @echo "Repo: knowledge-graph-builder"
  @echo "Python:"
  @uv run python -V
  @echo "Store:"
  @ls -la data/oxigraph/store 2>/dev/null || true
  @echo "RDF:"
  @ls -la data/rdf 2>/dev/null || true
  @echo "Raw:"
  @ls -la data/raw 2>/dev/null || true

extract:
  {{PY}} scripts/extract_last_7_days.py
  test -s data/raw/messages_last_7_days.jsonl
  head -n 1 data/raw/messages_last_7_days.jsonl | {{PY}} -c "import sys,json; json.loads(sys.stdin.read()); print('raw ok')"

canonicalize: extract
  {{PY}} scripts/canonicalize_last_7_days.py
  test -s data/raw/canonical_last_7_days.jsonl
  head -n 1 data/raw/canonical_last_7_days.jsonl | {{PY}} -c "import sys,json; d=json.loads(sys.stdin.read()); print('canonical ok', sorted(d.keys()))"

transform: canonicalize
  {{PY}} scripts/transform_to_linkml.py
  test -s data/raw/linkml_graph.json
  {{PY}} -c "import json; d=json.load(open('data/raw/linkml_graph.json')); print('linkml ok', 'posts', len(d.get('posts',{})) if isinstance(d.get('posts'),dict) else len(d.get('posts',[])))"

dump-rdf: transform
  {{PY}} scripts/dump_rdf.py
  test -s data/rdf/sioc_graph.ttl
  grep -q "sioc:Post" data/rdf/sioc_graph.ttl
  echo "rdf ok"

load-oxigraph: dump-rdf
  {{PY}} scripts/load_into_oxigraph.py

query-python:
  {{PY}} scripts/query_oxigraph.py

serve:
  oxigraph serve --location data/oxigraph/store --bind localhost:7878

query-http:
  curl -s -X POST http://localhost:7878/query \
    -H "Content-Type: application/sparql-query" \
    --data 'SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }' | {{PY}} -c "import sys,json; print(json.load(sys.stdin)['results']['bindings'][0]['count']['value'])"

run-all:
  just canonicalize
  just transform
  just dump-rdf
  just load-oxigraph
  @echo "OK: pipeline complete. Run 'just serve' in another terminal, then 'just query-http'."
