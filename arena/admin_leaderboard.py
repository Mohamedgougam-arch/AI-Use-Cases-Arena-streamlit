from __future__ import annotations

from typing import Any

from arena.auth import get_avatar_from_email, get_display_name_from_email, is_admin_email
from arena.participants import build_participant_scores


def build_admin_contributor_rows(
    use_cases: list[dict[str, Any]], known_users: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    scores = build_participant_scores(use_cases)
    by_email = {s["email"]: s for s in scores}

    emails: set[str] = set()
    for u in known_users:
        if not is_admin_email(u["email"]):
            emails.add(u["email"])
    for s in scores:
        emails.add(s["email"])

    last_seen = {u["email"]: u.get("lastSeenAt") for u in known_users}

    rows = []
    for email in emails:
        stats = by_email.get(email)
        rows.append(
            {
                "email": email,
                "name": stats["name"] if stats else get_display_name_from_email(email),
                "avatar": stats["avatar"] if stats else get_avatar_from_email(email),
                "submissions": stats["submissions"] if stats else 0,
                "votesCast": stats["votesCast"] if stats else 0,
                "votesReceived": stats["votesReceived"] if stats else 0,
                "comments": stats["comments"] if stats else 0,
                "score": stats["score"] if stats else 0,
                "lastSignedInAt": last_seen.get(email),
            }
        )

    rows.sort(
        key=lambda r: (-r["score"], -r["submissions"], r["email"]),
    )
    return [{**row, "rank": i + 1} for i, row in enumerate(rows)]


def get_admin_totals(use_cases: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "totalUseCases": len(use_cases),
        "totalVotes": sum(uc["votes"] for uc in use_cases),
    }
