from __future__ import annotations

from typing import Any

from arena.constants import departments_match
from arena.scoring import get_effort_score, get_impact_score, is_quick_win


def filter_and_sort_use_cases(
    use_cases: list[dict[str, Any]],
    *,
    search: str = "",
    department: str | None = None,
    category: str | None = None,
    impact: str | None = None,
    effort: str | None = None,
    tag: str | None = None,
    sort: str = "most-votes",
) -> list[dict[str, Any]]:
    result = list(use_cases)

    if search:
        q = search.lower()
        result = [
            uc
            for uc in result
            if q in uc["title"].lower()
            or q in uc["description"].lower()
            or any(q in t.lower() for t in uc.get("tags", []))
        ]
    if department:
        result = [uc for uc in result if departments_match(uc["department"], department)]
    if category:
        result = [uc for uc in result if uc["category"] == category]
    if impact:
        result = [uc for uc in result if uc["impact"] == impact]
    if effort:
        result = [uc for uc in result if uc["effort"] == effort]
    if tag:
        result = [uc for uc in result if tag in uc.get("tags", [])]

    if sort == "most-votes":
        result.sort(key=lambda uc: uc["votes"], reverse=True)
    elif sort == "newest":
        result.sort(key=lambda uc: uc["createdAt"], reverse=True)
    elif sort == "highest-impact":
        result.sort(key=lambda uc: get_impact_score(uc["impact"]), reverse=True)
    elif sort == "lowest-effort":
        result.sort(key=lambda uc: get_effort_score(uc["effort"]))
    elif sort == "trending":
        result.sort(key=lambda uc: uc["innovationScore"], reverse=True)
    elif sort == "quick-wins":
        result = [uc for uc in result if is_quick_win(uc)]
        result.sort(key=lambda uc: uc["innovationScore"], reverse=True)

    return result


def collect_tags(use_cases: list[dict[str, Any]]) -> list[str]:
    tags: set[str] = set()
    for uc in use_cases:
        tags.update(uc.get("tags", []))
    return sorted(tags)
