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

# Matches src/components/ui/badge.tsx variants (inline styles avoid sanitiser glitches).
BADGE_PALETTE: dict[str, tuple[str, str, str]] = {
    "Trending": ("rgba(249, 115, 22, 0.12)", "rgba(249, 115, 22, 0.35)", "#fb923c"),
    "High Impact": ("rgba(16, 185, 129, 0.12)", "rgba(16, 185, 129, 0.35)", "#34d399"),
    "Quick Win": ("rgba(6, 182, 212, 0.12)", "rgba(6, 182, 212, 0.35)", "#22d3ee"),
    "Strategic Bet": ("rgba(168, 85, 247, 0.12)", "rgba(168, 85, 247, 0.35)", "#c084fc"),
    "Crowd Favorite": ("rgba(236, 72, 153, 0.12)", "rgba(236, 72, 153, 0.35)", "#f472b6"),
}


def _badge_span(label: str) -> str:
    bg, border, color = BADGE_PALETTE.get(
        label, ("rgba(31, 111, 120, 0.2)", "rgba(31, 111, 120, 0.35)", "#c8e6ea")
    )
    safe = html.escape(label)
    return (
        "<span style=\"display:inline-block;box-sizing:border-box;margin:0 0.35rem 0.35rem 0;"
        "padding:0.15rem 0.6rem;border-radius:999px;font-size:0.7rem;font-weight:600;"
        f"line-height:1.35;background:{bg};color:{color};border:1px solid {border};\">"
        f"{safe}</span>"
    )


def _meta_pill(text: str) -> str:
    """Department chip (Vercel bg-secondary/30)."""
    safe = html.escape(text)
    return (
        "<span style=\"display:inline-block;box-sizing:border-box;margin:0 0.5rem 0.25rem 0;"
        "padding:0.15rem 0.5rem;border-radius:0.375rem;font-size:0.75rem;line-height:1.35;"
        "background:rgba(31,111,120,0.3);color:#c8e6ea;border:none;\">"
        f"{safe}</span>"
    )


def _meta_outline_chip(text: str) -> str:
    """Category / status chip (Vercel outline badge)."""
    safe = html.escape(text)
    return (
        "<span style=\"display:inline-block;box-sizing:border-box;margin:0 0.5rem 0.25rem 0;"
        "padding:0.15rem 0.5rem;border-radius:0.375rem;font-size:0.75rem;line-height:1.35;"
        "color:#b7c4c8;border:1px solid rgba(255,255,255,0.12);"
        "background:rgba(14,42,47,0.55);\">"
        f"{safe}</span>"
    )


def _meta_text(label: str, value: str) -> str:
    safe = html.escape(f"{label}: {value}")
    return (
        "<span style=\"display:inline-block;box-sizing:border-box;margin:0 0.5rem 0.25rem 0;"
        "font-size:0.75rem;line-height:1.35;color:#b7c4c8;white-space:nowrap;\">"
        f"{safe}</span>"
    )


def _meta_votes(count: int) -> str:
    return (
        "<span style=\"display:inline-block;box-sizing:border-box;margin:0 0.5rem 0.25rem 0;"
        "font-size:0.75rem;line-height:1.35;color:#8DC63F;font-weight:600;white-space:nowrap;\">"
        f"{count} votes</span>"
    )


def _meta_comments(count: int) -> str:
    return (
        "<span style=\"display:inline-block;box-sizing:border-box;margin:0 0.5rem 0.25rem 0;"
        "font-size:0.75rem;line-height:1.35;color:#b7c4c8;white-space:nowrap;\">"
        f"💬 {count}</span>"
    )


def _meta_line(use_case: dict[str, Any]) -> str:
    """Single-line metadata row (all inline styles for Streamlit sanitizer)."""
    parts = [
        _meta_pill(get_display_department(use_case["department"])),
        _meta_outline_chip(use_case["category"]),
        _meta_text("Impact", use_case["impact"]),
        _meta_text("Effort", use_case["effort"]),
        _meta_comments(len(use_case.get("comments", []))),
        _meta_votes(use_case["votes"]),
    ]
    return (
        "<p style=\"margin:0.5rem 0 0 0;padding:0;line-height:1.9;\">"
        f"{''.join(parts)}</p>"
    )


