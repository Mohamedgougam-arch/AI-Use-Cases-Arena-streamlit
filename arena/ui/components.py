from __future__ import annotations

import html
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
    title = html.escape(use_case["title"])
    desc = html.escape(use_case["description"])
    if len(desc) > 200:
        desc = desc[:200] + "..."
    badges = " ".join(
        f'<span class="badge-pill">{html.escape(b)}</span>'
        for b in use_case.get("badges", [])
    )
    st.markdown(
        f"""
        <div class="glass-card glass-card-hover" style="margin-bottom:0.75rem;">
          <h3 style="margin:0 0 0.5rem 0;font-size:1.1rem;">{title}</h3>
          {badges}
          <p style="color:#b7c4c8;font-size:0.875rem;margin:0.5rem 0 0.75rem 0;">{desc}</p>
          <p style="color:#8a9a90;font-size:0.75rem;margin:0;">
            {get_display_department(use_case['department'])} · {use_case['category']} ·
            Impact {use_case['impact']} · <strong style="color:#8DC63F;">{use_case['votes']} votes</strong>
          </p>
        </div>
        """,
        unsafe_allow_html=True,
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


def page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="page-hero">
          <h1 style="margin:0 0 0.35rem 0;font-size:1.75rem;">{title}</h1>
          <p style="margin:0;color:#b7c4c8;font-size:0.95rem;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
