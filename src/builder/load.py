"""Load stage: RDF/Turtle → Oxigraph triplestore."""

from typing import Any, Iterable, cast

from pyoxigraph import RdfFormat, Store

from builder.config import TURTLE_FILE, STORE_DIR


def main() -> None:
    STORE_DIR.mkdir(parents=True, exist_ok=True)

    store = Store(str(STORE_DIR))

    with open(TURTLE_FILE, "rb") as f:
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
