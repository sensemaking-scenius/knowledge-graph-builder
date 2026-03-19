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

# Phase 4: Data Enrichment

Reference: `docs/telethon-data-map.md` — full field inventory of Telethon data available for supergroups.

## 4.1 Forum Topics (first-class objects)
Currently: Thread class has only `id`, `name`, `has_parent`. Topics file just maps `{id: title}`.

- [ ] **Schema**: Expand `Thread` with `created`, `creator` (→ UserAccount), `icon_color` (int), `is_closed` (bool), `is_pinned` (bool), `is_hidden` (bool), `message_count` (int)
- [ ] **Extract**: Enrich `fetch_forum_topics()` — capture full ForumTopic fields: `date`, `from_id`, `icon_color`, `closed`, `pinned`, `hidden`, `top_message`, `unread_count`. Write as JSONL instead of flat `{id: title}` map
- [ ] **Transform**: Build Thread objects with all new fields from enriched topics file
- [ ] **Regenerate**: `just gen-model`
- [ ] **Verify**: Schema validates, new Thread fields appear in RDF output

## 4.2 Users (richer profiles)
Currently: `id`, `name`, `username`, `is_bot`, `is_verified`, `is_premium` from participants.

- [ ] **Schema**: Add `bio` (string, dcterms:description), `joined` (datetime), `is_deleted` (bool), `language` (string), `last_seen` (string — coarse status like "recently"/"last_week"/"online")
- [ ] **Extract**: Enrich `fetch_participants()` — capture `user.status` (map to coarse string), `user.lang_code`, `user.deleted`. Capture `.participant.date` as join date. Optionally batch `GetFullUserRequest` for bios (rate-limit sensitive — flag for opt-in)
- [ ] **Transform**: Map new participant fields to UserAccount slots
- [ ] **Regenerate**: `just gen-model`
- [ ] **Verify**: New user fields in RDF output

## 4.3 Media (type classification + polls)
Currently: `media_type` enum covers photo/video/document/webpage/audio/sticker/other.

- [ ] **Schema**: Add `MediaType` values: `poll`, `geo`, `geo_live`, `contact`, `voice`, `video_note`, `gif`, `game`, `dice`, `venue`. Add `poll_question` (string) slot on Post
- [ ] **Extract**: Already captured via `msg.to_dict()` — media object is in raw JSONL
- [ ] **Transform**: Expand `_classify_media()` in entities.py to detect all media types. Extract poll question text from `media.poll.question` when media type is poll
- [ ] **Regenerate**: `just gen-model`
- [ ] **Verify**: Media type distribution covers new types

## 4.4 Link Previews (WebPage metadata)
Currently: Link class has only `id` (the URL string). No title, description, or site name.

- [ ] **Schema**: Expand `Link` with `name` (string, site_name), `title` (string), `description` (string, dcterms:description), `link_type` (string — "article"/"video"/"photo"/etc.), `author` (string)
- [ ] **Extract**: Already in raw data — `msg.media.webpage` contains all fields
- [ ] **Transform**: In entities.py URL extraction, when a `MessageMediaWebPage` is present, populate Link fields from `webpage.site_name`, `webpage.title`, `webpage.description`, `webpage.type`, `webpage.author`
- [ ] **Regenerate**: `just gen-model`
- [ ] **Verify**: Link objects have rich metadata in RDF output

## 4.5 Albums (grouped media)
Currently: Not captured. Messages in the same album are treated as independent posts.

- [ ] **Schema**: Add `album_id` (string) slot on Post
- [ ] **Transform**: Map `msg['grouped_id']` to `album_id` when present. Messages sharing the same `grouped_id` are part of one media album
- [ ] **Regenerate**: `just gen-model`
- [ ] **Verify**: Album IDs appear on grouped posts

## 4.6 Engagement (views + structured reactions)
Currently: `num_views`, `reaction_count` (total int), `reactions` (list of strings like "👍 12"), `forwards` (int) are captured.

- [ ] **Schema**: Add `Reaction` class with `emoji` (string), `count` (int), `is_custom` (bool). Change Post.reactions from `multivalued string` to `multivalued Reaction` (inlined). Add `num_forwards` as alias/rename of `forwards` for consistency
- [ ] **Transform**: Build Reaction objects from `msg['reactions']['results']` — map `ReactionEmoji.emoticon` / `ReactionCustomEmoji.document_id`, extract count. Replace current string-based reactions
- [ ] **Regenerate**: `just gen-model`
- [ ] **Verify**: Reaction objects with emoji + count in RDF output

## 4.7 Rich Replies (quote text)
Currently: `reply_to` captures the target message ID. No quote text or thread metadata.

- [ ] **Schema**: Add `quote_text` (string) slot on Post
- [ ] **Transform**: Extract `msg['reply_to']['quote_text']` when present and map to Post.quote_text
- [ ] **Regenerate**: `just gen-model`
- [ ] **Verify**: Quote text appears on reply posts

## 4.8 Edits (edit timestamps)
Currently: `modified` slot exists in schema but check if transform actually populates it.

- [ ] **Audit**: Verify transform maps `msg['edit_date']` → Post.modified (may already work)
- [ ] **Fix if needed**: Ensure edit_date is correctly parsed and mapped
- [ ] **Verify**: Edited messages have `modified` timestamps in RDF output

## 4.9 Inline Bots (via_bot attribution)
Currently: Not captured.

- [ ] **Schema**: Add `via_bot` (string) slot on Post — the bot username/ID used to send the message
- [ ] **Transform**: Map `msg['via_bot_id']` to Post.via_bot. Resolve bot ID to username from participants if available
- [ ] **Regenerate**: `just gen-model`
- [ ] **Verify**: Bot-sent messages have via_bot attribution in RDF output
