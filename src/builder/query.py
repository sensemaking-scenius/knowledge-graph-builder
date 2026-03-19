"""Demo stage: SPARQL queries → rich CLI community insights dashboard."""

from datetime import datetime, timezone
from typing import Any, Iterable, cast

from pyoxigraph import RdfFormat, Store
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from builder.config import TURTLE_FILE

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SIOC = "http://rdfs.org/sioc/ns#"
DCTERMS = "http://purl.org/dc/terms/"
FOAF = "http://xmlns.com/foaf/0.1/"
TG = "https://example.org/telegram/"
XSD = "http://www.w3.org/2001/XMLSchema#"


def run_query(store: Store, sparql: str) -> list[dict[str, Any]]:
    """Execute a SPARQL SELECT and return rows as dicts of native values."""
    result = cast(Any, store.query(sparql))
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
        (f"{TG}channel/", "channel/"),
        (f"{TG}channel/2141367711/message/", "#"),
        (f"{TG}mention/", "@"),
    ]:
        if uri.startswith(prefix):
            return f"{label}{uri[len(prefix):]}"
    # For external URLs, keep as-is but truncate
    return truncate(uri, 60)


def display_name(name: str | None, user_uri: str | None) -> str:
    """Show foaf:name if available, otherwise fall back to short_uri."""
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
    # Collapse newlines
    text = " ".join(text.split())
    if len(text) <= length:
        return text
    return text[: length - 1] + "…"


def mention_handle(raw: str | None) -> str:
    """Extract @handle from mention literal like 'tg:mention/codybftw'."""
    if not raw:
        return ""
    prefix = "tg:mention/"
    if raw.startswith(prefix):
        return f"@{raw[len(prefix):]}"
    return raw


# ---------------------------------------------------------------------------
# Query sections
# ---------------------------------------------------------------------------


def community_overview(console: Console, store: Store) -> None:
    """Section 1: aggregate counts and date range."""
    rows = run_query(store, f"""
        SELECT
            (COUNT(DISTINCT ?post) AS ?posts)
            (COUNT(DISTINCT ?user) AS ?users)
            (COUNT(DISTINCT ?link) AS ?links)
            (MIN(?date) AS ?earliest)
            (MAX(?date) AS ?latest)
        WHERE {{
            ?post a <{SIOC}Post> .
            ?post <{DCTERMS}created> ?date .
            ?post <{SIOC}has_creator> ?user .
            OPTIONAL {{ ?post <{SIOC}links_to> ?link . }}
        }}
    """)

    reply_rows = run_query(store, f"""
        SELECT (COUNT(*) AS ?replies)
        WHERE {{ ?post <{SIOC}reply_of> ?parent . }}
    """)

    if not rows or rows[0]["posts"] is None:
        console.print("[dim]No data found.[/dim]")
        return

    r = rows[0]
    replies = reply_rows[0]["replies"] if reply_rows else "0"

    body = (
        f"[bold]{r['posts']}[/bold] posts  ·  "
        f"[bold]{r['users']}[/bold] contributors  ·  "
        f"[bold]{r['links']}[/bold] shared links  ·  "
        f"[bold]{replies}[/bold] replies\n"
        f"[dim]{format_date(r['earliest'])}  →  {format_date(r['latest'])}[/dim]"
    )
    console.print(Panel(body, title="Community Snapshot", border_style="blue"))


def most_active_contributors(console: Console, store: Store) -> None:
    """Section 2: users ranked by post count."""
    rows = run_query(store, f"""
        SELECT ?user ?name (COUNT(?post) AS ?count)
        WHERE {{
            ?post a <{SIOC}Post> .
            ?post <{SIOC}has_creator> ?user .
            OPTIONAL {{ ?user <{FOAF}name> ?name . }}
        }}
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
    """Section 3: 10 newest posts with date, author, snippet."""
    rows = run_query(store, f"""
        SELECT ?post ?date ?user ?name ?content
        WHERE {{
            ?post a <{SIOC}Post> .
            ?post <{DCTERMS}created> ?date .
            ?post <{SIOC}has_creator> ?user .
            ?post <{SIOC}content> ?content .
            OPTIONAL {{ ?user <{FOAF}name> ?name . }}
        }}
        ORDER BY DESC(?date)
        LIMIT 10
    """)

    table = Table(title="Recent Conversations")
    table.add_column("Date", style="dim", width=18)
    table.add_column("Author", style="cyan", width=12)
    table.add_column("Message", ratio=1)

    for row in rows:
        table.add_row(
            format_date(row["date"]),
            display_name(row["name"], row["user"]),
            truncate(row["content"], 80),
        )

    console.print(table)


def reply_network(console: Console, store: Store) -> None:
    """Section 4: who replies to whom (top pairs)."""
    rows = run_query(store, f"""
        SELECT ?replier ?replier_name ?original_author ?oa_name (COUNT(*) AS ?count)
        WHERE {{
            ?reply a <{SIOC}Post> .
            ?reply <{SIOC}has_creator> ?replier .
            ?reply <{SIOC}reply_of> ?parent .
            ?parent <{SIOC}has_creator> ?original_author .
            OPTIONAL {{ ?replier <{FOAF}name> ?replier_name . }}
            OPTIONAL {{ ?original_author <{FOAF}name> ?oa_name . }}
        }}
        GROUP BY ?replier ?replier_name ?original_author ?oa_name
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
            display_name(row["replier_name"], row["replier"]),
            "→",
            display_name(row["oa_name"], row["original_author"]),
            row["count"],
        )

    console.print(table)


