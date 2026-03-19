# Graph Inventory

A snapshot of what's currently in the knowledge graph. Numbers below are from `just demo` and SPARQL queries against `data/rdf/sioc_graph.ttl`.

> To regenerate: `just extract 7 && just build && just demo`

## Community

| Field | Value |
|-------|-------|
| **Name** | Sensemaking Scenius |
| **Site** | Telegram |
| **Date range** | *(depends on extraction window)* |

## Coverage

| Entity | Count |
|--------|------:|
| Posts | 332 |
| Users | 21 |
| Forums | 29 |
| Threads | 14 |
| Attachments | 27 |
| Linked documents | 136 |
| Concepts (hashtags) | *(varies)* |

## Entity Hierarchy

```
sioc:Community — "Sensemaking Scenius"
  +-- dcterms:hasPart --> sioc:Site — "Telegram"
        +-- sioc:host_of --> sioc:Forum — Supergroup (organizational)
              +-- sioc:parent_of --> sioc:Forum — topic channels
```

## Schema → RDF Mapping

How Telegram fields map through the schema to RDF predicates:

| Telegram field | LinkML class/slot | RDF predicate |
|---------------|-------------------|---------------|
| message text | Post.content | `sioc:content` |
| date | Post.created | `dcterms:created` |
| edit_date | Post.modified | `dcterms:modified` |
| from_id | Post.has_creator | `sioc:has_creator` → User |
| peer_id / reply_to.forum_topic | Post.has_container | `sioc:has_container` → Forum |
| reply_to.reply_to_msg_id | Post.reply_of | `sioc:reply_of` → Post |
| *(inverse, built in transform)* | Post.has_reply | `sioc:has_reply` → Post |
| fwd_from (channel_id + msg_id) | Post.sibling | `sioc:sibling` → Post (minted URI) |
| entities (hashtags) | Post.topics → Concept | `sioc:topic` → `skos:Concept` |
| webpage preview | Post.links_to → LinkedDocument | `sioc:links_to` → `foaf:Document` |
| media (photo/video/doc) | Post.attachment → Attachment | `sioc:attachment` → `foaf:Document` |
| poll | Post.has_poll → Poll | `tg:has_poll` → `sioc_types:Poll` |
| forwards count | Post.forwards | `tg:forwards` |
| pinned | Post.pinned | `tg:pinned` |
| reply_to.quote_text | Post.quote_text | `tg:quote_text` |
| grouped_id | Post.grouped_id | `tg:grouped_id` |
| via_bot_id | Post.via_bot | `tg:via_bot` → User |
| user.first_name | User.sioc_name | `sioc:name` |
| user.username | User.username | `foaf:accountName` |
| user.bot | User.is_bot | `tg:is_bot` |
| *(1:1 from User)* | Person.name | `foaf:name` |
| *(1:1 from User)* | Person.holds_account | `foaf:holdsAccount` → User |
| channel.title | Community.name | `foaf:name` |
| channel.about | Community.description | `dcterms:description` |
| forum topic.title | Forum.name | `sioc:name` |
| forum topic.closed | Forum.closed | `tg:closed` |
| media.mime_type | Attachment.format | `dcterms:format` |
| media.size | Attachment.extent | `dcterms:extent` |
| media type | Attachment.media_type | `tg:media_type` (MediaType enum) |
| media.duration | Attachment.duration | `tg:duration` |
| webpage.title | LinkedDocument.title | `dc:title` |
| webpage.description | LinkedDocument.doc_description | `dcterms:description` |
| webpage.author | LinkedDocument.doc_creator | `dcterms:creator` |
| webpage.site_name | LinkedDocument.site_name | `tg:site_name` |

## Sample SPARQL Queries

### Forum activity

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>

SELECT ?name (COUNT(?post) AS ?posts)
WHERE {
  ?post a sioc:Post ;
        sioc:has_container ?forum .
  ?forum sioc:name ?name .
}
GROUP BY ?name
ORDER BY DESC(?posts)
```

### Reply network

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>

SELECT ?from ?to (COUNT(*) AS ?replies)
WHERE {
  ?reply sioc:has_creator ?replier ;
         sioc:reply_of ?parent .
  ?parent sioc:has_creator ?original .
  ?replier sioc:name ?from .
  ?original sioc:name ?to .
}
GROUP BY ?from ?to
ORDER BY DESC(?replies)
LIMIT 10
```

### Media breakdown

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX tg:   <https://example.org/telegram/>

SELECT ?mtype (COUNT(?att) AS ?count)
WHERE {
  ?post sioc:attachment ?att .
  ?att tg:media_type ?mtype .
}
GROUP BY ?mtype
ORDER BY DESC(?count)
```

### Shared links

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX dc:   <http://purl.org/dc/elements/1.1/>

SELECT ?title (COUNT(?post) AS ?shares)
WHERE {
  ?post sioc:links_to ?doc .
  ?doc dc:title ?title .
}
GROUP BY ?title
ORDER BY DESC(?shares)
LIMIT 10
```
