from __future__ import annotations

from typing import Any

from arena.constants import is_known_department, normalize_department
from arena.scoring import get_effort_score, get_impact_score, is_quick_win, is_strategic_bet


def get_total_votes(use_cases: list[dict[str, Any]]) -> int:
    return sum(uc["votes"] for uc in use_cases)


def get_top_use_case(use_cases: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not use_cases:
        return None
    return max(use_cases, key=lambda uc: uc["votes"])


def get_department_stats(use_cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = {}
    for uc in use_cases:
        department = normalize_department(uc["department"])
        if not is_known_department(department):
            continue
        row = stats.get(
            department,
            {
                "department": department,
                "useCaseCount": 0,
                "totalVotes": 0,
                "innovationScore": 0,
                "engagement": 0,
            },
        )
        row["useCaseCount"] += 1
        row["totalVotes"] += uc["votes"]
        row["innovationScore"] += uc["innovationScore"]
        row["engagement"] += len(uc.get("comments", [])) + uc["votes"]
        stats[department] = row
    return sorted(stats.values(), key=lambda d: d["innovationScore"], reverse=True)


def get_trending_use_cases(
    use_cases: list[dict[str, Any]], limit: int = 5
) -> list[dict[str, Any]]:
    if not use_cases:
        return []
    badges_key = "badges"
    hot = [
        uc
        for uc in use_cases
        if "Trending" in uc.get(badges_key, []) or uc["votes"] >= 5
    ]
    hot.sort(key=lambda uc: uc["innovationScore"], reverse=True)
    if hot:
        return hot[:limit]
    return sorted(use_cases, key=lambda uc: uc["createdAt"], reverse=True)[:limit]


def get_voting_trend_data(use_cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not use_cases:
        return []
    month_map: dict[str, int] = {}
    for uc in use_cases:
        month = uc["createdAt"][:7]
        try:
            from datetime import datetime

            dt = datetime.fromisoformat(uc["createdAt"].replace("Z", "+00:00"))
            month = dt.strftime("%b")
        except ValueError:
            pass
        month_map[month] = month_map.get(month, 0) + uc["votes"]
    return [{"month": m, "votes": v} for m, v in month_map.items()]


def get_quick_wins(use_cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [uc for uc in use_cases if is_quick_win(uc)]


def get_strategic_bets(use_cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [uc for uc in use_cases if is_strategic_bet(uc)]


def get_category_distribution(use_cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for uc in use_cases:
        counts[uc["category"]] = counts.get(uc["category"], 0) + 1
    return [{"name": k, "value": v} for k, v in counts.items()]


def get_theme_counts(use_cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tag_map: dict[str, int] = {}
    for uc in use_cases:
        for tag in uc.get("tags", []):
            tag_map[tag] = tag_map.get(tag, 0) + 1
    return sorted(
        [{"name": k, "count": v} for k, v in tag_map.items()],
        key=lambda x: x["count"],
        reverse=True,
    )[:8]


def get_impact_effort_matrix(use_cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": uc["id"],
            "title": uc["title"],
            "impact": get_impact_score(uc["impact"]),
            "effort": get_effort_score(uc["effort"]),
            "votes": uc["votes"],
            "score": uc["innovationScore"],
        }
        for uc in use_cases
    ]


def generate_executive_summary(use_cases: list[dict[str, Any]]) -> str:
    if not use_cases:
        return """Executive Summary — AI Use Cases Arena

No use cases have been submitted yet. Encourage teams across Invest-NL to share their AI ideas in the arena. Once submissions and votes begin, this summary will highlight portfolio trends, quick wins, and department momentum."""

    total = len(use_cases)
    votes = get_total_votes(use_cases)
    top = get_top_use_case(use_cases)
    quick_wins = len(get_quick_wins(use_cases))
    depts = get_department_stats(use_cases)
    top_dept = depts[0]["department"] if depts else "N/A"

    return f"""Executive Summary — AI Use Cases Arena

Portfolio Overview: {total} AI use cases have been submitted across Invest-NL, generating {votes} total votes and strong cross-department engagement.

Top Priority: "{top['title'] if top else 'N/A'}" leads the arena with {top['votes'] if top else 0} votes and an innovation score of {top['innovationScore'] if top else 0}, indicating strong organizational alignment.

Quick Wins: {quick_wins} high-impact, low-effort opportunities are ready for rapid pilot deployment.

Department Leadership: {top_dept} is currently leading innovation momentum with the highest combined innovation score.

Recommendation: Prioritize quick wins for Q2 pilots while advancing strategic bets through structured feasibility assessments. Continue voting and commentary to refine the portfolio."""
