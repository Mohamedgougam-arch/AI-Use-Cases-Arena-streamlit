from __future__ import annotations

import html
from datetime import datetime, timezone
from typing import Any

import streamlit as st

from arena.auth import normalize_email
from arena.constants import get_display_department
from arena.participants import SCORE_POINTS
from arena.store import ArenaStore

STAT_ICONS = {
    "file": "📄",
    "votes": "👍",
    "trophy": "🏆",
    "building": "🏢",
}


def stat_card(
    label: str,
    value: str | int,
    trend: str | None = None,
    *,
    icon_key: str = "file",
) -> None:
    icon = STAT_ICONS.get(icon_key, "📄")
    trend_html = (
        f'<p class="stat-trend">{html.escape(str(trend))}</p>' if trend else ""
    )
    st.markdown(
        f"""
        <div class="stat-card glass-card-hover">
          <div class="stat-card-inner">
            <div>
              <p class="stat-label">{html.escape(label)}</p>
              <p class="stat-value">{html.escape(str(value))}</p>
              {trend_html}
            </div>
            <div class="stat-icon-box">{icon}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard_hero(
    title: str,
    welcome: str,
    email: str,
    *,
    is_admin: bool,
) -> None:
    st.markdown(
        f"""
        <div class="glass-card dashboard-hero">
          <div class="dashboard-hero-text">
            <p class="hero-welcome">{html.escape(welcome)}</p>
            <h1 class="hero-title-main">{html.escape(title)}</h1>
            <p class="hero-email">{html.escape(email)}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([1, 1])
    with c1:
        if not is_admin:
            if st.button("Submit Use Case →", type="primary", use_container_width=True):
                st.session_state["page"] = "Submit Use Case"
                st.rerun()
    with c2:
        target = "Admin Leaderboard" if is_admin else "Gallery"
        label = "Admin Leaderboard" if is_admin else "Browse Gallery"
        if st.button(label, use_container_width=True):
            st.session_state["page"] = target
            st.rerun()


def section_heading(title: str, *, icon: str = "", icon_tone: str = "primary") -> None:
    tone_class = f"section-icon-{icon_tone}"
    st.markdown(
        f"""
        <h2 class="section-heading">
          <span class="section-icon {tone_class}">{icon}</span>
          {html.escape(title)}
        </h2>
        """,
        unsafe_allow_html=True,
    )


def empty_state(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="empty-state">
          <div class="empty-state-icon">📥</div>
          <p class="empty-state-title">{html.escape(title)}</p>
          <p class="empty-state-desc">{html.escape(description)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def innovation_momentum_card(total_votes: int, has_data: bool) -> None:
    display = str(total_votes) if has_data else "—"
    st.markdown(
        f"""
        <div class="glass-card momentum-card">
          <h2 class="momentum-title">Innovation Momentum</h2>
          <p class="momentum-value text-gradient">{html.escape(display)}</p>
          <p class="momentum-caption">total votes cast</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def heatmap_html(dept_stats: list[dict[str, Any]]) -> str:
    if not dept_stats:
        return (
            '<p class="muted-copy">Department activity will appear here once '
            "use cases are submitted.</p>"
        )
    cells = []
    for d in dept_stats:
        alpha = min(0.4, d["innovationScore"] / 500)
        dept = html.escape(d["department"])
        count = d["useCaseCount"]
        cells.append(
            f"""
            <div class="heatmap-cell" style="background:rgba(141,198,63,{alpha});">
              <p class="heatmap-dept">{dept}</p>
              <p class="heatmap-count">{count}</p>
            </div>
            """
        )
    return f'<div class="heatmap-grid">{"".join(cells)}</div>'


def quick_win_item(title: str, score: int, uc_id: str) -> None:
    safe = html.escape(title)
    if st.button(safe, key=f"qw_{uc_id}", use_container_width=True):
        st.session_state["detail_id"] = uc_id
        st.session_state["page"] = "Use Case Detail"
        st.rerun()


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
                    st.toast(f"+{SCORE_POINTS['voteCast']} point — vote recorded")
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
        <div class="glass-card glass-card-hover use-case-card">
          <h3 class="uc-title">{title}</h3>
          {badges}
          <p class="uc-desc">{desc}</p>
          <p class="uc-meta">
            {html.escape(get_display_department(use_case['department']))} ·
            {html.escape(use_case['category'])} · Impact {html.escape(use_case['impact'])} ·
            <strong class="uc-votes">{use_case['votes']} votes</strong>
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
        <div class="glass-card page-hero">
          <h1 class="page-hero-title">{html.escape(title)}</h1>
          <p class="page-hero-sub">{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
