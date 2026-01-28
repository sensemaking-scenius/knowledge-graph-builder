import json
import os
from collections.abc import Mapping
from typing import Any, cast

from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.loaders import json_loader
from linkml_runtime.utils.schemaview import SchemaView

from builder.sioc_model import GraphDocument

INP = "data/raw/linkml_graph.json"
SCHEMA = "schemas/sioc_min.yaml"
OUT = "data/rdf/sioc_graph.ttl"


def ensure_str_keys(x: Any) -> Any:
    if isinstance(x, Mapping):
        return {str(k): ensure_str_keys(v) for k, v in x.items()}
    if isinstance(x, list):
        return [ensure_str_keys(v) for v in x]
    return x


def unwrap_id_value(v: Any) -> Any:
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
    raw = json.load(open(INP, "r", encoding="utf-8"))
    raw = ensure_str_keys(raw)
    raw = deep_clean_ids(raw)

    tmp = "data/raw/linkml_graph.normalized.json"
    os.makedirs("data/raw", exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False)

    sv = SchemaView(SCHEMA)

    doc = cast(GraphDocument, json_loader.load(tmp, target_class=GraphDocument))

    ttl = rdflib_dumper.dumps(doc, schemaview=sv)

    os.makedirs("data/rdf", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(ttl)

    print(f"Wrote RDF to {OUT}")


if __name__ == "__main__":
    main()
