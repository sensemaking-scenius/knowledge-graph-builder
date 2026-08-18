"""CLI for gamified entity annotation via Harmonica sessions."""

import argparse
import json
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from builder.config import (
    CONFIDENCE_THRESHOLD,
    GRAPH_FILE,
    MIN_PARTICIPANTS,
    SESSIONS_FILE,
)

console = Console()


def cmd_select(args: argparse.Namespace) -> None:
    """Preview the next batch of messages to annotate."""
    from builder.annotate.select import format_messages_for_session, select_batch

    posts = select_batch(batch_size=args.batch_size, forum_id=args.forum)
    if not posts:
        console.print("[yellow]No unannotated messages available.[/]")
        return

    console.print(
        Panel(
            f"[bold]{len(posts)} messages[/bold] selected for annotation",
            title="Batch Preview",
            border_style="cyan",
        )
    )
    console.print(format_messages_for_session(posts))


def cmd_create(args: argparse.Namespace) -> None:
    """Create a new Harmonica annotation session."""
    from builder.annotate.session import THEME_PROMPTS, create_annotation_session

    theme = args.theme
    if theme not in THEME_PROMPTS:
        console.print(f"[red]Unknown theme '{theme}'[/]")
        console.print(f"Available: {', '.join(THEME_PROMPTS)}")
        sys.exit(1)

    console.print(f"Creating [bold]{THEME_PROMPTS[theme]['label']}[/] session...")

    try:
        record = create_annotation_session(
            theme=theme,
            batch_size=args.batch_size,
            forum_id=args.forum,
        )
    except RuntimeError as e:
        console.print(f"[red]{e}[/]")
        sys.exit(1)

    console.print(
        Panel(
            f"[bold green]Session created![/]\n\n"
            f"Theme: {THEME_PROMPTS[theme]['label']}\n"
            f"Messages: {len(record['messages_annotated'])}\n"
            f"Session ID: {record['harmonica_session_id']}\n"
            f"Join URL: [link]{record['join_url']}[/link]\n\n"
            f"[dim]Share this link with your community![/]",
            title="New Annotation Round",
            border_style="green",
        )
    )


def cmd_check(args: argparse.Namespace) -> None:
    """Check status of an annotation session."""
    from builder.annotate.session import check_session

    session_id = args.session_id
    if not session_id:
        sessions = _load_sessions()
        active = [s for s in sessions if s.get("status") == "active"]
        if not active:
            console.print("[yellow]No active sessions.[/]")
            return
        session_id = active[-1]["harmonica_session_id"]
        console.print(f"Checking latest active session: {session_id}")

    result = check_session(session_id)
    responses = result["responses"]
    summary = result["summary"]

    resp_list = (
        responses if isinstance(responses, list)
        else responses.get("responses", [])
    )

    console.print(
        Panel(
            f"Participants: [bold]{len(resp_list)}[/] "
            f"(minimum needed: {MIN_PARTICIPANTS})\n"
            f"Summary: {'[green]Available[/]' if summary else '[yellow]Pending[/]'}",
            title=f"Session {session_id}",
            border_style="blue",
        )
    )

    if summary:
        summary_text = (
            summary.get("summary", summary.get("text", ""))
            if isinstance(summary, dict)
            else str(summary)
        )
        if summary_text:
            console.print(Panel(summary_text, title="Synthesis", border_style="cyan"))


