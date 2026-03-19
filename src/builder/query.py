"""Demo stage: SPARQL queries → rich CLI community insights dashboard."""

from datetime import datetime
from typing import Any, cast

from pyoxigraph import RdfFormat, Store
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from builder.config import TURTLE_FILE

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SIOC = "http://rdfs.org/sioc/ns#"
SIOC_TYPES = "http://rdfs.org/sioc/types#"
DCTERMS = "http://purl.org/dc/terms/"
DC = "http://purl.org/dc/elements/1.1/"
FOAF = "http://xmlns.com/foaf/0.1/"
SKOS = "http://www.w3.org/2004/02/skos/core#"
TG = "https://example.org/telegram/"
XSD = "http://www.w3.org/2001/XMLSchema#"

PREFIXES = f"""
PREFIX sioc: <{SIOC}>
PREFIX sioc_types: <{SIOC_TYPES}>
PREFIX dcterms: <{DCTERMS}>
PREFIX dc: <{DC}>
PREFIX foaf: <{FOAF}>
PREFIX skos: <{SKOS}>
PREFIX tg: <{TG}>
PREFIX xsd: <{XSD}>
"""


def run_query(store: Store, sparql: str) -> list[dict[str, Any]]:
    """Execute a SPARQL SELECT and return rows as dicts of native values."""
    result = cast(Any, store.query(PREFIXES + sparql))
    variables = [v.value for v in result.variables]
    rows: list[dict[str, Any]] = []
    for row in result:
        d: dict[str, Any] = {}
        for var in variables:
            val = row[var]
            d[var] = val.value if val is not None else None
        rows.append(d)
    return rows


def short_uri(uri: str | None) -> str:
    """Strip common URI prefixes to a readable short form."""
    if uri is None:
        return ""
    for prefix, label in [
        (f"{TG}user/", "user/"),
        (f"{TG}channel/", "ch/"),
        (f"{TG}channel/2141367711/message/", "#"),
        (f"{TG}channel/2141367711/forum/", "forum/"),
    ]:
        if uri.startswith(prefix):
            return f"{label}{uri[len(prefix):]}"
    return truncate(uri, 60)


def display_name(name: str | None, user_uri: str | None) -> str:
    """Show name if available, otherwise fall back to short_uri."""
    if name:
        return name
    return short_uri(user_uri)


def format_date(iso: str | None) -> str:
    """Format an ISO datetime string into a readable form."""
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%b %d, %I:%M %p").replace(" 0", " ")
    except ValueError:
        return iso


def truncate(text: str | None, length: int = 72) -> str:
    """Truncate text with ellipsis."""
    if not text:
        return ""
    text = " ".join(text.split())
    if len(text) <= length:
        return text
    return text[: length - 1] + "…"


# ---------------------------------------------------------------------------
# Query sections
# ---------------------------------------------------------------------------


def community_overview(console: Console, store: Store) -> None:
    """Section 1: aggregate counts and date range."""
    rows = run_query(store, """
        SELECT
            (COUNT(DISTINCT ?post) AS ?posts)
            (COUNT(DISTINCT ?user) AS ?users)
            (COUNT(DISTINCT ?forum) AS ?forums)
            (COUNT(DISTINCT ?doc) AS ?links)
            (MIN(?date) AS ?earliest)
            (MAX(?date) AS ?latest)
        WHERE {
            ?post a sioc:Post .
            ?post dcterms:created ?date .
            OPTIONAL { ?post sioc:has_creator ?user . }
            OPTIONAL { ?forum a sioc:Forum . }
            OPTIONAL { ?post sioc:links_to ?doc . }
        }
    """)

    reply_rows = run_query(store, """
        SELECT (COUNT(*) AS ?replies)
        WHERE { ?post sioc:reply_of ?parent . }
    """)

    if not rows or rows[0]["posts"] is None:
        console.print("[dim]No data found.[/dim]")
        return

    r = rows[0]
    replies = reply_rows[0]["replies"] if reply_rows else "0"

    body = (
        f"[bold]{r['posts']}[/bold] posts  ·  "
        f"[bold]{r['users']}[/bold] contributors  ·  "
        f"[bold]{r['forums']}[/bold] forums  ·  "
        f"[bold]{r['links']}[/bold] shared links  ·  "
        f"[bold]{replies}[/bold] replies\n"
        f"[dim]{format_date(r['earliest'])}  →  {format_date(r['latest'])}[/dim]"
    )
    console.print(Panel(body, title="Community Snapshot", border_style="blue"))


