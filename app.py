"""
AI Use Cases Arena — Streamlit application for Invest-NL.

Run: streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from arena.auth import ADMIN_DISPLAY_NAME
from arena.participants import (
    build_participant_scores,
    get_participant_score,
    is_participant_score_leader,
)
from arena.store import ArenaStore
from arena.ui import pages
from arena.ui.login import render_login
from arena.ui.styles import inject_styles, set_login_body_class

st.set_page_config(
    page_title="AI Use Cases Arena",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

is_authenticated_preview = bool(st.session_state.get("auth_email"))
inject_styles(login=not is_authenticated_preview)

if "store" not in st.session_state:
    st.session_state["store"] = ArenaStore()

store: ArenaStore = st.session_state["store"]
store.reload()

email: str | None = st.session_state.get("auth_email")
is_admin: bool = st.session_state.get("auth_is_admin", False)
is_authenticated = bool(email)

USER_PAGES = [
    "Dashboard",
    "Submit Use Case",
    "Gallery",
    "Insights",
    "Department Battle",
]

ADMIN_PAGES = [
    "Dashboard",
    "Gallery",
    "Insights",
    "Admin Leaderboard",
    "Department Battle",
]


def logout() -> None:
    for key in ("auth_email", "auth_is_admin", "detail_id", "exec_summary"):
        st.session_state.pop(key, None)
    st.session_state["page"] = "Dashboard"
    set_login_body_class(False)
    st.rerun()


if not is_authenticated:
    set_login_body_class(True)
    render_login()
    st.stop()

set_login_body_class(False)
inject_styles(login=False)

nav_pages = ADMIN_PAGES if is_admin else USER_PAGES
current = st.session_state.get("page", "Dashboard")
if current not in nav_pages and current != "Use Case Detail":
    st.session_state["page"] = "Dashboard"
    current = "Dashboard"

with st.sidebar:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem;">
          <span style="display:inline-flex;width:2.25rem;height:2.25rem;border-radius:0.6rem;
          background:rgba(141,198,63,0.2);align-items:center;justify-content:center;">✨</span>
          <div><p style="margin:0;font-weight:700;font-size:0.9rem;">AI Use Cases</p>
          <p style="margin:0;color:#8DC63F;font-size:0.75rem;">Arena</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sidebar_index = nav_pages.index(current) if current in nav_pages else 0
    choice = st.radio(
        "Navigate",
        nav_pages,
        index=sidebar_index,
        label_visibility="collapsed",
    )
    if choice != st.session_state["page"]:
        st.session_state["page"] = choice
        st.rerun()

    st.divider()

    if is_admin:
        st.caption("Administrator mode")
        st.caption(ADMIN_DISPLAY_NAME)
    else:
        scores = store.use_cases
        my = get_participant_score(scores, email)
        participants = build_participant_scores(scores)
        if is_participant_score_leader(email, participants):
            st.success("🏆 Score leader")
        st.metric("Your score", f"{my['score'] if my else 0} pts")
        if my:
            st.caption(
                f"{my['submissions']} submitted · "
                f"{my['votesReceived']} votes on your ideas · "
                f"{my['votesCast']} votes cast"
            )
        st.caption(email or "")

    if st.button("Sign out", use_container_width=True):
        logout()

    st.markdown(
        """
        <div style="margin-top:1rem;padding:0.75rem;border-radius:0.5rem;
        border:1px solid rgba(255,255,255,0.08);background:rgba(7,26,29,0.5);">
        <p style="margin:0 0 0.35rem 0;font-size:0.75rem;font-weight:600;">About this tool</p>
        <p style="margin:0;font-size:0.65rem;color:#b7c4c8;line-height:1.45;">
        Internal arena to submit, vote on, and prioritize AI use cases across Invest-NL.</p>
        <p style="margin:0.5rem 0 0 0;font-size:0.6rem;color:rgba(183,196,200,0.65);">
        Mohamed Gougam · May 2026</p></div>
        """,
        unsafe_allow_html=True,
    )

page = st.session_state["page"]

if page == "Dashboard":
    pages.render_dashboard(store, email or "", is_admin)
elif page == "Submit Use Case":
    if is_admin:
        st.warning("Administrators cannot submit use cases.")
        st.session_state["page"] = "Dashboard"
        st.rerun()
    else:
        pages.render_submit(store, email or "")
elif page == "Gallery":
    pages.render_gallery(store, email or "")
elif page == "Use Case Detail":
    pages.render_detail(store, email or "", is_admin)
elif page == "Insights":
    pages.render_insights(store)
elif page == "Admin Leaderboard":
    if not is_admin:
        st.session_state["page"] = "Dashboard"
        st.rerun()
    else:
        pages.render_leaderboard(store)
elif page == "Department Battle":
    pages.render_battle(store)