def cmd_import(args: argparse.Namespace) -> None:
    """Import synthesis results from a session into the knowledge graph."""
    from builder.annotate.ingest import ingest_entities
    from builder.annotate.parse import filter_by_confidence, parse_summary_entities
    from builder.annotate.session import check_session

    session_id = args.session_id
    if not session_id:
        sessions = _load_sessions()
        synthesized = [s for s in sessions if s.get("status") == "synthesized"]
        if not synthesized:
            console.print("[yellow]No synthesized sessions ready for import.[/]")
            return
        session_id = synthesized[-1]["harmonica_session_id"]

    sessions = _load_sessions()
    session_record = None
    for s in sessions:
        if s["harmonica_session_id"] == session_id:
            session_record = s
            break

    if not session_record:
        console.print(f"[red]Session {session_id} not found locally.[/]")
        sys.exit(1)

    console.print(f"Fetching results for session {session_id}...")
    result = check_session(session_id)
    responses = result["responses"]
    summary = result["summary"]

    if not summary:
        console.print("[yellow]No synthesis available yet. Try again later.[/]")
        return

    resp_list = (
        responses if isinstance(responses, list)
        else responses.get("responses", [])
    )
    participant_count = len(resp_list)

    entities = parse_summary_entities(summary, responses, participant_count)
    if not entities:
        console.print("[yellow]No entities found in synthesis.[/]")
        return

    above, below = filter_by_confidence(entities, CONFIDENCE_THRESHOLD)

    table = Table(title="Discovered Entities")
    table.add_column("Entity", style="bold")
    table.add_column("Type", style="cyan")
    table.add_column("Confidence", justify="right")
    table.add_column("Status")

    for e in above:
        table.add_row(
            e["name"],
            e["type"],
            f"{e['confidence']:.0%}",
            "[green]importing[/]",
        )
    for e in below:
        table.add_row(
            e["name"],
            e["type"],
            f"{e['confidence']:.0%}",
            "[dim]below threshold[/]",
        )
    console.print(table)

    if not above:
        console.print("[yellow]No entities above confidence threshold.[/]")
        return

    counts = ingest_entities(
        harmonica_session_id=session_id,
        entities=above,
        post_ids=session_record["messages_annotated"],
        participant_count=participant_count,
        theme=session_record["theme"],
        created=session_record["created"],
    )

    console.print(
        Panel(
            f"[bold green]Import complete![/]\n\n"
            f"New concepts: {counts['new_concepts']}\n"
            f"Annotations: {counts['new_annotations']}\n"
            f"Posts linked: {counts['posts_linked']}\n\n"
            f"[dim]Run `just serialize` then `just load` to update the triplestore.[/]",
            title="Import Results",
            border_style="green",
        )
    )


def cmd_status(_args: argparse.Namespace) -> None:
    """Show annotation coverage and session history."""
    sessions = _load_sessions()

    if not sessions:
        console.print("[dim]No annotation sessions yet.[/]")
        console.print(
            "Start one with: [bold]just annotate-create[/]"
        )
        return

    table = Table(title="Annotation Sessions")
    table.add_column("Theme", style="cyan")
    table.add_column("Messages", justify="right")
    table.add_column("Participants", justify="right")
    table.add_column("Status")
    table.add_column("Created")

    for s in sessions:
        status_style = {
            "active": "[yellow]active[/]",
            "synthesized": "[blue]synthesized[/]",
            "imported": "[green]imported[/]",
        }.get(s.get("status", ""), s.get("status", ""))

        table.add_row(
            s.get("theme", "?"),
            str(len(s.get("messages_annotated", []))),
            str(s.get("participant_count", 0)),
            status_style,
            s.get("created", "")[:10],
        )

    console.print(table)

    total_annotated = set()
    for s in sessions:
        total_annotated.update(s.get("messages_annotated", []))

    if GRAPH_FILE.exists():
        with open(GRAPH_FILE, "r", encoding="utf-8") as f:
            graph = json.load(f)
        total_posts = len(graph.get("posts", {}))
        total_concepts = len(graph.get("concepts", {}))
        pct = (len(total_annotated) / total_posts * 100) if total_posts else 0

        console.print(
            f"\nCoverage: [bold]{len(total_annotated)}[/]/{total_posts} "
            f"messages annotated ({pct:.0f}%)"
        )
        console.print(f"Concepts in graph: [bold]{total_concepts}[/]")


def _load_sessions() -> list[dict]:
    if not SESSIONS_FILE.exists():
        return []
    with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gamified entity annotation via Harmonica sessions",
        prog="python -m builder.annotate",
    )
    sub = parser.add_subparsers(dest="command")

    p_select = sub.add_parser("select", help="Preview next message batch")
    p_select.add_argument("--batch-size", type=int, default=8)
    p_select.add_argument("--forum", help="Filter to a specific forum ID")

    p_create = sub.add_parser("create", help="Create annotation session")
    p_create.add_argument(
        "--theme",
        default="free_hunt",
        choices=[
            "free_hunt", "whos_who", "tool_chest",
            "project_radar", "idea_map", "link_dive",
        ],
    )
    p_create.add_argument("--batch-size", type=int, default=8)
    p_create.add_argument("--forum", help="Filter to a specific forum ID")

    p_check = sub.add_parser("check", help="Check session status")
    p_check.add_argument("session_id", nargs="?", help="Harmonica session ID")

    p_import = sub.add_parser("import", help="Import synthesis into graph")
    p_import.add_argument("session_id", nargs="?", help="Harmonica session ID")

    sub.add_parser("status", help="Show annotation coverage")

    args = parser.parse_args()

    commands = {
        "select": cmd_select,
        "create": cmd_create,
        "check": cmd_check,
        "import": cmd_import,
        "status": cmd_status,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
