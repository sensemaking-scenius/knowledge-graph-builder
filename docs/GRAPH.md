# Graph Inventory

A snapshot of what's currently in the knowledge graph. Numbers below are from `just demo` and SPARQL queries against `data/rdf/sioc_graph.ttl`.

> To regenerate: `just extract 7 && just build && just demo`

## Community

| Field | Value |
|-------|-------|
| **Name** | Sensemaking Scenius |
| **Members** | 71 |
| **Date range** | Mar 4 – Mar 11, 2026 |
| **Extraction** | ~7 days (date-bounded) |

## Coverage

| Metric | Count |
|--------|------:|
| Posts | 86 |
| Contributors | 15 |
| Shared links | 33 |
| Replies | 79 |
| Forum threads | 13 |
| Total triples | 1,178 |

## Forum Threads

13 threads (11 named, 2 unnamed/ad-hoc):

| Thread | Posts |
|--------|------:|
| Events | 18 |
| Asks n Offers | 16 |
| Scenius Workshop | 9 |
| Links | 9 |
| Welcome Wagon | 5 |
| New Website [WG] | 4 |
| Community wrangling | 4 |
| Fundraising Support | 3 |
| Proposals | 2 |
| Sensemaking Frameworks | 0* |
| AI Tools Library | 0* |

\* Present in topic list but no posts in the current extraction window.

## Data Richness

How many of the 86 posts have each feature:

| Feature | Posts | % |
|---------|------:|--:|
| Has reactions | 43 | 50% |
| Has been edited | 46 | 53% |
| Has media attachment | 25 | 29% |
| Has reply parent | 79 | 92% |
| Is forwarded | 2 | 2% |
| Is service action | 1 | 1% |

### Media Breakdown

| Type | Posts |
|------|------:|
| webpage | 16 |
| photo | 9 |

## Schema → RDF Mapping

How Telegram fields map through the schema to RDF predicates:

| Telegram field | LinkML slot | RDF predicate |
|---------------|-------------|---------------|
| message text | `content` | `sioc:content` |
| date | `created` | `dcterms:created` |
| edit_date | `modified` | `dcterms:modified` |
| from_id | `has_creator` | `sioc:has_creator` |
| peer_id | `has_container` | `sioc:has_container` |
| reply_to.reply_to_msg_id | `reply_to` | `sioc:reply_of` |
| reply_to.reply_to_top_id | `has_thread` | `tg:has_thread` |
| entities (URLs) | `links_to` | `sioc:links_to` |
| entities (hashtags) | `topics` | `sioc:topic` |
| entities (mentions) | `mentions` | `tg:mentions` |
| forwards | `forwards` | `tg:forwards` |
| pinned | `pinned` | `tg:pinned` |
| views | `num_views` | `sioc:num_views` |
| replies.replies | `num_replies` | `sioc:num_replies` |
| reactions (count) | `reaction_count` | `tg:reaction_count` |
| reactions (emojis) | `reactions` | `tg:reactions` |
| media type | `media_type` | `tg:media_type` |
| fwd_from | `forwarded_from` | `tg:forwarded_from` |
| service action | `is_service` / `service_action` | `tg:is_service` / `tg:service_action` |
| user.username | `username` | `foaf:accountName` |
| user.first_name | `name` | `foaf:name` |
| user.bot | `is_bot` | `tg:is_bot` |
| user.verified | `is_verified` | `tg:is_verified` |
| user.premium | `is_premium` | `tg:is_premium` |
| channel.title | `name` | `foaf:name` |
| channel.about | `description` | `dcterms:description` |
| channel.members_count | `member_count` | `tg:member_count` |
| forum topic.title | `name` (Thread) | `foaf:name` |
| forum topic.parent | `has_parent` | `sioc:has_parent` |

## Sample SPARQL Queries

### Most reacted posts

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX tg:   <https://example.org/telegram/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?author ?content ?count
WHERE {
  ?post a sioc:Post ;
        sioc:content ?content ;
        sioc:has_creator ?user ;
        tg:reaction_count ?count .
  ?user foaf:accountName ?author .
}
ORDER BY DESC(?count)
LIMIT 10
```

### Thread activity

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX tg:   <https://example.org/telegram/>

SELECT ?name (COUNT(?post) AS ?posts)
WHERE {
  ?post a sioc:Post ;
        tg:has_thread ?thread .
  ?thread foaf:name ?name .
}
GROUP BY ?name
ORDER BY DESC(?posts)
```

### Posts with media

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX tg:   <https://example.org/telegram/>

SELECT ?mtype (COUNT(?post) AS ?count)
WHERE {
  ?post a sioc:Post ;
        tg:media_type ?mtype .
}
GROUP BY ?mtype
ORDER BY DESC(?count)
```

### Reply network

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?from ?to (COUNT(*) AS ?replies)
WHERE {
  ?reply sioc:has_creator ?replier ;
         sioc:reply_of ?parent .
  ?parent sioc:has_creator ?original .
  ?replier foaf:accountName ?from .
  ?original foaf:accountName ?to .
}
GROUP BY ?from ?to
ORDER BY DESC(?replies)
LIMIT 10
```
