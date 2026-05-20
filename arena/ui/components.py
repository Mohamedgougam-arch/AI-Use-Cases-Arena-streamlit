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
    """KPI card matching Vercel StatCard (inline styles avoid Streamlit HTML sanitiser bugs)."""
    icon = STAT_ICONS.get(icon_key, "📄")
    safe_label = html.escape(label)
    safe_value = html.escape(str(value))
    trend_html = (
        f'<p style="margin:0.35rem 0 0 0;color:#8DC63F;font-size:0.75rem;line-height:1.3;'
        f"overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">"
        f"{html.escape(str(trend))}</p>"
        if trend
        else ""
    )
    card = (
        '<div class="arena-stat-card" style="display:flex;justify-content:space-between;'
        "align-items:flex-start;gap:0.75rem;background:rgba(14,42,47,0.82);"
        "border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:1.25rem;"
        'margin-bottom:0.5rem;box-shadow:0 4px 24px rgba(0,0,0,0.2);">'
        '<div style="flex:1;min-width:0;">'
        f'<p style="margin:0;color:#b7c4c8;font-size:0.875rem;">{safe_label}</p>'
        f'<p style="margin:0.35rem 0 0 0;color:#f5f7fa;font-size:1.875rem;font-weight:700;'
        f'line-height:1.1;">{safe_value}</p>{trend_html}</div>'
        '<span style="flex-shrink:0;display:inline-flex;align-items:center;justify-content:center;'
        "width:2.5rem;height:2.5rem;border-radius:0.5rem;background:rgba(141,198,63,0.12);"
        f'font-size:1.15rem;">{icon}</span></div>'
    )
    st.markdown(card, unsafe_allow_html=True)


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


def required_select(
    label: str, options: list[str], placeholder: str = "Select..."
) -> str | None:
    """Selectbox with placeholder row (works on all Streamlit versions)."""
    choices = [placeholder, *options]
    picked = st.selectbox(label, choices, index=0)
    return None if picked == placeholder else picked


def page_header(title: str, subtitle: str, *, icon: str = "") -> None:
    icon_html = (
        f'<div class="page-header-icon"><span>{icon}</span></div>' if icon else ""
    )
    st.markdown(
        f"""
        <div class="glass-card page-hero">
          {icon_html}
          <h1 class="page-header-title">{html.escape(title)}</h1>
          <p class="page-header-sub">{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
