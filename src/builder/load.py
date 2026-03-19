"""Load stage: POST RDF/Turtle to Oxigraph SPARQL server."""

import json
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen

from builder.config import TURTLE_FILE

OXIGRAPH_STORE_URL = "http://localhost:7878/store"


def main() -> None:
    if not TURTLE_FILE.exists():
        print(f"Turtle file not found: {TURTLE_FILE}")
        print("Run `just build` first (transform → serialize).")
        sys.exit(1)

    data = TURTLE_FILE.read_bytes()

    # PUT to default graph (replaces all existing data)
    default_graph_url = OXIGRAPH_STORE_URL + "?default"
    req_load = Request(default_graph_url, method="PUT", data=data)
    req_load.add_header("Content-Type", "text/turtle")

    try:
        urlopen(req_load)
    except URLError as e:
        print(f"Failed to connect to Oxigraph at {OXIGRAPH_STORE_URL}")
        print(f"Is the server running? Start it with: just up")
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Loaded {len(data):,} bytes of Turtle into Oxigraph")

    # Verify with a count query
    count_query = "SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }"
    req_q = Request(
        "http://localhost:7878/query",
        method="POST",
        data=count_query.encode(),
    )
    req_q.add_header("Content-Type", "application/sparql-query")
    req_q.add_header("Accept", "application/sparql-results+json")

    with urlopen(req_q) as resp:
        result = json.loads(resp.read())
        count = result["results"]["bindings"][0]["count"]["value"]
        print(f"Triple count: {count}")


if __name__ == "__main__":
    main()
