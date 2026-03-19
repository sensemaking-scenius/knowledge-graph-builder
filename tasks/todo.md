# Safe Expansion, RDF Mapping Audit, Full History

## Phase 1: Expand to 30 Days Safely
- [x] Add `EXTRACT_DAYS` env var + `STATE_FILE` path to config.py
- [x] Add logging, rate-limiting, flood_sleep_threshold to extract.py
- [x] Add `--days` CLI argument
- [x] Parameterize justfile extract recipe

## Phase 2: RDF Mapping Audit & Expansion

### 2a: Schema Expansion
- [x] Add `rdfs:` prefix
- [x] Add `Thread` class (sioc:Thread)
- [x] Expand `Community` with name, description, member_count
- [x] Expand `UserAccount` with username, is_bot, is_verified, is_premium
- [x] Expand `Post` with 10 new slots (modified, num_views, num_replies, has_thread, reaction_count, reactions, media_type, forwarded_from, is_service, service_action)
- [x] Add `MediaType` and `ServiceActionType` enums
- [x] Add `threads` slot to GraphDocument

### 2b: Regenerate Models
- [x] `just gen-model` — all new classes, slots, enums generated

### 2c: Extract Enrichment
- [x] Expand `fetch_participants()` — bot, verified, premium flags
- [x] Add `fetch_channel_metadata()` — GetFullChannelRequest → channel.json

### 2d: Transform Expansion
- [x] `messages.py` — map edit_date, views, replies, reactions, media, fwd_from, service actions, threads
- [x] `users.py` — accept username, is_bot, is_verified, is_premium
- [x] `channel.py` — load channel.json for Community enrichment
- [x] `__init__.py` — thread registry, enriched participant metadata, message deduplication

### 2e: Dashboard
- [x] Most Reacted Posts section
- [x] Forum Threads section
- [x] Media Breakdown section
- [x] Recently Edited Posts section

## Phase 3: Full Historical Index
- [x] State file management (load_state/save_state)
- [x] `fetch_full()` with first-run and incremental modes
- [x] State saving every 500 messages for resume
- [x] `--full` and `--fresh` CLI flags
- [x] `extract-full` and `extract-fresh` justfile recipes
- [x] Message deduplication by ID in transform

## Verification
- [x] Schema validates via SchemaView
- [x] Models import and all new fields work
- [x] Transform: 94 posts, 15 users, 35 links, 14 threads
- [x] Serialize: 1261 triples in Turtle
- [x] Demo dashboard: all 11 sections render correctly
- [ ] `just load` — blocked by pyoxigraph 0.5.4 persistent store bug (pre-existing, unrelated)

---

# SIOC Data Model Migration

Full migration to the SIOC-compliant data model defined in `docs/data-model.md`.
Detailed decisions and rationale: `elucidate-data-model-migration.md`.

## Phase 4: Schema + Config

### 4.1 Rewrite `schemas/sioc.yaml`
- [x] Add new prefixes: `sioc_types`, `skos`, `dc`
- [x] Change `id` slot: `dcterms:identifier` → `sioc:id`
- [x] **Community**: remove `member_count`, add `has_part` (→ Site)
- [x] **Site** (NEW): `sioc:Site` — id, name, host_of (→ Forum, multivalued)
- [x] **Forum** (NEW): `sioc:Forum` — id, name, description, has_host (→ Site), has_parent (→ Forum), parent_of (→ Forum, multivalued), container_of (→ Post refs, multivalued), tg:closed (bool)
- [x] **Thread**: change `has_parent` range from Community → Forum
- [x] **User** (rename UserAccount): `sioc:User` — id, sioc:name, username, is_bot, account_of (→ Person), avatar, description
- [x] **Person** (NEW): `foaf:Person` — id, foaf:name, holds_account (→ User, multivalued)
- [x] **Post**: major slot overhaul
- [x] **Poll** (NEW): `sioc_types:Poll`
- [x] **Attachment** (NEW): `foaf:Document` — id, dcterms:format, dcterms:extent, tg:media_type, tg:duration
- [x] **LinkedDocument** (NEW): `foaf:Document` — id, dc:title, dcterms:description, dcterms:creator, tg:site_name
- [x] **Concept** (NEW): `skos:Concept` — id, skos:prefLabel
- [x] **Reaction** (NEW, schema-only for now): `tg:Reaction` — id, reactor (→ User), emoji, target (→ Post)
- [x] Remove old Link class, ServiceActionType enum
- [x] Update MediaType enum (for Attachment context)
- [x] Update GraphDocument: add site, forums, persons, concepts, attachments, linked_documents, polls; remove links

### 4.2 Regenerate `models.py`
- [x] Run `just gen-model`
- [x] Verify generated classes match schema

### 4.3 Update `config.py`
- [x] Add URI helpers: `site_uri()`, `forum_uri()`, `person_uri()`, `poll_uri()`, `concept_uri()`, `attachment_uri()`, `document_uri()`
- [x] Add `FORUMS_FILE` path constant
- [x] Update/verify existing URI helpers

### 4.4 Validate
- [x] `just validate` — schema is valid LinkML
- [x] `just gen-model` — models generate cleanly
- [x] Review: generated classes match data model doc

---

## Phase 5: Extract

### 5.1 Forum structure extraction
- [x] New function: `fetch_forums()` — topic ID, title, open/closed, creation date
- [x] Output: `data/raw/forums.json`
- [x] Wire into CLI pipeline

