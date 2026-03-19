# SIOC Core Ontology — Complete Specification Reference

> Source: [W3C Member Submission, 12 June 2007](https://www.w3.org/submissions/sioc-spec/)
> Namespace: `http://rdfs.org/sioc/ns#`
> Revision: 1.26

This document is a comprehensive reference for aligning our LinkML schema (`schemas/sioc.yaml`) to the SIOC specification. It covers every class, property, module, and external vocabulary integration defined in the spec, followed by a mapping analysis against our current schema.

---

## Table of Contents

1. [Namespaces](#namespaces)
2. [Core Classes (11)](#core-classes)
3. [Object Properties (48)](#object-properties)
4. [Datatype Properties (12)](#datatype-properties)
5. [SIOC Types Module](#sioc-types-module)
6. [SIOC Services Module](#sioc-services-module)
7. [External Vocabulary Integration](#external-vocabulary-integration)
8. [Design Principles](#design-principles)
9. [Conformance](#conformance)
10. [Mapping Analysis: Current Schema vs Spec](#mapping-analysis)

---

## Namespaces

| Prefix | URI | Purpose |
|--------|-----|---------|
| `sioc:` | `http://rdfs.org/sioc/ns#` | SIOC Core Ontology |
| `sioc_types:` | `http://rdfs.org/sioc/types#` | SIOC Types Module |
| `sioc_services:` | `http://rdfs.org/sioc/services#` | SIOC Services Module |
| `foaf:` | `http://xmlns.com/foaf/0.1/` | Friend of a Friend |
| `dc:` | `http://purl.org/dc/elements/1.1/` | Dublin Core Elements |
| `dcterms:` | `http://purl.org/dc/terms/` | Dublin Core Terms |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | SKOS Core Vocabulary |
| `content:` | `http://purl.org/rss/1.0/modules/content/` | RSS 1.0 Content Module |
| `aowl:` | `http://bblfish.net/work/atom-owl/2006-06-06/AtomOwl.rdf` | AtomOwl |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | XML Schema Datatypes |

> When might the other namespaces be useful and used such as: sioc_types, sioc_services, foaf, dc, dcterms, skos, content, aowl, and xsd?
---

## Core Classes

### 1. `sioc:Community`

- **Superclass**: `sioc:Space`
- **Definition**: A high-level concept that defines an online community and what it consists of.
- **Scope**: Joins people and sites via common topics, interests, or goals. Differs from Site — a Site is a single community site; a Community can encompass multiple Sites and resources.
- **Key properties**: `dcterms:hasPart` (to link constituent parts)

> So "Community" would be the overarching "Sensemaking Scenius" community. Not the telegram we use, not our website, not anything else. It's our whole community?

### 2. `sioc:Container`

- **Definition**: An area in which content Items are contained. High-level grouping mechanism.
- **Hierarchy**: Parent/child relationships via `sioc:has_parent` / `sioc:parent_of`
- **Domain for**: `container_of`, `has_owner`, `has_parent`, `has_subscriber`, `parent_of`
- **Range for**: `has_container`, `has_parent`, `owner_of`, `parent_of`, `subscriber_of`

### 3. `sioc:Forum` (subclass of `sioc:Container`)

- **Definition**: A discussion area on which Posts or entries are made.
- **Characteristics**: Has moderators, subscribers, topic focus, hierarchical structure.
- **Examples**: Mailing lists, message boards, Usenet newsgroups, weblogs.
- **Domain for**: `has_host`, `has_moderator`, `scope_of`
- **Range for**: `has_scope`, `host_of`, `moderator_of`
- **SIOC Types subclasses**: `ArgumentativeDiscussion`, `ChatChannel`, `MailingList`, `MessageBoard`, `Weblog`

### 4. `sioc:Item` (subclass of `foaf:Document`)

- **Definition**: A content Item that can be posted to or created within a Container.
- **Domain for**: `about`, `has_container`, `has_creator`, `has_modifier`, `has_reply`, `ip_address`, `next_by_date`, `next_version`, `previous_by_date`, `previous_version`, `reply_of`
- **Range for**: `container_of`, `creator_of`, `has_reply`, `modifier_of`, `next_by_date`, `next_version`, `previous_by_date`, `previous_version`, `reply_of`

### 5. `sioc:Post` (subclass of `sioc:Item`)

- **Definition**: An article or message that can be posted to a Forum.
- **Characteristics**: Posted by User to Forum. May be threaded. Can have content and attachments.
- **Domain for**: `attachment`, `content`, `note`, `num_replies`, `related_to`, `sibling`
- **Range for**: `related_to`, `sibling`
- **SIOC Types subclasses**: `BlogPost`, `BoardPost`, `Comment`, `InstantMessage`, `MailMessage`, `WikiArticle`

### 6. `sioc:Role`

- **Definition**: A function of a User within a scope of a particular Forum, Site, etc.
- **Purpose**: Express functions or access control privileges.
- **Domain for**: `function_of`, `has_scope`
- **Range for**: `has_function`, `scope_of`

### 7. `sioc:Site` (subclass of `sioc:Space`)

- **Definition**: The location of an online community or set of communities — a web-accessible data Space.
- **Domain for**: `has_administrator`, `host_of`
- **Range for**: `administrator_of`, `has_host`

### 8. `sioc:Space`

- **Definition**: A place where data resides (website, desktop, fileshare, etc.).
- **Domain for**: `has_usergroup`, `space_of`
- **Range for**: `has_space`, `usergroup_of`

### 9. `sioc:Thread` (subclass of `sioc:Container`)

- **Definition**: A container for a series of threaded discussion Posts or Items.
- **Purpose**: Groups Posts from a single discussion thread. Useful where `has_reply`/`reply_of` structure is absent.

### 10. `sioc:User` (subclass of `foaf:OnlineAccount`)

- **Definition**: A User account in an online community site.
- **Integration**: Combines with `foaf:Person` (via `foaf:holdsAccount`) — `sioc:User` describes account-specific properties; `foaf:Person` describes the individual.
- **Domain for**: `account_of`, `administrator_of`, `avatar`, `creator_of`, `email`, `email_sha1`, `has_function`, `member_of`, `moderator_of`, `modifier_of`, `owner_of`, `subscriber_of`
- **Range for**: `function_of`, `has_administrator`, `has_creator`, `has_member`, `has_moderator`, `has_modifier`, `has_owner`, `has_subscriber`

### 11. `sioc:Usergroup`

- **Definition**: A set of User accounts whose owners have a common purpose or interest. Can be used for access control.
- **Domain for**: `has_member`, `usergroup_of`
- **Range for**: `has_usergroup`, `member_of`

> I need help understanding how to structure things in a broad sense using these classes. The Sensemaking Scenius community is our digital/physical community. We mainly use a telegram supergroup to communicate with each other; the telegram group is a supergroup with 'topic' channels that all members have access to and also forthcoming opt-in side channels/groups in telegram that are not part of the supergroup. We also have various video/voice calls in Zoom, Google Meet, etc. We also have a Notion. We also have a website. We also have this knowledge graph project that will be useful and used by the community. Members also have their own personal websites and projects. We also have a GitHub. We also have a Google workspace. So what might the class structure be for all of this?
---

## Object Properties

| # | Property | Domain | Range | Inverse | Description |
|---|----------|--------|-------|---------|-------------|
| 1 | `sioc:about` | Item | *(open)* | — | Subject matter of an Item |
| 2 | `sioc:account_of` | User | foaf:Agent | *(foaf:holdsAccount)* | Links User to the foaf:Agent who owns the account |
| 3 | `sioc:administrator_of` | User | Site | `has_administrator` | Site that User administers |
| 4 | `sioc:attachment` | Post | *(open)* | — | URI of a file attached to a Post |
| 5 | `sioc:avatar` | User | *(open)* | — | Image/depiction representing User |
| 6 | `sioc:container_of` | Container | Item | `has_container` | Item contained in this Container |
| 7 | `sioc:creator_of` | User | Item | `has_creator` | Item that User created |
| 8 | `sioc:email` | User | *(open)* | — | Email address of User |
| 9 | `sioc:feed` | *(open)* | *(open)* | — | RSS/Atom feed for a resource |
| 10 | `sioc:function_of` | Role | User | `has_function` | User who has this Role |
| 11 | `sioc:has_administrator` | Site | User | `administrator_of` | User who administers this Site |
| 12 | `sioc:has_container` | Item | Container | `container_of` | Container to which Item belongs |
| 13 | `sioc:has_creator` | Item | User | `creator_of` | User who made this Item |
| 14 | `sioc:has_function` | User | Role | `function_of` | Role that User has |
| 15 | `sioc:has_host` | Forum | Site | `host_of` | Site hosting this Forum |
| 16 | `sioc:has_member` | Usergroup | User | `member_of` | User who is member of Usergroup |
| 17 | `sioc:has_moderator` | Forum | User | `moderator_of` | User who moderates this Forum |
| 18 | `sioc:has_modifier` | Item | User | `modifier_of` | User who modified this Item |
| 19 | `sioc:has_owner` | Container | User | `owner_of` | User who owns this Container |
| 20 | `sioc:has_parent` | Container | Container | `parent_of` | Parent Container |
| 21 | `sioc:has_reply` | Item | Item | `reply_of` | Item that is a reply to this Item |
| 22 | `sioc:has_scope` | Role | Forum | `scope_of` | Forum to which Role applies |
| 23 | `sioc:has_space` | *(open)* | Space | `space_of` | Data Space containing this resource |
| 24 | `sioc:has_subscriber` | Container | User | `subscriber_of` | User subscribed to this Container |
| 25 | `sioc:has_usergroup` | Space | Usergroup | `usergroup_of` | Usergroup with access to Space |
| 26 | `sioc:host_of` | Site | Forum | `has_host` | Forum hosted on this Site |
| 27 | `sioc:link` | *(open)* | *(open)* | — | URI of document containing this SIOC object (rarely needed) |
| 28 | `sioc:links_to` | *(open)* | *(open)* | — | Links extracted from hyperlinks (subproperty of `dcterms:references`) |
| 29 | `sioc:member_of` | User | Usergroup | `has_member` | Usergroup that User belongs to |
| 30 | `sioc:moderator_of` | User | Forum | `has_moderator` | Forum that User moderates |
| 31 | `sioc:modifier_of` | User | Item | `has_modifier` | Item that User modified |
| 32 | `sioc:next_by_date` | Item | Item | `previous_by_date` | Next Item in Container by date |
| 33 | `sioc:next_version` | Item | Item | `previous_version` | Next revision of this Item |
| 34 | `sioc:owner_of` | User | Container | `has_owner` | Container owned by User |
| 35 | `sioc:parent_of` | Container | Container | `has_parent` | Child Container |
| 36 | `sioc:previous_by_date` | Item | Item | `next_by_date` | Previous Item in Container by date |
| 37 | `sioc:previous_version` | Item | Item | `next_version` | Previous revision of this Item |
| 38 | `sioc:related_to` | Post | Post | — | Related Posts (by topic/reference) |
| 39 | `sioc:reply_of` | Item | Item | `has_reply` | Item this is a reply to |
| 40 | `sioc:scope_of` | Forum | Role | `has_scope` | Role scoped to this Forum |
| 41 | `sioc:sibling` | Post | Post | *(symmetric)* | Twin Post in different Forum (symmetric property) |
| 42 | `sioc:space_of` | Space | *(open)* | `has_space` | Resource belonging to this Space |
| 43 | `sioc:subscriber_of` | User | Container | `has_subscriber` | Container User is subscribed to |
| 44 | `sioc:topic` | *(open)* | *(open)* | — | Topic of interest (subproperty of `dc:subject`). Used for categories/tags. |
| 45 | `sioc:usergroup_of` | Usergroup | Space | `has_usergroup` | Space the Usergroup accesses |

---

## Datatype Properties

| # | Property | Domain | Range | Description |
|---|----------|--------|-------|-------------|
| 1 | `sioc:content` | Post | rdfs:Literal | Plain-text content of Post. Rich content via `content:encoded` or AtomOwl. |
| 2 | `sioc:email_sha1` | User | rdfs:Literal | SHA1-encoded email address |
| 3 | `sioc:id` | *(open)* | rdfs:Literal | Identifier, unique per type per site |
| 4 | `sioc:ip_address` | Item | rdfs:Literal | IP address used when creating Item |
| 5 | `sioc:name` | *(open)* | rdfs:Literal | Name of SIOC instance (username, group name, etc.) |
| 6 | `sioc:note` | Post | rdfs:Literal | Editorial note (e.g., "edited by User") |
| 7 | `sioc:num_replies` | Post | xsd:integer | Number of replies (useful when reply structure absent) |
| 8 | `sioc:num_views` | *(open)* | xsd:integer | View count for Item, Thread, User profile, etc. |

---

## SIOC Types Module

**Namespace**: `http://rdfs.org/sioc/types#`

Extends core ontology with specialized sub-types without adding complexity to the core.

### Container Subclasses

`AddressBook`, `AnnotationSet`, `AudioChannel`, `BookmarkFolder`, `Briefcase`, `EventCalendar`, `ImageGallery`, `ProjectDirectory`, `ResumeBank`, `ReviewArea`, `SubscriptionList`, `SurveyCollection`, `VideoChannel`, `Wiki`

> Lots of cool stuff in here that would be useful.

### Forum Subclasses

`ArgumentativeDiscussion`, `ChatChannel`, `MailingList`, `MessageBoard`, `Weblog`

> ChatChannel, MessageBoard, and Weblog are interesting, how might they be useful?

### Post Subclasses

`BlogPost`, `BoardPost`, `Comment`, `InstantMessage`, `MailMessage`, `WikiArticle`

> BlogPost, BoardPost, Comment, InstantMessage are interesting, how might they be useful?

### Item Subclasses

`Poll`

> Telegram has polls, maybe we could use this?

---

## SIOC Services Module

**Namespace**: `http://rdfs.org/sioc/services#`

- **Class**: `sioc_services:Service` — indicates web service associated with a Site or part thereof
- **Property**: `sioc_services:service_definition` — links to full service definition (e.g., WSDL)

> When might we use this and why?

---

## External Vocabulary Integration

The SIOC spec explicitly integrates with these external vocabularies:

### Classes

| Class | Usage with SIOC |
|-------|-----------------|
| `foaf:Person` | The person who holds a `sioc:User` account (linked via `foaf:holdsAccount`) |
| `foaf:OnlineAccount` | Superclass of `sioc:User` |
| `foaf:Agent` | Range of `sioc:account_of` |
| `skos:Concept` | Topics/tags — linked from Items via `sioc:topic` |

> Seems like we should be using foaf as the highest level for people in the community?

### Properties

| Property | Usage with SIOC |
|----------|-----------------|
| `dc:subject` | Keywords describing Item subject (superclass of `sioc:topic`) |
| `dc:title` | Title of Item or Post |
| `dcterms:created` | Creation timestamp |
| `dcterms:modified` | Modification timestamp |
| `dcterms:hasPart` | Part-whole relationships (Community, Post) |
| `dcterms:isPartOf` | Inverse of hasPart |
| `dcterms:references` | Superclass of `sioc:links_to` |
| `foaf:holdsAccount` | Links `foaf:Person` → `sioc:User` |
| `foaf:name` | Name of person/agent |
| `foaf:accountName` | Account username |
| `content:encoded` | Rich/HTML content of a Post (CDATA) |

> Seems like these will be useful?

---

## Design Principles

1. **Interoperability**: Link online community sites using Semantic Web technologies to find related information and new connections.
2. **Extensibility**: Core describes basics; RDF framework allows mixing with other vocabularies.
3. **Pragmatism**: Straightforward — designed for simultaneous deployment and extension at wide scale.
4. **Network perspective**: Items form networks linked to Users; enables community structure discovery.
5. **Vocabulary mixing**: Combines with Dublin Core, FOAF, RSS, AtomOwl without centralized agreement.

---

## Conformance

- All SIOC documents MUST be valid RDF documents.
- RFC 2119 keywords apply: MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, OPTIONAL.

---

## Mapping Analysis

### Current Schema vs SIOC Spec

Our schema (`schemas/sioc.yaml`) maps to SIOC as follows:

> This may have to be entirely reconsidered to make the most sense with this spec, our community structure, future growth, and the current docs/telethon-data-map.md we have available to us

#### Classes — What We Have

| Our Class | SIOC Class | Status | Notes |
|-----------|------------|--------|-------|
| `GraphDocument` | *(none)* | LinkML-only | Tree root container, no SIOC equivalent (correct) |
| `Community` | `sioc:Community` | Correct | Spec says Community is subclass of Space |
| `Thread` | `sioc:Thread` | Correct | Spec says Thread is subclass of Container |
| `UserAccount` | `sioc:UserAccount` | **Check** | Spec class is `sioc:User`, not `sioc:UserAccount`. The URI `sioc:UserAccount` doesn't exist in the spec. |
| `Link` | `schema:URL` | Non-SIOC | Uses schema.org, not SIOC. Spec uses `sioc:links_to` as a property, not a class. |
| `Post` | `sioc:Post` | Correct | Subclass of Item in spec |

#### Classes — What We're Missing (potentially useful)

| SIOC Class | Relevance to Telegram | Priority |
|------------|----------------------|----------|
| `sioc:Forum` | Could model the channel/group itself (as container for Posts). Spec: Forum is the discussion area, Community is the higher-level concept. | High — Telegram group/channel IS a Forum |
| `sioc:Site` | Could model Telegram-the-platform as a Site hosting Forums | Medium |
| `sioc:Container` | Abstract parent of Forum and Thread | Low (use Forum/Thread directly) |
| `sioc:Item` | Abstract parent of Post | Low (use Post directly) |
| `sioc:Space` | Abstract parent of Site and Community | Low |
| `sioc:Role` | Could model admin/moderator roles | Low |
| `sioc:Usergroup` | Could model admin groups | Low |

#### Properties — Alignment Check

| Our Slot | Our URI | Spec URI | Status |
|----------|---------|----------|--------|
| `id` | `dcterms:identifier` | `sioc:id` | **Diverges** — spec has `sioc:id` for SIOC identifiers; `dcterms:identifier` is valid but different |
| `name` | `foaf:name` | `sioc:name` | **Diverges** — spec has `sioc:name` for SIOC instances; `foaf:name` is for persons |
| `description` | `dcterms:description` | *(none specific)* | OK — no SIOC-specific description property |
| `username` | `foaf:accountName` | *(foaf integration)* | Correct — spec says User is subclass of foaf:OnlineAccount |
| `content` | `sioc:content` | `sioc:content` | Correct |
| `created` | `dcterms:created` | `dcterms:created` | Correct |
| `modified` | `dcterms:modified` | `dcterms:modified` | Correct |
| `has_creator` | `sioc:has_creator` | `sioc:has_creator` | Correct |
| `has_container` | `sioc:has_container` | `sioc:has_container` | Correct — but spec range is Container, we point to Community |
| `has_parent` | `sioc:has_parent` | `sioc:has_parent` | Correct — but spec domain/range is Container↔Container, we use Thread→Community |
| `reply_to` | `sioc:reply_of` | `sioc:reply_of` | Correct |
| `links_to` | `sioc:links_to` | `sioc:links_to` | Correct |
| `topics` | `sioc:topic` | `sioc:topic` | Correct — but spec range is open (URI/skos:Concept), we use plain string |
| `num_views` | `sioc:num_views` | `sioc:num_views` | Correct |
| `num_replies` | `sioc:num_replies` | `sioc:num_replies` | Correct |
| `has_thread` | `tg:has_thread` | *(none)* | Custom — no SIOC equivalent for Post→Thread. Spec would use Thread `container_of` Post. |
| `member_count` | `tg:member_count` | *(none)* | Custom — no SIOC equivalent |
| `is_bot` | `tg:is_bot` | *(none)* | Custom — Telegram-specific |
| `is_verified` | `tg:is_verified` | *(none)* | Custom — Telegram-specific |
| `is_premium` | `tg:is_premium` | *(none)* | Custom — Telegram-specific |
| `forwards` | `tg:forwards` | *(none)* | Custom |
| `pinned` | `tg:pinned` | *(none)* | Custom |
| `mentions` | `tg:mentions` | *(none)* | Custom |
| `entity_links` | `sioc:links_to` | `sioc:links_to` | Correct — but duplicates `links_to` slot URI |
| `reaction_count` | `tg:reaction_count` | *(none)* | Custom |
| `reactions` | `tg:reactions` | *(none)* | Custom |
| `media_type` | `tg:media_type` | *(none)* | Custom |
| `forwarded_from` | `tg:forwarded_from` | *(none)* | Custom |
| `is_service` | `tg:is_service` | *(none)* | Custom |
| `service_action` | `tg:service_action` | *(none)* | Custom |

#### SIOC Properties We Could Adopt

| Spec Property | Potential Use | Priority |
|---------------|--------------|----------|
| `sioc:has_host` | Forum → Site (channel hosted on Telegram) | Medium |
| `sioc:host_of` | Site → Forum (inverse) | Medium |
| `sioc:has_moderator` | Forum → User (Telegram admin/moderator) | Medium |
| `sioc:attachment` | Post → file URI (photos, documents, etc.) | High — replaces `media_type` with richer model |
| `sioc:avatar` | User → image URI | Low |
| `sioc:has_reply` | Inverse of `reply_of` — we only model one direction | Low |
| `sioc:container_of` | Container → Item (inverse of `has_container`) | Low |
| `sioc:note` | Post editorial note | Low |
| `sioc:sibling` | Cross-posted messages | Low |
| `sioc:feed` | RSS/Atom feed for channel | Low |
| `sioc:next_by_date` / `sioc:previous_by_date` | Chronological ordering | Low |

### Key Issues to Address

1. **`sioc:UserAccount` does not exist** — The spec class is `sioc:User`. Our `class_uri: sioc:UserAccount` is non-standard. Should be `sioc:User`.

2. **Missing `sioc:Forum`** — Telegram groups/channels are discussion forums. The spec distinguishes Community (high-level, multi-site) from Forum (specific discussion area). A Telegram group is a Forum within the Telegram Community/Site. Currently we use Community as the container, but `has_container` spec range is Container (Forum is a subclass of Container; Community is NOT).

3. **`has_container` range mismatch** — Spec: `Item → Container`. Our schema: `Post → Community`. Community is a subclass of Space, not Container. Posts should be contained in a Forum (or Thread), not a Community.

4. **`has_parent` domain/range mismatch** — Spec: `Container → Container`. We use: `Thread → Community`. If we add Forum, Thread's parent should be the Forum, not the Community.

5. **Duplicate `sioc:links_to`** — Both `links_to` and `entity_links` slots use the same URI `sioc:links_to`. This creates ambiguity in RDF serialization.

6. **`sioc:topic` range** — Spec expects URIs (e.g., SKOS concepts, DMOZ categories). We use plain strings. Consider minting URIs for hashtag topics or using `dc:subject` for string-based subjects.

7. **`sioc:name` vs `foaf:name`** — For SIOC instances (Users, Usergroups, Roles), the spec defines `sioc:name`. We use `foaf:name`, which is appropriate for the Person behind the account but not necessarily for the account itself. Since `sioc:User` is a subclass of `foaf:OnlineAccount`, `foaf:accountName` (which we use for `username`) is correct for the login name, but display names could use `sioc:name`.

### Recommended Structural Changes

```
Current:    Community ← has_container ← Post
Spec-aligned: Site → host_of → Forum ← has_container ← Post
              Community (high-level, may encompass multiple Forums)
              Thread ← has_parent ← Forum (Thread is child Container of Forum)
```

This would mean:
- **Telegram** = `sioc:Site`
- **A specific group/channel** = `sioc:Forum` (subclass of Container)
- **The broader community** = `sioc:Community` (optional, higher-level grouping)
- **Discussion threads** = `sioc:Thread` (subclass of Container, child of Forum)
- **Messages** = `sioc:Post` (contained in Forum or Thread)
- **Users** = `sioc:User` (not UserAccount)
