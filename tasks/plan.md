# SIOC Data Model Migration Plan

Single source of truth for the data model migration. Task checklist in `tasks/todo.md`.
Spec reference: `docs/sioc.md`. Telethon field inventory: `docs/telethon.md`.

---

## Approach

- **Schema-outward full rewrite**, one coordinated change
- **Sequencing**: Schema+Config → Extract → Transform → Serialize → Query
- Test at each phase boundary

---

## Class Inventory

### sioc:Community
- Single instance: "Sensemaking Scenius" — the people and purpose, not any single platform
- Connected to Sites via `dcterms:hasPart`
- No `member_count` (operational, not sensemaking)

### sioc:Site
- Telegram-the-platform. Hosts Forums, has Users.
- Connected to Community via `dcterms:isPartOf`
- `host_of` → Forums

### sioc:Forum (two variants)
- **Supergroup**: plain `sioc:Forum`, organizational container — cannot post directly to it
  - `has_host` → Site, `parent_of` → child Forums
- **Topic channels**: `sioc:Forum` typed as `sioc_types:ChatChannel` — where messages live
  - `has_parent` → supergroup Forum
- Side channels: independent Forums on the same Site, not children of supergroup

```
sioc:Site — "Telegram"
  |-- host_of --> sioc:Forum — Supergroup (organizational)
  |     |-- parent_of --> sioc:Forum (ChatChannel) — "General"
  |     |-- parent_of --> sioc:Forum (ChatChannel) — "Resources"
  |     +-- parent_of --> sioc:Forum (ChatChannel) — "Events"
  |-- host_of --> sioc:Forum (ChatChannel) — Side Channel A
  +-- host_of --> sioc:Forum (ChatChannel) — Side Channel B
```

### sioc:Thread
- Reply threads within topic channels (not topic channels themselves)
- Maps to `reply_to.reply_to_top_id` — a chain of replies
- Subclass of Container, child of Forum via `has_parent`

### sioc:Post / sioc_types:InstantMessage
- Every Telegram message. Contained in Forum or Thread via `has_container`.
- NOT contained in Community (Community is a Space, not a Container — spec violation fixed)

### sioc_types:Poll
- Subclass of `sioc:Item`, attached to Post via `tg:has_poll`
- Properties: question, answers with vote counts, quiz flag, closed, public_voters, multiple_choice
- The Post handles who/when/where; the Poll holds structured content

### sioc:User (NOT sioc:UserAccount)
- `sioc:UserAccount` doesn't exist in the spec. Using `sioc:User` (subclass of `foaf:OnlineAccount`)
- Represents the Telegram account, not the human
- Bots: `tg:is_bot` boolean flag

### foaf:Person
- Real human behind one or more User accounts
- **Created 1:1 per User now** — sets up cross-platform foundation
- Linked via `foaf:holdsAccount` → User, User `sioc:account_of` → Person

### skos:Concept
- Topics/hashtags as first-class entities with minted URIs (`tg:topic/{tag}`)
- `sioc:topic` → Concept instances (not plain strings)

### foaf:Document — Attachments
- **LinkML class: `Attachment`**, `class_uri: foaf:Document`
- Media files attached to Posts via `sioc:attachment`
- Properties: `dcterms:format` (mime type), `dcterms:extent` (file size), `tg:media_type`, `tg:duration`
- URI: `tg:attachment/{message_id}/{index}`

### foaf:Document — Links
- **LinkML class: `LinkedDocument`**, `class_uri: foaf:Document`
- Web pages linked from Posts via `sioc:links_to`
- Properties: `dc:title`, `dcterms:description`, `dcterms:creator`, `tg:site_name`
- URI: the URL itself
- Metadata from Telegram's WebPage preview (free in message data)

> Two LinkML classes, one RDF type. Distinguished by the SIOC property (`sioc:attachment` vs `sioc:links_to`), not by class. SIOC deliberately leaves both ranges open; `foaf:Document` is SIOC-native.

### tg:Reaction (schema-only for v1)
- Modeled in schema but not populated yet
- Properties: reactor (→ User), emoji, target (→ Post)
- Current data: aggregate emoji+count from message data (no per-user attribution without extra API calls)

### GraphDocument (LinkML tree_root)
- Flat collections of all entity types — idiomatic LinkML
- The structural hierarchy lives in relationships (site host_of forum, etc.)
- In RDF output, GraphDocument disappears — just triples

---

## Property Decisions

