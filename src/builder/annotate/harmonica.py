"""Harmonica REST API client for session management."""

from typing import Any

import httpx

from builder.config import HARMONICA_API_KEY, HARMONICA_API_URL

_TIMEOUT = 30.0


def _client() -> httpx.Client:
    if not HARMONICA_API_KEY:
        raise RuntimeError(
            "HARMONICA_API_KEY not set. "
            "Get one from harmonica.chat → Profile → API Keys, "
            "then add it to .env"
        )
    return httpx.Client(
        base_url=HARMONICA_API_URL,
        headers={"Authorization": f"Bearer {HARMONICA_API_KEY}"},
        timeout=_TIMEOUT,
    )


def create_session(
    topic: str,
    goal: str,
    context: str,
    questions: list[str] | None = None,
) -> dict[str, Any]:
    """Create a Harmonica deliberation session and return its metadata."""
    payload: dict[str, Any] = {
        "topic": topic,
        "goal": goal,
        "context": context,
    }
    if questions:
        payload["questions"] = questions
    with _client() as client:
        resp = client.post("/api/v1/sessions", json=payload)
        resp.raise_for_status()
        return resp.json()


def get_session(session_id: str) -> dict[str, Any]:
    with _client() as client:
        resp = client.get(f"/api/v1/sessions/{session_id}")
        resp.raise_for_status()
        return resp.json()


def get_responses(session_id: str) -> dict[str, Any]:
    with _client() as client:
        resp = client.get(f"/api/v1/sessions/{session_id}/responses")
        resp.raise_for_status()
        return resp.json()


def get_summary(session_id: str) -> dict[str, Any]:
    with _client() as client:
        resp = client.get(f"/api/v1/sessions/{session_id}/summary")
        resp.raise_for_status()
        return resp.json()


def list_sessions(status: str | None = None) -> list[dict[str, Any]]:
    with _client() as client:
        params: dict[str, str] = {}
        if status:
            params["status"] = status
        resp = client.get("/api/v1/sessions", params=params)
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else data.get("sessions", [])
