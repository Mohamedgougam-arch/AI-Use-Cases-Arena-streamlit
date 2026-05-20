from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import streamlit as st

from arena.auth import normalize_email
from arena.constants import get_display_department
from arena.participants import SCORE_POINTS
from arena.store import ArenaStore


def stat_card(label: str, value: str | int, trend: str | None = None) -> None:
    trend_html = f'<p style="color:#8a9a90;font-size:0.75rem;margin:0.25rem 0 0 0;">{trend}</p>' if trend else ""
    st.markdown(
        f"""<div class="stat-card">
        <p class="label">{label}</p>
        <p class="value">{value}</p>{trend_html}</div>""",
        unsafe_allow_html=True,
    )


def format_relative_date(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        days = (now - dt).days
        if days == 0:
            return "Today"
        if days == 1:
            return "Yesterday"
        if days < 7:
            return f"{days} days ago"
        if days < 30:
            return f"{days // 7} weeks ago"
        return dt.strftime("%d %b %Y")
    except ValueError:
        return iso[:10]


def format_date(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y")
    except ValueError:
        return iso[:10]


def render_vote_controls(
    store: ArenaStore, email: str, use_case: dict[str, Any], *, compact: bool = False
) -> None:
    uc_id = use_case["id"]
    voted = store.has_voted(email, uc_id)
    cols = st.columns([1, 2] if compact else [1, 3])
    with cols[0]:
        if voted:
            if st.button("♥", key=f"unvote_{uc_id}", help="Remove vote"):
                store.unvote(email, uc_id)
                st.rerun()
        else:
            if st.button("♡", key=f"vote_{uc_id}", help="Vote"):
                if store.vote(email, uc_id):
                    pts = SCORE_POINTS["voteCast"]
                    st.toast(f"+{pts} point — vote recorded")
                st.rerun()
    with cols[1]:
        st.caption(f"**{use_case['votes']}** votes")


def render_use_case_card(
    store: ArenaStore,
    email: str,
    use_case: dict[str, Any],
    *,
    show_vote: bool = True,
) -> None:
    with st.container():
        st.markdown(f"### {use_case['title']}")
        badges = " ".join(f'<span class="badge-pill">{b}</span>' for b in use_case.get("badges", []))
        if badges:
            st.markdown(badges, unsafe_allow_html=True)
        st.caption(use_case["description"][:200] + ("..." if len(use_case["description"]) > 200 else ""))
        meta = (
            f"{get_display_department(use_case['department'])} · "
            f"{use_case['category']} · Impact {use_case['impact']} · "
            f"{use_case['votes']} votes · {len(use_case.get('comments', []))} comments"
        )
        st.caption(meta)
        st.caption(
            f"by {use_case.get('submitterEmail') or use_case.get('submitter', '')} · "
            f"{format_relative_date(use_case['createdAt'])} · Score {use_case['innovationScore']}"
        )
        c1, c2 = st.columns([1, 1])
        with c1:
            if show_vote:
                render_vote_controls(store, email, use_case, compact=True)
        with c2:
            if st.button("View details", key=f"detail_{use_case['id']}"):
                st.session_state["detail_id"] = use_case["id"]
                st.session_state["page"] = "Use Case Detail"
                st.rerun()
        st.divider()


def page_header(title: str, subtitle: str) -> None:
    st.title(title)
    st.caption(subtitle)