def forum_hierarchy(console: Console, store: Store) -> None:
    """Section 2: Forum hierarchy with post counts."""
    rows = run_query(store, """
        SELECT ?forum ?fname (COUNT(DISTINCT ?post) AS ?posts)
        WHERE {
            ?forum a sioc:Forum .
            OPTIONAL { ?forum foaf:name ?fname . }
            OPTIONAL { ?post sioc:has_container ?forum . }
        }
        GROUP BY ?forum ?fname
        ORDER BY DESC(?posts)
        LIMIT 20
    """)

    if not rows:
        return

    table = Table(title="Forum Hierarchy")
    table.add_column("#", style="dim", width=3)
    table.add_column("Forum", ratio=1)
    table.add_column("Posts", justify="right", style="bold")

    for i, row in enumerate(rows, 1):
        label = row["fname"] if row["fname"] else short_uri(row["forum"])
        table.add_row(str(i), label, row["posts"])

    console.print(table)


def most_active_contributors(console: Console, store: Store) -> None:
    """Section 3: users ranked by post count."""
    rows = run_query(store, """
        SELECT ?user ?name (COUNT(?post) AS ?count)
        WHERE {
            ?post a sioc:Post .
            ?post sioc:has_creator ?user .
            OPTIONAL { ?user sioc:name ?name . }
        }
        GROUP BY ?user ?name
        ORDER BY DESC(?count)
        LIMIT 15
    """)

    table = Table(title="Most Active Contributors")
    table.add_column("#", style="dim", width=3)
    table.add_column("User", style="cyan")
    table.add_column("Posts", justify="right", style="bold")

    for i, row in enumerate(rows, 1):
        table.add_row(str(i), display_name(row["name"], row["user"]), row["count"])

    console.print(table)


def recent_conversations(console: Console, store: Store) -> None:
    """Section 4: 10 newest posts with date, author, snippet."""
    rows = run_query(store, """
        SELECT ?post ?date ?user ?name ?content ?forum ?fname
        WHERE {
            ?post a sioc:Post .
            ?post dcterms:created ?date .
            ?post sioc:has_creator ?user .
            ?post sioc:content ?content .
            OPTIONAL { ?user sioc:name ?name . }
            OPTIONAL { ?post sioc:has_container ?forum .
                       ?forum foaf:name ?fname . }
        }
        ORDER BY DESC(?date)
        LIMIT 10
    """)

    table = Table(title="Recent Conversations")
    table.add_column("Date", style="dim", width=18)
    table.add_column("Author", style="cyan", width=12)
    table.add_column("Forum", style="green", width=16)
    table.add_column("Message", ratio=1)

    for row in rows:
        table.add_row(
            format_date(row["date"]),
            display_name(row["name"], row["user"]),
            truncate(row["fname"], 16) if row["fname"] else "",
            truncate(row["content"], 60),
        )

    console.print(table)


def reply_network(console: Console, store: Store) -> None:
    """Section 5: who replies to whom (top pairs)."""
    rows = run_query(store, """
        SELECT ?replier ?rname ?original ?oname (COUNT(*) AS ?count)
        WHERE {
            ?reply a sioc:Post .
            ?reply sioc:has_creator ?replier .
            ?reply sioc:reply_of ?parent .
            ?parent sioc:has_creator ?original .
            OPTIONAL { ?replier sioc:name ?rname . }
            OPTIONAL { ?original sioc:name ?oname . }
        }
        GROUP BY ?replier ?rname ?original ?oname
        ORDER BY DESC(?count)
        LIMIT 10
    """)

    table = Table(title="Reply Network (who replies to whom)")
    table.add_column("From", style="cyan")
    table.add_column("→", style="dim", width=2)
    table.add_column("To", style="green")
    table.add_column("Replies", justify="right", style="bold")

    for row in rows:
        table.add_row(
            display_name(row["rname"], row["replier"]),
            "→",
            display_name(row["oname"], row["original"]),
            row["count"],
        )

    console.print(table)


def busiest_threads(console: Console, store: Store) -> None:
    """Section 6: posts with most replies."""
    rows = run_query(store, """
        SELECT ?parent ?content ?author ?aname (COUNT(?reply) AS ?replies)
        WHERE {
            ?reply sioc:reply_of ?parent .
            ?parent a sioc:Post .
            ?parent sioc:content ?content .
            ?parent sioc:has_creator ?author .
            OPTIONAL { ?author sioc:name ?aname . }
        }
        GROUP BY ?parent ?content ?author ?aname
        ORDER BY DESC(?replies)
        LIMIT 10
    """)

    table = Table(title="Busiest Threads")
    table.add_column("Post", style="dim", width=6)
    table.add_column("Author", style="cyan", width=12)
    table.add_column("Snippet", ratio=1)
    table.add_column("Replies", justify="right", style="bold")

    for row in rows:
        table.add_row(
            short_uri(row["parent"]),
            display_name(row["aname"], row["author"]),
            truncate(row["content"], 60),
            row["replies"],
        )

    console.print(table)


