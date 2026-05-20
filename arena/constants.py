from __future__ import annotations

from typing import Literal

Department = Literal[
    "Capital",
    "Market Development",
    "HR",
    "Finance",
    "Operations",
    "Relationship Management",
    "Data management related",
    "IT related",
    "Cyber Security",
]

DEPARTMENTS: tuple[str, ...] = (
    "Capital",
    "Market Development",
    "HR",
    "Finance",
    "Operations",
    "Relationship Management",
    "Data management related",
    "IT related",
    "Cyber Security",
)

DEPARTMENT_LEGACY_ALIASES: dict[str, str] = {"Investment": "Capital"}

CATEGORIES: tuple[str, ...] = (
    "Productivity",
    "Risk",
    "Customer Experience",
    "Finance",
    "Operations",
    "ESG",
    "Investment Analysis",
    "Legal",
    "HR",
    "Other",
)

IMPACT_LEVELS: tuple[str, ...] = ("Low", "Medium", "High")
EFFORT_LEVELS: tuple[str, ...] = ("Low", "Medium", "High")

SORT_OPTIONS: tuple[tuple[str, str], ...] = (
    ("most-votes", "Most votes"),
    ("newest", "Newest"),
    ("highest-impact", "Highest impact"),
    ("lowest-effort", "Lowest effort"),
    ("trending", "Trending"),
    ("quick-wins", "Quick wins"),
)

GAMIFICATION_BADGES: tuple[dict[str, str], ...] = (
    {"id": "ai-explorer", "name": "AI Explorer", "description": "Submitted your first use case"},
    {"id": "innovation-champion", "name": "Innovation Champion", "description": "Earned 200+ XP"},
    {"id": "top-contributor", "name": "Top Contributor", "description": "Submitted 3+ use cases"},
    {"id": "quick-win-finder", "name": "Quick Win Finder", "description": "High-impact, low-effort idea"},
    {"id": "popular-idea", "name": "Popular Idea", "description": "20+ votes on a use case"},
    {"id": "arena-champion", "name": "Arena Champion", "description": "Reached Arena Champion rank"},
    {"id": "strategic-thinker", "name": "Strategic Thinker", "description": "Submitted a strategic bet"},
    {"id": "collaboration-hero", "name": "Collaboration Hero", "description": "Added 5+ comments"},
)


def is_known_department(value: str) -> bool:
    return value.strip() in DEPARTMENTS


def normalize_department(value: str) -> str:
    trimmed = value.strip()
    if is_known_department(trimmed):
        return trimmed
    return DEPARTMENT_LEGACY_ALIASES.get(trimmed, trimmed)


def departments_match(a: str, b: str) -> bool:
    return normalize_department(a) == normalize_department(b)


def get_display_department(value: str) -> str:
    normalized = normalize_department(value)
    return normalized if is_known_department(normalized) else value