def _date_badge(iso: str) -> str:
    safe = html.escape(format_date(iso))
    return (
        "<span style=\"display:inline-flex;align-items:center;gap:0.25rem;box-sizing:border-box;"
        "padding:0.15rem 0.5rem;border-radius:0.375rem;font-size:0.7rem;font-weight:500;"
        "color:#b7c4c8;border:1px solid rgba(255,255,255,0.12);background:rgba(245,247,250,0.05);\">"
        f"📅 {safe}</span>"
    )


def _status_badge(status: str) -> str:
    safe = html.escape(status)
    return (
        "<span style=\"display:inline-block;box-sizing:border-box;padding:0.15rem 0.5rem;"
        "border-radius:0.375rem;font-size:0.7rem;font-weight:500;color:#b7c4c8;"
        "border:1px solid rgba(255,255,255,0.1);background:rgba(14,42,47,0.6);\">"
        f"{safe}</span>"
    )


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
    if trend:
        safe_trend = html.escape(str(trend))
        trend_html = (
            "<p style=\"margin:0.35rem 0 0 0;color:#8DC63F;font-size:0.75rem;"
            "line-height:1.3;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;\">"
            f"{safe_trend}</p>"
        )
    else:
        trend_html = ""
    card = (
        "<div style=\"display:flex;justify-content:space-between;align-items:flex-start;"
        "gap:0.75rem;background:rgba(14,42,47,0.82);border:1px solid rgba(255,255,255,0.1);"
        "border-radius:12px;padding:1.25rem;margin-bottom:0.5rem;box-shadow:0 4px 24px rgba(0,0,0,0.2);\">"
        "<div style=\"flex:1;min-width:0;\">"
        f"<p style=\"margin:0;color:#b7c4c8;font-size:0.875rem;\">{safe_label}</p>"
        "<p style=\"margin:0.35rem 0 0 0;color:#f5f7fa;font-size:1.875rem;font-weight:700;"
        f"line-height:1.1;\">{safe_value}</p>"
        f"{trend_html}</div>"
        "<span style=\"flex-shrink:0;display:inline-flex;align-items:center;justify-content:center;"
        "width:2.5rem;height:2.5rem;border-radius:0.5rem;background:rgba(141,198,63,0.12);"
        f"font-size:1.15rem;\">{icon}</span></div>"
    )
    st.markdown(card, unsafe_allow_html=True)


def dashboard_hero(
    title: str,
    welcome: str,
    email: str,
    *,
    is_admin: bool,
) -> None:
    """Hero banner with CTAs on the right (Vercel dashboard-home)."""
    st.markdown('<span class="hero-panel-marker"></span>', unsafe_allow_html=True)
    text_col, btn_col = st.columns([2.4, 1], gap="large")
    with text_col:
        st.markdown(
            f"<p style=\"margin:0;color:#b7c4c8;font-size:0.875rem;\">{html.escape(welcome)}</p>"
            f"<h1 style=\"margin:0.25rem 0 0 0;color:#f5f7fa;font-size:1.75rem;font-weight:700;"
            f"letter-spacing:-0.02em;\">{html.escape(title)}</h1>"
            f"<p style=\"margin:0.35rem 0 0 0;color:#b7c4c8;font-size:0.875rem;"
            f"max-width:28rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;\">"
            f"{html.escape(email)}</p>",
            unsafe_allow_html=True,
        )
    with btn_col:
        if not is_admin:
            if st.button("Submit Use Case →", type="primary", use_container_width=True):
                st.session_state["page"] = "Submit Use Case"
                st.rerun()
        target = "Admin Leaderboard" if is_admin else "Gallery"
        label = "Admin Leaderboard" if is_admin else "Browse Gallery"
        if st.button(label, type="secondary", use_container_width=True):
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


