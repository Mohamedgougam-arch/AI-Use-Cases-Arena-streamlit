from __future__ import annotations

import re

AUTH_STORAGE_KEY = "ai-use-cases-arena-auth"
ADMIN_EMAIL = "arena-admin@invest-nl.nl"
ADMIN_DISPLAY_NAME = "Arena Admin"
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def is_admin_login(value: str) -> bool:
    return value.strip().lower() == "admin"


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email.strip().lower()))


def normalize_email(email: str) -> str:
    return email.strip().lower()


def is_admin_email(email: str) -> bool:
    return normalize_email(email) == ADMIN_EMAIL


def get_display_name_from_email(email: str) -> str:
    local = normalize_email(email).split("@")[0] or email
    name = re.sub(r"[._-]+", " ", local).strip()
    if not name:
        return email
    return " ".join(part.capitalize() for part in name.split() if part)


def get_avatar_from_email(email: str) -> str:
    local = normalize_email(email).split("@")[0] or ""
    parts = re.sub(r"[._-]+", " ", local).strip().split()
    if len(parts) >= 2:
        return f"{(parts[0][:1] or '').upper()}{(parts[1][:1] or '').upper()}"
    return (local[:2] or "??").upper()


def try_login(raw_input: str) -> tuple[bool, str | None, bool]:
    """Return (ok, email, is_admin)."""
    trimmed = raw_input.strip()
    if is_admin_login(trimmed):
        return True, ADMIN_EMAIL, True
    normalized = normalize_email(trimmed)
    if not is_valid_email(normalized):
        return False, None, False
    return True, normalized, False
