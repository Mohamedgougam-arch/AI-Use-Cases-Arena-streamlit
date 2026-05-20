from __future__ import annotations

import html as html_lib

import streamlit as st

from arena.auth import ADMIN_DISPLAY_NAME
from arena.participants import (
    build_participant_scores,
    get_participant_score,
    is_participant_score_leader,
)
from arena.store import ArenaStore
from arena.ui.brand import logo_box_html

USER_NAV = [
    ("Dashboard", "📊"),
    ("Submit Use Case", "➕"),
    ("Gallery", "▦"),
    ("Insights", "📈"),
    ("Department Battle", "⚔"),
]

ADMIN_NAV = [
    ("Dashboard", "📊"),
    ("Gallery", "▦"),
    ("Insights", "📈"),
    ("Admin Leaderboard", "🏆"),
    ("Department Battle", "⚔"),
]


def _score_panel_html(store: ArenaStore, email: str | None, is_admin: bool) -> str:
    if is_admin:
        body = (
            '<p class="sidebar-score-label">Administrator mode</p>'
            '<p class="sidebar-score-detail">Browse, vote, and review the admin leaderboard. '
            "No submissions or personal scoring.</p>"
            f'<p class="sidebar-email">{html_lib.escape(ADMIN_DISPLAY_NAME)}</p>'
        )
    else:
        my = get_participant_score(store.use_cases, email)
        participants = build_participant_scores(store.use_cases)
        leader = (
            '<p class="leader-badge">🏆 Top score</p>'
            if is_participant_score_leader(email, participants)
            else ""
        )
        score = my["score"] if my else 0
        detail = ""
        if my:
            detail = (
                f'<p class="sidebar-score-detail">{my["submissions"]} submitted · '
                f'{my["votesReceived"]} votes on your ideas · '
                f'{my["votesCast"]} votes cast</p>'
            )
        email_line = (
            f'<p class="sidebar-email" title="{html_lib.escape(email or "")}">'
            f"{html_lib.escape(email or '')}</p>"
            if email
            else ""
        )
        body = (
            f"{leader}"
            '<p class="sidebar-score-label">Your score</p>'
            f'<p class="sidebar-score-value">{score} <span>pts</span></p>'
            f"{detail}{email_line}"
        )
    return f'<div class="sidebar-score-panel">{body}</div>'


def render_sidebar(
    store: ArenaStore,
    *,
    email: str | None,
    is_admin: bool,
    nav_pages: list[str],
    current: str,
    on_logout,
) -> None:
    st.markdown(
        f"""
        <div class="sidebar-brand">
          <div class="sidebar-brand-icon">{logo_box_html(width=28)}</div>
          <div>
            <p class="sidebar-brand-title">AI Use Cases</p>
            <p class="sidebar-brand-sub">Arena</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_items = ADMIN_NAV if is_admin else USER_NAV

    for label, icon in nav_items:
        if label not in nav_pages:
            continue
        if st.button(
            f"{icon}  {label}",
            key=f"nav_btn_{label}",
            use_container_width=True,
            type="primary" if label == current else "secondary",
        ):
            if label != current:
                st.session_state["page"] = label
                st.rerun()

    st.markdown(_score_panel_html(store, email, is_admin), unsafe_allow_html=True)

    if st.button("Sign out", key="sign_out_btn", use_container_width=True):
        on_logout()

    st.markdown(
        """
        <div class="about-tool-compact">
          <p class="about-title">About this tool</p>
          <p class="about-body">Internal arena to submit, vote on, and prioritize AI use cases
          across Invest-NL.</p>
          <p class="about-credit">Developed in-house at Invest-NL - Mohamed Gougam · May 2026</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