| Property | Mapping | Notes |
|----------|---------|-------|
| Identifiers | `sioc:id` | Not `dcterms:identifier`. "Unique per type per site." |
| User display name | `sioc:name` | For SIOC instances |
| Person name | `foaf:name` | For the human |
| Username | `foaf:accountName` | Login/@handle |
| Content | `sioc:content` | Plain text |
| Rich content | `content:encoded` | **Deferred** — investigate Telethon HTML export later |
| Created | `dcterms:created` | Timestamp |
| Modified | `dcterms:modified` | Edit timestamp |
| Authorship | `sioc:has_creator` / `sioc:creator_of` | Both directions |
| Replies | `sioc:reply_of` / `sioc:has_reply` | Both directions |
| Forwards | `sioc:sibling` | Spec: "twin Post in different Forum." Mint URI from fwd_from data. |
| Topics | `sioc:topic` → `skos:Concept` | Minted URIs, not strings |
| Quotes | `tg:quote_text` | Text quoted in a reply |
| Albums | `tg:grouped_id` | Same ID = same album. Query-time grouping. |
| Inline bots | `tg:via_bot` → User | Bot used to send message |
| Pinned | `tg:pinned` | Boolean |
| Forward count | `tg:forwards` | Integer |
| Forum closed | `tg:closed` | Boolean, topic is closed/archived |
| Join date | `tg:join_date` | When User joined Forum |

---

## Deferred (explicit)

| Item | Reason |
|------|--------|
| **sioc:Role** | No admin/moderator modeling for v1. Derive later from participant data. |
| **Per-user Reactions** | Requires extra API call per message. Schema has the class; data not populated. |
| **content:encoded** | Reconstructing HTML from Telegram entities is complex. Plain text suffices for now. |
| **Service actions** | Absorbed into entity properties (Forum created/closed, Post pinned, User joined). No separate class. |
| **num_views, num_replies** | Operational/derivable. Removed from schema. |
| **Chronological chains** | No `next_by_date`/`previous_by_date`. Timestamps + ORDER BY. |

---

## Namespace Usage

| Prefix | Namespace | Use |
|--------|-----------|-----|
| `sioc:` | `http://rdfs.org/sioc/ns#` | Core classes and properties |
| `sioc_types:` | `http://rdfs.org/sioc/types#` | ChatChannel, InstantMessage, Poll |
| `foaf:` | `http://xmlns.com/foaf/0.1/` | Person, Document, holdsAccount, name, accountName |
| `dcterms:` | `http://purl.org/dc/terms/` | created, modified, hasPart, isPartOf, description, format, extent, creator |
| `dc:` | `http://purl.org/dc/elements/1.1/` | title (for links) |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Concept, prefLabel |
| `content:` | `http://purl.org/rss/1.0/modules/content/` | encoded (deferred) |
| `tg:` | `https://example.org/telegram/` | Telegram-specific extensions |

---

## tg: Extensions

| Term | Type | Domain | Description |
|------|------|--------|-------------|
| `tg:Reaction` | Class | — | Reaction entity (deferred) |
| `tg:is_bot` | Property | User | Bot flag |
| `tg:via_bot` | Property | Post | Inline bot → User |
| `tg:quote_text` | Property | Post | Quoted text in reply |
| `tg:grouped_id` | Property | Post | Album group ID |
| `tg:pinned` | Property | Post | Pinned flag |
| `tg:forwards` | Property | Post | Forward count |
| `tg:media_type` | Property | Attachment | photo, video, voice, etc. |
| `tg:duration` | Property | Attachment | Audio/video length |
| `tg:site_name` | Property | LinkedDocument | Source site name |
| `tg:closed` | Property | Forum | Closed/archived flag |
| `tg:join_date` | Property | User | When user joined Forum |
| `tg:invited_by` | Property | User | Who invited → User |
| `tg:has_poll` | Property | Post | Attached Poll |
| `tg:reactor` | Property | Reaction | Who reacted → User |
| `tg:emoji` | Property | Reaction | Reaction emoji |
| `tg:target` | Property | Reaction | Post reacted to |

---

## Key Findings

1. **Raw message JSON already contains** polls, media metadata, WebPage previews, reactions (aggregate + recent per-user), and forward source references. Extract expansion is mainly about forum structure.
2. **`foaf:Document`** is the idiomatic SIOC choice for attachments and links. The property distinguishes them, not the type.
3. **`sioc:id`** is the correct SIOC identifier — "unique per type per site."

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Two LinkML classes → same `foaf:Document` class_uri | High | Test early with `just validate` + `just gen-model` |
| Serialize breaks with deeper entity structure | Medium | Test after schema phase |
| Forum extraction (Telethon API limits) | Medium | Extend existing GetForumTopicsRequest |
| `sioc:id` + `identifier: true` in LinkML | Medium | Test that LinkML handles this correctly |
| sioc_types typing (ChatChannel, InstantMessage) | Medium | Research class_uri vs type mixins |
| Poll data not in current test data | Low | Write code; test when polls exist |

## Open Questions (resolve during implementation)

1. **sioc_types typing**: How to express Forum-as-ChatChannel and Post-as-InstantMessage in LinkML?
2. **Bidirectional properties**: Use LinkML `inverse` for reply_of/has_reply, or manage both in transform?
3. **Forum-as-container**: Express `container_of` as refs (not inlined) in LinkML JSON.