def render_vote_box(store: ArenaStore, email: str, use_case: dict[str, Any]) -> None:
    """Vertical vote control (matches Vercel VoteButton compact)."""
    uc_id = use_case["id"]
    voted = store.has_voted(email, uc_id)
    st.markdown('<span class="vote-box-marker"></span>', unsafe_allow_html=True)
    icon = "▼" if voted else "▲"
    if voted:
        if st.button(icon, key=f"unvote_{uc_id}", help="Remove vote", type="primary"):
            store.unvote(email, uc_id)
            st.rerun()
    elif st.button(icon, key=f"vote_{uc_id}", help="Vote"):
        if store.vote(email, uc_id):
            st.toast(f"+{SCORE_POINTS['voteCast']} point — vote recorded")
        st.rerun()
    st.markdown(
        f'<p class="vote-count-caption">{use_case["votes"]}</p>',
        unsafe_allow_html=True,
    )


def render_vote_controls(
    store: ArenaStore, email: str, use_case: dict[str, Any], *, compact: bool = False
) -> None:
    """Horizontal vote controls for detail page."""
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
    show_detail_button: bool = True,
) -> None:
    """List card matching Vercel UseCaseCard (vote left, content right, one glass row)."""
    title = html.escape(use_case["title"])
    desc = html.escape(use_case["description"])
    if len(desc) > 200:
        desc = desc[:200] + "..."
    popular = ""
    if use_case["votes"] >= 5:
        popular = (
            "<p style=\"margin:0 0 0.5rem 0;\">"
            + _badge_span(f"Popular · {use_case['votes']} votes")
            + "</p>"
        )
    tags = use_case.get("tags") or []
    tag_bits = "".join(
        "<span style=\"display:inline-block;box-sizing:border-box;margin:0 0.25rem 0.25rem 0;"
        "padding:0.1rem 0.45rem;border-radius:999px;font-size:0.7rem;color:#b7c4c8;"
        "background:rgba(255,255,255,0.06);\">"
        f"#{html.escape(t)}</span>"
        for t in tags[:3]
    )
    submitter = html.escape(
        use_case.get("submitterEmail") or use_case.get("submitter") or "Unknown"
    )
    rel_date = html.escape(format_relative_date(use_case["createdAt"]))
    card_body = (
        "<div style=\"min-width:0;\">"
        "<div style=\"display:flex;justify-content:space-between;align-items:flex-start;"
        "gap:0.75rem;margin-bottom:0.5rem;\">"
        f"<h3 style=\"margin:0;font-size:1rem;font-weight:700;color:#f5f7fa;"
        f"line-height:1.3;flex:1;min-width:0;\">{title}</h3>"
        "<div style=\"display:flex;flex-wrap:wrap;gap:0.35rem;justify-content:flex-end;"
        "flex-shrink:0;\">"
        f"{_date_badge(use_case['createdAt'])}"
        f"{_status_badge(use_case.get('status', 'Submitted'))}"
        "</div></div>"
        f"<p style=\"margin:0 0 0.5rem 0;font-size:0.875rem;color:#b7c4c8;line-height:1.45;"
        f"display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;\">"
        f"{desc}</p>"
        f"{popular}"
        f"{_meta_line(use_case)}"
        f"<p style=\"margin:0.5rem 0 0 0;font-size:0.7rem;color:#8a9a90;\">"
        f"by {submitter} · {rel_date}</p>"
        f"<p style=\"margin:0.35rem 0 0 0;line-height:1.6;\">{tag_bits}</p>"
        "</div>"
    )
    col_vote, col_body = st.columns([1, 11], gap="small")
    with col_vote:
        st.markdown('<span class="uc-list-marker"></span>', unsafe_allow_html=True)
        if show_vote:
            render_vote_box(store, email, use_case)
    with col_body:
        st.markdown(card_body, unsafe_allow_html=True)
        detail_key = f"detail_{use_case['id']}"
        detail_label = "View details" if show_detail_button else "View use case →"
        if st.button(detail_label, key=detail_key, type="secondary", use_container_width=True):
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