def busiest_threads(console: Console, store: Store) -> None:
    """Section 5: posts with most replies."""
    rows = run_query(store, f"""
        SELECT ?parent ?content ?author ?author_name (COUNT(?reply) AS ?replies)
        WHERE {{
            ?reply <{SIOC}reply_of> ?parent .
            ?parent a <{SIOC}Post> .
            ?parent <{SIOC}content> ?content .
            ?parent <{SIOC}has_creator> ?author .
            OPTIONAL {{ ?author <{FOAF}name> ?author_name . }}
        }}
        GROUP BY ?parent ?content ?author ?author_name
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
            display_name(row["author_name"], row["author"]),
            truncate(row["content"], 60),
            row["replies"],
        )

    console.print(table)


def most_shared_links(console: Console, store: Store) -> None:
    """Section 6: URLs ranked by share count."""
    rows = run_query(store, f"""
        SELECT ?link (COUNT(?post) AS ?shares)
        WHERE {{
            ?post a <{SIOC}Post> .
            ?post <{SIOC}links_to> ?link .
        }}
        GROUP BY ?link
        ORDER BY DESC(?shares)
        LIMIT 15
    """)

    table = Table(title="Most Shared Links")
    table.add_column("#", style="dim", width=3)
    table.add_column("URL", ratio=1)
    table.add_column("Shares", justify="right", style="bold")

    for i, row in enumerate(rows, 1):
        table.add_row(str(i), truncate(row["link"], 80), row["shares"])

    console.print(table)


def most_mentioned(console: Console, store: Store) -> None:
    """Section 7: @handles ranked by mention count."""
    rows = run_query(store, f"""
        SELECT ?handle (COUNT(?post) AS ?mentions)
        WHERE {{
            ?post a <{SIOC}Post> .
            ?post <{TG}mentions> ?handle .
        }}
        GROUP BY ?handle
        ORDER BY DESC(?mentions)
        LIMIT 15
    """)

    table = Table(title="Most Mentioned People")
    table.add_column("#", style="dim", width=3)
    table.add_column("Handle", style="cyan")
    table.add_column("Mentions", justify="right", style="bold")

    for i, row in enumerate(rows, 1):
        table.add_row(str(i), mention_handle(row["handle"]), row["mentions"])

    console.print(table)


def most_reacted_posts(console: Console, store: Store) -> None:
    """Section 8: posts with the most reactions."""
    rows = run_query(store, f"""
        SELECT ?post ?content ?author ?author_name ?count
        WHERE {{
            ?post a <{SIOC}Post> .
            ?post <{TG}reaction_count> ?count .
            ?post <{SIOC}content> ?content .
            ?post <{SIOC}has_creator> ?author .
            OPTIONAL {{ ?author <{FOAF}name> ?author_name . }}
        }}
        ORDER BY DESC(?count)
        LIMIT 10
    """)

    if not rows:
        return

    table = Table(title="Most Reacted Posts")
    table.add_column("Post", style="dim", width=6)
    table.add_column("Author", style="cyan", width=12)
    table.add_column("Snippet", ratio=1)
    table.add_column("Reactions", justify="right", style="bold")

    for row in rows:
        table.add_row(
            short_uri(row["post"]),
            display_name(row["author_name"], row["author"]),
            truncate(row["content"], 60),
            row["count"],
        )

    console.print(table)


def forum_threads(console: Console, store: Store) -> None:
    """Section 9: forum threads by post count."""
    rows = run_query(store, f"""
        SELECT ?thread ?name (COUNT(?post) AS ?posts)
        WHERE {{
            ?post a <{SIOC}Post> .
            ?post <{TG}has_thread> ?thread .
            OPTIONAL {{ ?thread <{FOAF}name> ?name . }}
        }}
        GROUP BY ?thread ?name
        ORDER BY DESC(?posts)
        LIMIT 10
    """)

    if not rows:
        return

    table = Table(title="Forum Threads (by post count)")
    table.add_column("#", style="dim", width=3)
    table.add_column("Thread", ratio=1)
    table.add_column("Posts", justify="right", style="bold")

    for i, row in enumerate(rows, 1):
        label = row["name"] if row["name"] else short_uri(row["thread"])
        table.add_row(str(i), label, row["posts"])

    console.print(table)


def media_breakdown(console: Console, store: Store) -> None:
    """Section 10: posts by media type."""
    rows = run_query(store, f"""
        SELECT ?mtype (COUNT(?post) AS ?count)
        WHERE {{
            ?post a <{SIOC}Post> .
            ?post <{TG}media_type> ?mtype .
        }}
        GROUP BY ?mtype
        ORDER BY DESC(?count)
    """)

    if not rows:
        return

    table = Table(title="Media Breakdown")
    table.add_column("Type", style="cyan")
    table.add_column("Posts", justify="right", style="bold")

    for row in rows:
        table.add_row(row["mtype"] or "unknown", row["count"])

    console.print(table)


def most_edited_posts(console: Console, store: Store) -> None:
    """Section 11: recently edited posts."""
    rows = run_query(store, f"""
        SELECT ?post ?content ?author ?author_name ?modified
        WHERE {{
            ?post a <{SIOC}Post> .
            ?post <{DCTERMS}modified> ?modified .
            ?post <{SIOC}content> ?content .
            ?post <{SIOC}has_creator> ?author .
            OPTIONAL {{ ?author <{FOAF}name> ?author_name . }}
        }}
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
            display_name(row["author_name"], row["author"]),
            truncate(row["content"], 60),
        )

    console.print(table)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

SECTIONS = [
    community_overview,
    most_active_contributors,
    recent_conversations,
    reply_network,
    busiest_threads,
    most_shared_links,
    most_mentioned,
    most_reacted_posts,
    forum_threads,
    media_breakdown,
    most_edited_posts,
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