def most_shared_links(console: Console, store: Store) -> None:
    """Section 7: linked documents ranked by share count."""
    rows = run_query(store, """
        SELECT ?doc ?title (COUNT(?post) AS ?shares)
        WHERE {
            ?post a sioc:Post .
            ?post sioc:links_to ?doc .
            OPTIONAL { ?doc dc:title ?title . }
        }
        GROUP BY ?doc ?title
        ORDER BY DESC(?shares)
        LIMIT 15
    """)

    table = Table(title="Most Shared Links")
    table.add_column("#", style="dim", width=3)
    table.add_column("Document", ratio=1)
    table.add_column("Shares", justify="right", style="bold")

    for i, row in enumerate(rows, 1):
        label = row["title"] if row["title"] else truncate(row["doc"], 80)
        table.add_row(str(i), label, row["shares"])

    console.print(table)


def topic_distribution(console: Console, store: Store) -> None:
    """Section 8: topics (skos:Concept) by post count."""
    rows = run_query(store, """
        SELECT ?concept ?label (COUNT(?post) AS ?count)
        WHERE {
            ?post sioc:topic ?concept .
            ?concept skos:prefLabel ?label .
        }
        GROUP BY ?concept ?label
        ORDER BY DESC(?count)
        LIMIT 15
    """)

    if not rows:
        return

    table = Table(title="Topics (Hashtags)")
    table.add_column("#", style="dim", width=3)
    table.add_column("Topic", style="cyan")
    table.add_column("Posts", justify="right", style="bold")

    for i, row in enumerate(rows, 1):
        table.add_row(str(i), f"#{row['label']}" if row["label"] else short_uri(row["concept"]), row["count"])

    console.print(table)


def media_breakdown(console: Console, store: Store) -> None:
    """Section 9: attachments by media type."""
    rows = run_query(store, """
        SELECT ?mtype (COUNT(?att) AS ?count)
        WHERE {
            ?att a foaf:Document .
            ?att tg:media_type ?mtype .
        }
        GROUP BY ?mtype
        ORDER BY DESC(?count)
    """)

    if not rows:
        return

    table = Table(title="Media Breakdown (Attachments)")
    table.add_column("Type", style="cyan")
    table.add_column("Count", justify="right", style="bold")

    for row in rows:
        table.add_row(row["mtype"] or "unknown", row["count"])

    console.print(table)


def most_edited_posts(console: Console, store: Store) -> None:
    """Section 10: recently edited posts."""
    rows = run_query(store, """
        SELECT ?post ?content ?author ?aname ?modified
        WHERE {
            ?post a sioc:Post .
            ?post dcterms:modified ?modified .
            ?post sioc:content ?content .
            ?post sioc:has_creator ?author .
            OPTIONAL { ?author sioc:name ?aname . }
        }
        ORDER BY DESC(?modified)
        LIMIT 10
    """)

    if not rows:
        return

    table = Table(title="Recently Edited Posts")
    table.add_column("Edited", style="dim", width=18)
    table.add_column("Author", style="cyan", width=12)
    table.add_column("Snippet", ratio=1)

    for row in rows:
        table.add_row(
            format_date(row["modified"]),
            display_name(row["aname"], row["author"]),
            truncate(row["content"], 60),
        )

    console.print(table)


def forwarded_content(console: Console, store: Store) -> None:
    """Section 11: posts with sibling (forwarded from other channels)."""
    rows = run_query(store, """
        SELECT ?post ?content ?author ?aname ?sibling
        WHERE {
            ?post a sioc:Post .
            ?post sioc:sibling ?sibling .
            ?post sioc:content ?content .
            ?post sioc:has_creator ?author .
            OPTIONAL { ?author sioc:name ?aname . }
        }
        LIMIT 10
    """)

    if not rows:
        return

    table = Table(title="Forwarded Content (Siblings)")
    table.add_column("Author", style="cyan", width=12)
    table.add_column("Source", style="green", width=20)
    table.add_column("Snippet", ratio=1)

    for row in rows:
        table.add_row(
            display_name(row["aname"], row["author"]),
            short_uri(row["sibling"]),
            truncate(row["content"], 60),
        )

    console.print(table)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

SECTIONS = [
    community_overview,
    forum_hierarchy,
    most_active_contributors,
    recent_conversations,
    reply_network,
    busiest_threads,
    most_shared_links,
    topic_distribution,
    media_breakdown,
    most_edited_posts,
    forwarded_content,
]


def main() -> None:
    console = Console()

    if not TURTLE_FILE.exists():
        console.print(
            f"[red]Turtle file not found at {TURTLE_FILE}[/red]\n"
            "Run [bold]just build[/bold] first to generate the RDF."
        )
        return

    store = Store()
    with open(TURTLE_FILE, "rb") as f:
        store.load(f, format=RdfFormat.TURTLE)

    console.rule("[bold blue]Community Insights Dashboard[/bold blue]")
    console.print()

    for section in SECTIONS:
        section(console, store)
        console.print()

    console.rule("[dim]End of report[/dim]")


if __name__ == "__main__":
    main()
