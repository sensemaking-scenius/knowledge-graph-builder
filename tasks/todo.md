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
- [ ] Add new prefixes: `sioc_types`, `skos`, `dc`, `content`
- [ ] Change `id` slot: `dcterms:identifier` → `sioc:id`
- [ ] **Community**: remove `member_count`, add `has_part` (→ Site)
- [ ] **Site** (NEW): `sioc:Site` — id, name, host_of (→ Forum, multivalued)
- [ ] **Forum** (NEW): `sioc:Forum` — id, name, description, has_host (→ Site), has_parent (→ Forum), parent_of (→ Forum, multivalued), container_of (→ Post/Thread refs, multivalued), tg:closed (bool)
- [ ] **Thread**: change `has_parent` range from Community → Forum
- [ ] **User** (rename UserAccount): `sioc:User` — id, sioc:name, username, is_bot, account_of (→ Person), avatar, description
- [ ] **Person** (NEW): `foaf:Person` — id, foaf:name, holds_account (→ User, multivalued)
- [ ] **Post**: major slot overhaul
  - Remove: mentions, entity_links, num_views, num_replies, reaction_count, reactions (string list), media_type, forwarded_from, is_service, service_action
  - Change: has_container → Forum, topics → Concept, links_to → LinkedDocument
  - Add: has_reply (→ Post), sibling (→ Post), attachment (→ Attachment, multivalued), has_poll (→ Poll), via_bot (→ User), quote_text, grouped_id
  - Keep: id, content, created, modified, has_creator (→ User), reply_of (→ Post), forwards, pinned
- [ ] **Poll** (NEW): `sioc_types:Poll` — id, question, answers (structured), vote_count, quiz, closed, public_voters, multiple_choice, has_creator (→ User)
- [ ] **Attachment** (NEW): `foaf:Document` — id, dcterms:format, dcterms:extent, tg:media_type, tg:duration
- [ ] **LinkedDocument** (NEW): `foaf:Document` — id, dc:title, dcterms:description, dcterms:creator, tg:site_name
- [ ] **Concept** (NEW): `skos:Concept` — id, skos:prefLabel
- [ ] **Reaction** (NEW, schema-only for now): `tg:Reaction` — id, reactor (→ User), emoji, target (→ Post)
- [ ] Remove old Link class, ServiceActionType enum
- [ ] Update MediaType enum (for Attachment context)
- [ ] Update GraphDocument: add site, forums, persons, concepts, attachments, linked_documents, polls; remove links

### 4.2 Regenerate `models.py`
- [ ] Run `just gen-model`
- [ ] Verify generated classes match schema

### 4.3 Update `config.py`
- [ ] Add URI helpers: `site_uri()`, `forum_uri()`, `person_uri()`, `poll_uri()`, `concept_uri()`, `attachment_uri()`, `document_uri()`
- [ ] Add `FORUMS_FILE` path constant
- [ ] Update/verify existing URI helpers

### 4.4 Validate
- [ ] `just validate` — schema is valid LinkML
- [ ] `just gen-model` — models generate cleanly
- [ ] Review: generated classes match data model doc

---

## Phase 5: Extract

### 5.1 Forum structure extraction
- [ ] New function: `fetch_forums()` — supergroup metadata + all topic channels
  - Topic ID, title, open/closed status, creation date
  - Supergroup vs topic channel distinction
- [ ] Output: `data/raw/forums.json`
- [ ] Wire into CLI pipeline

### 5.2 Verify existing message data
- [ ] Confirm poll data in messages.jsonl (when polls exist)
- [ ] Confirm media metadata (mime_type, size, duration) in raw JSON
- [ ] Confirm webpage preview data (title, description, site_name, author) in raw JSON
- [ ] Confirm reaction data (aggregate) in raw JSON
- [ ] Confirm fwd_from has channel_id + channel_post for sibling refs
- [ ] Confirm reply_to has quote_text when present

### 5.3 Enhance participant extraction
- [ ] Check for avatar, bio/description in participant data
- [ ] Add UserFull fetch if needed (rate-limit sensitive)

### 5.4 Test
- [ ] Run `just extract` end-to-end
- [ ] Inspect forums.json output
- [ ] Spot-check messages.jsonl for poll/media/webpage data

---

## Phase 6: Transform (biggest phase)

### 6.1 Restructure `transform/__init__.py`
- [ ] New dedup registries: forums, persons, concepts, attachments, linked_documents, polls
- [ ] Load forum data from `forums.json`
- [ ] Update GraphDocument construction with all new collections

