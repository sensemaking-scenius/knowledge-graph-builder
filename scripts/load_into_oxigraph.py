from pathlib import Path
from typing import Any, Iterable, cast

from pyoxigraph import RdfFormat, Store

RDF_FILE = "data/rdf/sioc_graph.ttl"
STORE_DIR = "data/oxigraph/store"


def main() -> None:
    Path(STORE_DIR).mkdir(parents=True, exist_ok=True)

    store = Store(STORE_DIR)

    with open(RDF_FILE, "rb") as f:
        store.load(f, format=RdfFormat.TURTLE)

    store.flush()
    print("Loaded RDF into Oxigraph store")

    q = """
    SELECT (COUNT(*) AS ?count)
    WHERE { ?s ?p ?o . }
    """

    result = store.query(q)
    rows = cast(Iterable[Any], result)

    for row in rows:
        print("Triple count:", row["count"].value)


if __name__ == "__main__":
    main()
