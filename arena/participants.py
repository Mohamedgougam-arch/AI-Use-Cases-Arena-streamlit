from __future__ import annotations

from typing import Any

from arena.auth import (
    ADMIN_EMAIL,
    get_avatar_from_email,
    get_display_name_from_email,
    is_admin_email,
    normalize_email,
)

SCORE_POINTS = {
    "submit": 10,
    "voteReceived": 2,
    "voteCast": 1,
    "comment": 1,
}

SCORE_RULES = [
    ("Submit a use case", SCORE_POINTS["submit"]),
    ("Each vote your idea receives", SCORE_POINTS["voteReceived"]),
    ("Vote on someone else's idea", SCORE_POINTS["voteCast"]),
    ("Leave a comment", SCORE_POINTS["comment"]),
]


def build_participant_scores(use_cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scores: dict[str, dict[str, Any]] = {}

    def ensure(raw_email: str) -> dict[str, Any] | None:
        if not raw_email or "@" not in raw_email:
            return None
        email = normalize_email(raw_email)
        if email == ADMIN_EMAIL or is_admin_email(email):
            return None
        if email not in scores:
            scores[email] = {
                "email": email,
                "name": get_display_name_from_email(email),
                "avatar": get_avatar_from_email(email),
                "submissions": 0,
                "votesReceived": 0,
                "votesCast": 0,
                "comments": 0,
                "score": 0,
            }
        return scores[email]

    for uc in use_cases:
        submitter = uc.get("submitterEmail") or (
            uc.get("submitterId") if "@" in (uc.get("submitterId") or "") else None
        )
        if submitter:
            p = ensure(submitter)
            if p:
                p["submissions"] += 1
                p["votesReceived"] += uc["votes"]

        voters = uc.get("voterEmails") or [
            v for v in uc.get("voterIds", []) if "@" in v
        ]
        for voter in voters:
            v = ensure(voter)
            if v:
                v["votesCast"] += 1

        for c in uc.get("comments", []):
            author = c.get("userEmail") or (
                c.get("userId") if "@" in c.get("userId", "") else None
            )
            if author:
                a = ensure(author)
                if a:
                    a["comments"] += 1

    for p in scores.values():
        p["score"] = (
            p["submissions"] * SCORE_POINTS["submit"]
            + p["votesReceived"] * SCORE_POINTS["voteReceived"]
            + p["votesCast"] * SCORE_POINTS["voteCast"]
            + p["comments"] * SCORE_POINTS["comment"]
        )

    return sorted(scores.values(), key=lambda x: x["score"], reverse=True)


def get_participant_score(
    use_cases: list[dict[str, Any]], email: str | None
) -> dict[str, Any] | None:
    if not email or is_admin_email(email):
        return None
    normalized = normalize_email(email)
    for p in build_participant_scores(use_cases):
        if p["email"] == normalized:
            return p
    return {
        "email": normalized,
        "name": get_display_name_from_email(normalized),
        "avatar": get_avatar_from_email(normalized),
        "submissions": 0,
        "votesReceived": 0,
        "votesCast": 0,
        "comments": 0,
        "score": 0,
    }


def is_participant_score_leader(
    email: str | None, scores: list[dict[str, Any]]
) -> bool:
    if not email or not scores:
        return False
    top = scores[0]["score"]
    if top <= 0:
        return False
    normalized = normalize_email(email)
    entry = next((p for p in scores if p["email"] == normalized), None)
    return entry is not None and entry["score"] == top
