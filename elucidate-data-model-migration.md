# Data Model Migration Plan — SIOC Alignment

## Summary of Decisions

| Decision | Choice |
|----------|--------|
| Approach | Schema-outward full rewrite, one coordinated PR |
| Sequencing | Schema+Config → Extract → Transform → Serialize → Query |
| GraphDocument | Flat collections (idiomatic LinkML) |
| Person class | Yes, 1:1 with User for now |
| content:encoded | Deferred — investigate Telethon HTML export later |
| Reactions | Aggregate only (emoji+count); Reaction class in schema but not populated |
| Roles | Deferred entirely — no Role class for v1 |
| Polls | Full Poll class with structured data |
| Attachments | Full foaf:Document (Attachment class in LinkML) with all metadata |
| Links | Full foaf:Document (LinkedDocument class in LinkML) with WebPage preview enrichment |
| Document typing | Two LinkML classes (Attachment, LinkedDocument) both mapping to `foaf:Document` — distinguished by SIOC property (`sioc:attachment` vs `sioc:links_to`) |
| Forums | Full hierarchy extraction (supergroup + topic channels), no roles/admins |
| Extract output | Keep raw JSON, add forums.json for forum structure |

### Key Findings

1. **Raw message JSON already contains** polls, media metadata (mime type, size, duration), WebPage previews (title, description, author, site_name), reactions (aggregate + recent per-user), and forward source references. Extract expansion is mainly about forum structure.

2. **`foaf:Document` is the idiomatic SIOC choice** for both attachments and links. The SIOC spec deliberately leaves `sioc:attachment` and `sioc:links_to` ranges open. The property distinguishes the relationship type, not the object's class.

3. **`sioc:id` (not `dcterms:identifier`)** is the correct SIOC identifier property — "identifier unique per type per site."

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Two LinkML classes mapping to same `foaf:Document` class_uri | High | Test early with `just validate` + `just gen-model`. LinkML should handle this (different class names, same RDF type). |
| Serialize breaks with deeper entity structure | Medium | LinkML rdflib_dumper should handle it; test after schema is done. |
| Forum hierarchy extraction (Telethon API limitations) | Medium | Extend existing GetForumTopicsRequest. May need additional calls. |
| `sioc:id` + `identifier: true` in LinkML | Medium | Test that LinkML still treats this as the identifier slot. |
| sioc_types typing (ChatChannel, InstantMessage) | Medium | Research LinkML `class_uri` vs type mixins before implementing. |
| Poll data not in current test data | Low | Write the code; test when poll data exists. |
| Large coordinated change | Medium | Granular git commits per phase. Test at each boundary. |

## Open Questions (resolve during implementation)

1. **sioc_types typing**: How to express Forum-as-ChatChannel and Post-as-InstantMessage in LinkML? Options: separate subclasses, `class_uri` pointing to sioc_types, or a type discriminator slot.
2. **Bidirectional properties**: Use LinkML `inverse` for reply_of/has_reply and holds_account/account_of, or manage both in transform?
3. **Forum-as-container**: Express `container_of` as a reference (not inlined) in LinkML JSON. Posts live in GraphDocument's flat collection; Forum.container_of holds URI refs.
