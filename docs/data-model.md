# Data Model Decisions — SIOC Alignment

Snapshot of decisions made while aligning our LinkML schema to the SIOC spec.
Reference docs: `docs/sioc-spec-reference.md`, `docs/telethon-data-map.md`

---

## Community Structure

**Sensemaking Scenius** is a `sioc:Community` — the top-level umbrella over all platforms and spaces the community uses. It is NOT the Telegram group, the website, or any single platform. It's the people, purpose, and shared identity.

Future scope (not modeled yet): community website, Notion, GitHub, Google Workspace, Zoom/Meet calls. Each would be a `sioc:Site` linked to the Community via `dcterms:hasPart`.

---

## Class Decisions

### sioc:Community
- Single instance: "Sensemaking Scenius"
- Superclass is `sioc:Space`
- Connected to Sites via `dcterms:hasPart`

### sioc:Site
- Telegram-the-platform is a `sioc:Site`
- Why Site and not others: Site is a "web-accessible data Space that hosts Forums, Users, and Usergroups." Telegram hosts forums (our groups), has users (accounts), and has usergroups (admins). It's not a Community (that's us), not a Forum (it contains many), not a raw Space (it's specifically web-accessible with structure).
- Connected back to Community via `dcterms:isPartOf` (inverse of `dcterms:hasPart`)
- Provides `host_of`, `has_administrator` relationships

### sioc:Forum — two distinct uses

**Supergroup (organizational parent):**
- Plain `sioc:Forum` with NO `sioc_types` specialization
- The supergroup (`forum=True` in Telegram) is an organizational container — you cannot send messages directly to it
- Connected to hosting Site via `sioc:has_host` (Forum → Site)
- Contains child Forums (topic channels) via `parent_of`

**Topic channels + side channels (where chat happens):**
- `sioc:Forum` typed as `sioc_types:ChatChannel`
- These are the actual discussion areas where messages are posted
- Topic channels are children of the supergroup Forum via `has_parent`
- Opt-in side channels are NOT children of the supergroup — they're independent Forums hosted on the same Site and part of the same Community

```
sioc:Site — "Telegram"
  |-- host_of --> sioc:Forum — Supergroup (plain Forum, organizational)
  |     |-- parent_of --> sioc:Forum (ChatChannel) — "General"
  |     |-- parent_of --> sioc:Forum (ChatChannel) — "Resources"
  |     +-- parent_of --> sioc:Forum (ChatChannel) — "Events"
  |-- host_of --> sioc:Forum (ChatChannel) — Side Channel A
  +-- host_of --> sioc:Forum (ChatChannel) — Side Channel B
```

### sioc:Thread
- For **reply threads** within topic channels (not for topic channels themselves)
- Maps to Telegram's `reply_to.reply_to_top_id` — a chain of replies to a message
- Thread is a subclass of `sioc:Container` (child of Forum via `has_parent`)
- Contains reply Posts via `container_of`

### sioc:Post / sioc_types:InstantMessage
- Every Telegram message is a `sioc:Post` typed as `sioc_types:InstantMessage`
- Contained in a Forum (topic channel) or Thread (reply chain) via `has_container`
- NOT contained in Community (that was a spec violation — Community is a Space, not a Container)

### sioc_types:Poll
- Telegram polls modeled as `sioc_types:Poll` (subclass of `sioc:Item`)
- Properties: question text, answer options, vote counts, quiz flag, closed status, public_voters, multiple_choice
- Polls are community decision artifacts worth preserving structurally
- **Containment**: attached to the Post that carries them (via `tg:has_poll`). Every Telegram message is a Post — polls are structured content of a Post, not standalone timeline items. The Post handles who/when/where; the Poll holds the structured content.

### sioc:User (NOT sioc:UserAccount)
- `sioc:UserAccount` does not exist in the spec — must be `sioc:User`
- `sioc:User` is a subclass of `foaf:OnlineAccount`
- Represents the Telegram account specifically, not the human behind it
- Bots are `sioc:User` instances with a `tg:is_bot` boolean flag (not a separate subclass)

### foaf:Person
- The real human behind one or more `sioc:User` accounts
- **Create Person per User now** — even if 1:1 for Telegram-only, it sets up the cross-platform foundation
- Linked to accounts via `foaf:holdsAccount -> sioc:User`
- A community member might have a Telegram account, GitHub account, personal website — all linked back to one `foaf:Person`
- Enables cross-platform queries: "everything this person did across all platforms"
- Minimal properties for now: `foaf:name`

### skos:Concept
- Topics/hashtags as first-class entities with minted URIs
- `sioc:topic` points to `skos:Concept` instances (not plain strings)
- Example: `tg:topic/sensemaking` -> `skos:Concept` with label "sensemaking"
- Enables topic taxonomy, cross-platform topic linking, richer queries

### sioc:Role
- Minimal `sioc:Role` instances linking User to Forum scope
- Properties: role type (admin / creator / member), custom title (rank), scope (Forum)
- Connected via `sioc:has_function` (User -> Role) and `sioc:has_scope` (Role -> Forum)
- No Usergroup class — admin status is derivable from Role instances
- No granular permission modeling — just the role type classification
- `sioc:has_moderator` on Forum points to admin Users directly (shortcut for common queries)
- `sioc:has_owner` on Forum points to the creator/owner User
- `sioc:has_subscriber` on Forum points to member Users (spec-native membership relationship)

### Attachments (foaf:Document via sioc:attachment)
- Attached media files typed as `foaf:Document` — native to SIOC's vocabulary (Item is already a subclass of foaf:Document)
- Linked from Post via `sioc:attachment` (spec property §4, open range)
- **Note**: the spec designed `sioc:attachment` as a simple URI pointer. Rich typing with metadata properties is an extension beyond spec intent, but permitted by the open range. We capture metadata here because it's free at extract time and expensive to reconstruct later.
- Standard metadata: `dcterms:format` (mime type), `dcterms:extent` (file size)
- Telegram-specific metadata: `tg:media_type` (photo, video, document, voice, sticker, etc.), `tg:duration` (audio/video length)
- URI minted per attachment (e.g., `tg:attachment/{message_id}/{index}`)

### Links (foaf:Document via sioc:links_to)
- Linked web pages typed as `foaf:Document`, enriched with Telegram's WebPage preview data
- Linked from Post via `sioc:links_to` (spec property §28, subproperty of `dcterms:references`)
- Standard metadata: `dc:title`, `dcterms:description`, `dcterms:creator` (author)
- Additional: `tg:site_name` (source site name from WebPage preview)
- This metadata comes free from Telethon — no extra API calls needed

### Reaction (new class, SIOC extension)
- First-class entities: each reaction is a node in the graph
- Properties: reactor (-> User), emoji/emoticon, target (-> Post)
- Modeled as a SIOC extension — `tg:Reaction` class that references `sioc:Post` and `sioc:User`
- Enables "what does person X react to most?" and sentiment/engagement analysis
- Per-user attribution when available (depends on `can_see_list` flag)

### Service actions — absorbed into entities
- Service messages (topic created, user joined, message pinned, etc.) are state changes, not content
- Absorbed into the entities they affect: Forum gets created/closed timestamps, User gets `tg:join_date`, Post gets `tg:pinned`
- No separate SystemNotification class — the resulting state on the entity is what matters for sensemaking

---

## Property Decisions

### Authorship: sioc:has_creator / sioc:creator_of
- `sioc:has_creator` (Item → User) — who created the Item. Inherited by all Item subclasses (Post, Poll, etc.)
- `sioc:creator_of` (User → Item) — inverse; what a User created
- Both directions modeled for bidirectional traversal

### Identifiers: sioc:id
- **Decided**: Use `sioc:id` (not `dcterms:identifier`)
- Spec: "identifier unique per type per site" — exactly what Telegram IDs are
- Aligns with SIOC-first philosophy

### Content: dual representation
- `sioc:content` — plain text (from `message.message`)
- `content:encoded` — rich/formatted content reconstructed from `message.message` + `message.entities` (bold, italic, code, links, etc.)

### Forwards: sioc:sibling
- Forwarded messages use `sioc:sibling` (spec-native symmetric property)
- Spec rationale: "A Post may have a sibling or a twin that exists in a different Forum, copied from one Forum to another"
- For inbound forwards from external channels, mint a URI from `fwd_from` data (`tg:post/{channel_id}/{message_id}`) — dangling reference that could be enriched later
- Focus: forwards within community and inbound forwards

### Topics: sioc:topic with minted URIs
- Use `sioc:topic` (not `dc:subject`) pointing to `skos:Concept` URIs
- Hashtags become first-class entities in the graph
- Plain string keywords could additionally use `dc:subject` if needed

### Naming
- `foaf:name` — for the Person (human's display name)
- `sioc:name` — for all SIOC instances (User display name, Forum name, Site name, etc.)
- `foaf:accountName` — for the login/username (already correct in current schema)

### Edits
- `dcterms:modified` — edit timestamp (from `message.edit_date`)
- `sioc:has_modifier` — who edited (usually the author)
- No version history (Telethon doesn't provide pre-edit content outside admin log)

### Replies: sioc:reply_of / sioc:has_reply
- `sioc:reply_of` (Post → Post it replies to) — the reply points to its parent
- `sioc:has_reply` (Post → Posts that reply to it) — the parent points to its replies
- Both directions modeled for bidirectional traversal

### Quotes
- When a reply quotes a specific passage, capture `quote_text` on the reply Post
- Strong sensemaking signal — shows exactly what someone is responding to
- Custom property: `tg:quote_text` (no SIOC equivalent)

### Cross-chat replies
- Model as `sioc:reply_of` pointing to a minted URI for the external Post
- Creates dangling references that could be enriched if that chat is ever ingested
- URI pattern: `tg:post/{chat_id}/{message_id}`

### Inline bots
- Track via `tg:via_bot` property on Post, pointing to the bot's `sioc:User` entity
- Shows how community members use bot tools in conversation

### User profiles
- `sioc:id` — Telegram numeric ID
- `sioc:name` — display name
- `foaf:accountName` — @username
- `sioc:account_of` — links User back to foaf:Person (inverse of `foaf:holdsAccount`)
- `tg:is_bot` — boolean flag
- `sioc:avatar` — profile photo URI
- `dcterms:description` — bio/about text (from UserFull)

### Forum metadata
- `dcterms:description` — supergroup about/description text
- `sioc:name` — Forum name/title
- `tg:closed` — boolean, whether a topic is closed (archived)
- No operational settings (slowmode, noforwards, etc.)

### Membership
- `tg:join_date` — when a User joined a Forum (from participant data)
- `tg:invited_by` — who invited them (-> User)
- Membership changes (join/leave/kick/ban) absorbed into User/Forum entity properties

### Chronological ordering
- **No** `sioc:next_by_date` / `sioc:previous_by_date` chains
- `dcterms:created` timestamps are sufficient; use SPARQL ORDER BY for chronological queries

### Related posts: sioc:related_to (future)
- `sioc:related_to` (Post → Post) — for Posts related by topic or reference, distinct from replies and forwards
- Not modeled now; potential future use for linking Posts that share topics, URLs, or concepts

### Albums
- `tg:grouped_id` property on Post
- Posts with the same grouped_id form an album
- Query-time grouping, no Album container class

---

## Namespace Usage

| Namespace | Status | Use in our schema |
|-----------|--------|-------------------|
| `sioc:` | Active | Core classes and properties |
| `sioc_types:` | Active | `ChatChannel`, `InstantMessage`, `Poll` type specializations |
| `foaf:` | Active | `Person`, `Document`, `holdsAccount`, `name`, `accountName` |
| `dcterms:` | Active | `created`, `modified`, `hasPart`, `isPartOf`, `description` |
| `dc:` | Active | `subject` for plain-text keywords |
| `skos:` | Active | `Concept` for topic entities |
| `content:` | Active | `encoded` for rich/formatted message content |
| `xsd:` | Implicit | Datatype ranges (integer, datetime, boolean) |
| `tg:` | Active | Telegram-specific extensions (see below) |
| `sioc_services:` | Future | SPARQL endpoint / knowledge graph service for the community |
| `aowl:` | Not needed | AtomOwl for Atom feeds — not relevant |

### tg: namespace properties and classes

| Term | Type | Domain | Description |
|------|------|--------|-------------|
| `tg:Reaction` | Class | — | Reaction entity (SIOC extension) |
| `tg:is_bot` | Property | User | Boolean: is a bot account |
| `tg:via_bot` | Property | Post | Inline bot used to send message (-> User) |
| `tg:quote_text` | Property | Post | Quoted passage text in a reply |
| `tg:grouped_id` | Property | Post | Album/media group identifier |
| `tg:pinned` | Property | Post | Boolean: message is pinned |
| `tg:forwards` | Property | Post | Forward count |
| `tg:media_type` | Property | foaf:Document | Telegram media type (photo, video, voice, sticker, etc.) |
| `tg:duration` | Property | foaf:Document | Audio/video duration |
| `tg:site_name` | Property | foaf:Document | Source site name (from WebPage preview) |
| `tg:closed` | Property | Forum | Boolean: topic is closed/archived |
| `tg:join_date` | Property | User | When user joined a Forum |
| `tg:invited_by` | Property | User | Who invited this user (-> User) |
| `tg:reactor` | Property | Reaction | Who reacted (-> User) |
| `tg:emoji` | Property | Reaction | Reaction emoji/emoticon |
| `tg:target` | Property | Reaction | Post being reacted to (-> Post) |
| `tg:has_poll` | Property | Post | Attached Poll entity (-> sioc_types:Poll) |

---

## Spec Violations Fixed (from original analysis)

| # | Issue | Resolution |
|---|-------|------------|
| 1 | `sioc:UserAccount` doesn't exist | Changed to `sioc:User` |
| 2 | `has_container` range is Community | Changed to Forum (Container subclass) |
| 3 | `has_parent` on Thread points to Community | Changed to point to Forum |
| 4 | Duplicate `sioc:links_to` | Merge into single `sioc:links_to` property |
| 5 | `sioc:topic` range is string | Changed to URI (`skos:Concept`) |
| 6 | Missing `sioc:Forum` | Added Forum class for supergroup and topic channels |
| 7 | Missing `foaf:Person` | Added Person class for real humans behind accounts |
| 8 | Missing `sioc:Site` | Added Site class for the Telegram platform |
| 9 | `dcterms:identifier` vs `sioc:id` | Switched to `sioc:id` |

---

## Out of Scope (Explicit)

- **Admin log events** — too granular, too operational for sensemaking
- **Group calls** — ephemeral, not captured well enough by Telegram data
- **Operational settings** — slowmode, noforwards, banned_rights, etc.
- **Chronological linked lists** — timestamps suffice for ordering
- **Usergroup class** — admin status derivable from Role instances
- **Granular permissions** — just role type, no 16-permission breakdown
- **Statistics API data** — growth/activity analytics, separate concern
- **Stories, paid messages, giveaways** — platform features, not sensemaking
- **Version history for edits** — no pre-edit content available
- **`sioc:num_replies`** — derivable via SPARQL COUNT on `reply_of`; no need to store
- **`sioc:num_views`** — operational analytics, not sensemaking; separate concern from knowledge graph

---

## Full Class Inventory

```
sioc:Community — "Sensemaking Scenius"
  +-- dcterms:hasPart --> sioc:Site — "Telegram"
        |-- host_of --> sioc:Forum — Supergroup (organizational)
        |     |-- parent_of --> sioc:Forum (ChatChannel) — topic channels
        |     |     |-- container_of --> sioc:Thread — reply threads
        |     |     |     +-- container_of --> sioc:Post (InstantMessage)
        |     |     +-- container_of --> sioc:Post (InstantMessage)
        |     +-- parent_of --> sioc:Forum (ChatChannel) — more topics...
        +-- host_of --> sioc:Forum (ChatChannel) — side channels

foaf:Person -- foaf:holdsAccount --> sioc:User -- sioc:account_of --> foaf:Person
  |-- has_function --> sioc:Role -- has_scope --> sioc:Forum
  +-- creator_of --> sioc:Post

sioc:Forum
  |-- has_owner --> sioc:User (creator)
  |-- has_moderator --> sioc:User (admins)
  +-- has_subscriber --> sioc:User (members)

sioc:Post (InstantMessage)
  |-- sioc:has_creator --> sioc:User
  |-- sioc:attachment --> foaf:Document (media files)
  |-- sioc:links_to --> foaf:Document (web pages)
  |-- sioc:topic --> skos:Concept
  |-- sioc:reply_of / sioc:has_reply --> sioc:Post (both directions)
  |-- sioc:sibling --> sioc:Post (forwards)
  +-- tg:target <-- tg:Reaction -- tg:reactor --> sioc:User

sioc_types:Poll (subclass of sioc:Item, attached to Post via tg:has_poll)
  +-- question, answers, vote counts, quiz flag, closed status
```