### 6.2 Rewrite `transform/channel.py` → Community + Site + Forum hierarchy
- [ ] Community (simplified — no member_count)
- [ ] Site ("Telegram") with URI, name
- [ ] Forum per supergroup (organizational, plain Forum)
- [ ] Forum per topic channel (ChatChannel type, child of supergroup)
- [ ] Wire: Community hasPart→Site, Site host_of→Forums, Forum parent_of→child Forums

### 6.3 Rewrite `transform/users.py` → User + Person
- [ ] Rename UserAccount → User
- [ ] Create Person per User (1:1)
- [ ] Wire: Person holds_account→User, User account_of→Person
- [ ] New properties: avatar, description (if available from participants)
- [ ] `sioc:name` for User display name, `foaf:name` for Person name

### 6.4 Rewrite `transform/messages.py` → Post + related entities
- [ ] Update Post with new slot names and ranges
- [ ] `has_container` → forum_uri (topic channel)
- [ ] `reply_of` + `has_reply` — both directions
- [ ] `sibling` — from fwd_from (channel_id + message_id → minted URI)
- [ ] `attachment` — create Attachment entities for media
  - Extract: mime_type, file_size, duration, media_type
  - URI: `tg:attachment/{message_id}/{index}`
- [ ] `links_to` — create LinkedDocument entities from webpage previews
  - Extract: url, title, description, author, site_name
  - URI: the URL itself
- [ ] `has_poll` — create Poll entities from MessageMediaPoll
  - Extract: question, answers, vote counts, quiz, closed
  - URI: `tg:poll/{message_id}`
- [ ] `topics` → create Concept entities, register in concepts registry
- [ ] `quote_text` — from reply_to
- [ ] `grouped_id` — from message
- [ ] `via_bot` — from via_bot_id, register bot User
- [ ] Remove: mentions, entity_links, num_views, num_replies, reaction_count, reactions (strings), media_type (on Post), forwarded_from, is_service, service_action

### 6.5 Update `transform/entities.py`
- [ ] Topic extraction → return Concept objects (not URI strings)
- [ ] URL extraction → return LinkedDocument objects with metadata
- [ ] Remove mention extraction from Post pipeline
- [ ] Remove entity_links handling

### 6.6 Thread handling
- [ ] Thread.has_parent → forum_uri instead of channel_uri

### 6.7 Test
- [ ] `just transform` runs cleanly
- [ ] Inspect linkml_graph.json — all new entity types present
- [ ] Spot-check: Forum hierarchy, Person↔User links, Document metadata

---

## Phase 7: Serialize

### 7.1 Update `serialize.py`
- [ ] Update `deep_clean_ids` for new entity structure if needed
- [ ] Verify LinkML json_loader handles all new classes
- [ ] Verify rdflib_dumper produces correct Turtle

### 7.2 Inspect RDF output
- [ ] Correct class URIs (sioc:User, sioc:Forum, foaf:Person, etc.)
- [ ] Correct property URIs (sioc:id, sioc:attachment, sioc:links_to, etc.)
- [ ] New prefix declarations in Turtle header
- [ ] Relationship triples (site host_of forum, forum container_of post, etc.)

---

## Phase 8: Load + Query

### 8.1 Load
- [ ] `just load` works (just POSTs Turtle, should be unchanged)
- [ ] Triple count is reasonable

### 8.2 Rewrite `query.py`
- [ ] Update namespace prefixes
- [ ] Rewrite community_overview (Community → Site → Forum structure)
- [ ] Rewrite most_active_contributors (sioc:User)
- [ ] Rewrite recent_conversations (has_container → Forum)
- [ ] Rewrite reply_network
- [ ] Rewrite busiest_threads (Thread.has_parent → Forum)
- [ ] Rewrite most_shared_links (sioc:links_to → foaf:Document)
- [ ] Remove/replace most_mentioned
- [ ] Rewrite most_reacted_posts
- [ ] Rewrite forum_threads (real Forum entities now)
- [ ] Rewrite media_breakdown (media_type on Attachment, not Post)
- [ ] Keep most_edited_posts (dcterms:modified still works)
- [ ] New: Forum hierarchy overview
- [ ] New: Topic (skos:Concept) distribution
- [ ] New: Attachment/media summary
- [ ] New: Poll results (if data exists)

### 8.3 End-to-end test
- [ ] `just run-all` — full pipeline
- [ ] `just demo` — Rich dashboard
- [ ] `just query` — SPARQL against Oxigraph

---

## Phase 9: Documentation + Cleanup

- [ ] Update `CLAUDE.md` schema section
- [ ] Update `docs/data-model.md` if implementation deviations
- [ ] Update `README.md`
- [ ] Clean up dead code / unused imports
- [ ] Update memory file with new schema state