### 5.2 Verify existing message data
- [x] Confirm media metadata (mime_type, size) in raw JSON
- [x] Confirm webpage preview data (title, description, site_name, author) in raw JSON
- [x] Confirm reaction data (aggregate) in raw JSON
- [x] Confirm fwd_from has channel_id + channel_post for sibling refs
- [x] No polls found in current data (0 poll messages)
- [x] No quote_text found in current data
- [x] No via_bot_id found in current data
- [x] No grouped_id found in current data

### 5.3 Enhance participant extraction
- [ ] Check for avatar, bio/description in participant data (deferred — rate-limit sensitive)

### 5.4 Test
- [x] Verified forums.json generated from existing topics data
- [x] Spot-checked messages.jsonl for media/webpage/reaction/fwd_from data

---

## Phase 6: Transform (biggest phase)

### 6.1 Restructure `transform/__init__.py`
- [x] New dedup registries: forums, persons, concepts, attachments, linked_documents, polls
- [x] Load forum data from `forums.json`
- [x] Update GraphDocument construction with all new collections
- [x] Build has_reply index (second pass over posts)

### 6.2 Rewrite `transform/channel.py` → Community + Site + Forum hierarchy
- [x] Community (simplified — no member_count)
- [x] Site ("Telegram") with URI, name
- [x] Forum per supergroup (organizational, plain Forum)
- [x] Forum per topic channel (child of supergroup)
- [x] Wire: Community hasPart→Site, Site host_of→Forums, Forum parent_of→child Forums

### 6.3 Rewrite `transform/users.py` → User + Person
- [x] Rename UserAccount → User
- [x] Create Person per User (1:1)
- [x] Wire: Person holds_account→User, User account_of→Person
- [x] `sioc:name` for User display name, `foaf:name` for Person name

### 6.4 Rewrite `transform/messages.py` → Post + related entities
- [x] Update Post with new slot names and ranges
- [x] `has_container` → forum_uri (topic channel)
- [x] `reply_of` + `has_reply` — both directions
- [x] `sibling` — from fwd_from (channel_id + message_id → minted URI)
- [x] `attachment` — create Attachment entities for media
- [x] `links_to` — create LinkedDocument entities from webpage previews
- [x] `has_poll` — create Poll entities from MessageMediaPoll (no polls in current data)
- [x] `topics` → create Concept entities, register in concepts registry
- [x] `quote_text` — from reply_to (no quote_text in current data)
- [x] `grouped_id` — from message (no grouped_id in current data)
- [x] `via_bot` — from via_bot_id (no via_bot in current data)
- [x] Remove: mentions, entity_links, num_views, num_replies, reaction_count, reactions (strings), media_type (on Post), forwarded_from, is_service, service_action
- [x] Skip service messages (no longer mapped)

### 6.5 Update `transform/entities.py`
- [x] Topic extraction → return Concept objects (not URI strings)
- [x] URL extraction → return LinkedDocument objects with metadata
- [x] Remove mention extraction from Post pipeline
- [x] Remove entity_links handling

### 6.6 Thread handling
- [x] Thread.has_parent_forum → forum_uri instead of channel_uri

### 6.7 Test
- [x] `just transform` runs cleanly — 332 posts, 21 users, 29 forums, 27 attachments, 136 linked docs
- [x] Inspect linkml_graph.json — all new entity types present
- [x] Spot-check: Forum hierarchy, Person↔User links, Document metadata

---

## Phase 7: Serialize

### 7.1 Update `serialize.py`
- [x] No changes needed — `deep_clean_ids` is generic
- [x] Verify LinkML json_loader handles all new classes
- [x] Verify rdflib_dumper produces correct Turtle (5160 lines)

### 7.2 Inspect RDF output
- [x] Correct class URIs (sioc:User, sioc:Forum, foaf:Person, foaf:Document, skos:Concept)
- [x] Correct property URIs (sioc:id, sioc:attachment, sioc:links_to, sioc:host_of, etc.)
- [x] New prefix declarations: dc:, skos:, sioc_types: (via schema)
- [x] Relationship triples: site host_of forums, hasPart, holdsAccount, sibling, has_reply

---

## Phase 8: Load + Query

### 8.1 Load
- [ ] `just load` works (requires Docker Oxigraph — untested offline)
- [ ] Triple count is reasonable

### 8.2 Rewrite `query.py`
- [x] Update namespace prefixes (PREFIXES block with all 8 prefixes)
- [x] Rewrite community_overview (counts forums + linked docs)
- [x] Rewrite most_active_contributors (sioc:User, sioc:name)
- [x] Rewrite recent_conversations (has_container → Forum with name)
- [x] Rewrite reply_network (sioc:name instead of foaf:name)
- [x] Rewrite busiest_threads
- [x] Rewrite most_shared_links (sioc:links_to → foaf:Document with dc:title)
- [x] Remove most_mentioned (no longer in schema)
- [x] Remove most_reacted_posts (reactions not yet populated as entities)
- [x] Rewrite media_breakdown (media_type on Attachment)
- [x] Keep most_edited_posts (dcterms:modified)
- [x] New: Forum hierarchy overview (forum_hierarchy section)
- [x] New: Topic (skos:Concept) distribution (topic_distribution section)
- [x] New: Forwarded content / siblings (forwarded_content section)

### 8.3 End-to-end test
- [x] `just demo` — Rich dashboard, all 11 sections render correctly
- [ ] `just load` + `just query` — requires Docker Oxigraph

---

## Phase 9: Documentation + Cleanup

- [x] Update `CLAUDE.md` schema section (13 classes, new prefixes)
- [ ] Update `docs/data-model.md` if implementation deviations
- [ ] Update `README.md`
- [x] Clean up dead code / unused imports
- [x] Update memory file with new schema state
