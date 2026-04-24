"""Fireflies.ai GraphQL API client (transcripts)."""

from __future__ import annotations

from typing import Any

import httpx

from app.config import Settings

_TRANSCRIPT_QUERY = """
query Transcript($transcriptId: String!) {
  transcript(id: $transcriptId) {
    id
    title
    sentences {
      speaker_name
      text
    }
    summary {
      overview
      short_summary
      gist
      short_overview
    }
  }
}
"""


class FirefliesAPIError(RuntimeError):
    pass


class FirefliesClient:
    def __init__(self, settings: Settings) -> None:
        self._url = settings.fireflies_graphql_url.rstrip("/")
        self._api_key = settings.fireflies_api_key
        self._timeout = settings.fireflies_timeout_seconds

    def _require_key(self) -> None:
        if not self._api_key or not str(self._api_key).strip():
            raise FirefliesAPIError("FIREFLIES_API_KEY is not configured")

    async def graphql(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        self._require_key()
        payload = {"query": query, "variables": variables}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.post(self._url, json=payload, headers=headers)
            r.raise_for_status()
            body = r.json()
        if isinstance(body, dict) and body.get("errors"):
            parts: list[str] = []
            for err in body["errors"]:
                if isinstance(err, dict):
                    parts.append(str(err.get("message", err)))
                else:
                    parts.append(str(err))
            raise FirefliesAPIError("; ".join(parts) if parts else "GraphQL error")
        if not isinstance(body, dict):
            raise FirefliesAPIError("Unexpected response shape")
        data = body.get("data")
        if not isinstance(data, dict):
            raise FirefliesAPIError("Missing data in GraphQL response")
        return data

    async def fetch_transcript(self, transcript_id: str) -> dict[str, Any]:
        """
        Return a normalized dict: title, transcript, summary, raw (Fireflies transcript object).
        """
        data = await self.graphql(_TRANSCRIPT_QUERY, {"transcriptId": transcript_id})
        raw = data.get("transcript")
        if raw is None:
            raise FirefliesAPIError("transcript not found or not accessible")
        if not isinstance(raw, dict):
            raise FirefliesAPIError("Invalid transcript payload")

        lines: list[str] = []
        sentences = raw.get("sentences")
        if isinstance(sentences, list):
            for s in sentences:
                if not isinstance(s, dict):
                    continue
                text = s.get("text")
                if not isinstance(text, str) or not text.strip():
                    continue
                speaker = s.get("speaker_name")
                if isinstance(speaker, str) and speaker.strip():
                    lines.append(f"{speaker.strip()}: {text.strip()}")
                else:
                    lines.append(text.strip())

        summary_block = raw.get("summary")
        summary_text = _pick_summary_text(summary_block)

        return {
            "title": raw.get("title") if isinstance(raw.get("title"), str) else None,
            "transcript": "\n".join(lines),
            "summary": summary_text,
            "raw": raw,
        }


def _pick_summary_text(summary: Any) -> str | None:
    if not isinstance(summary, dict):
        return None
    for key in ("overview", "short_summary", "gist", "short_overview"):
        v = summary.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None
