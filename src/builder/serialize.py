"""Serialize stage: LinkML graph JSON → RDF/Turtle."""

import json

from collections.abc import Mapping
from typing import Any, cast

from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.loaders import json_loader
from linkml_runtime.utils.schemaview import SchemaView

from builder.config import GRAPH_FILE, SCHEMA_FILE, TURTLE_FILE
from builder.models import GraphDocument


def ensure_str_keys(x: Any) -> Any:
    """Recursively convert all dict keys to strings."""
    if isinstance(x, Mapping):
        return {str(k): ensure_str_keys(v) for k, v in x.items()}
    if isinstance(x, list):
        return [ensure_str_keys(v) for v in x]
    return x


def unwrap_id_value(v: Any) -> Any:
    """Unwrap nested {"id": ...} wrappers to plain string IDs."""
    if isinstance(v, str):
        return v
    if isinstance(v, Mapping) and "id" in v and len(v) == 1:
        inner = v["id"]
        if isinstance(inner, str):
            return inner
        if isinstance(inner, Mapping) and "id" in inner and len(inner) == 1 and isinstance(inner["id"], str):
            return inner["id"]
    return v


def deep_clean_ids(x: Any) -> Any:
    """Fix ID structure throughout a JSON tree for LinkML loader compatibility."""
    if isinstance(x, Mapping):
        out = {}
        for k, v in x.items():
            k = str(k)
            if k == "id":
                out[k] = unwrap_id_value(v)
            else:
                out[k] = deep_clean_ids(v)
        return out
    if isinstance(x, list):
        return [deep_clean_ids(v) for v in x]
    return x


def main() -> None:
    raw = json.load(open(GRAPH_FILE, "r", encoding="utf-8"))
    raw = ensure_str_keys(raw)
    raw = deep_clean_ids(raw)

    # Write normalized JSON to a temp file for the LinkML loader
    normalized = GRAPH_FILE.parent / "linkml_graph.normalized.json"
    with open(normalized, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False)

    sv = SchemaView(str(SCHEMA_FILE))
    doc = cast(GraphDocument, json_loader.load(str(normalized), target_class=GraphDocument))
    ttl = rdflib_dumper.dumps(doc, schemaview=sv)

    TURTLE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TURTLE_FILE, "w", encoding="utf-8") as f:
        f.write(ttl)

    print(f"Wrote RDF to {TURTLE_FILE}")


if __name__ == "__main__":
    main()
