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
from arena.ui.styles import inject_styles

st.set_page_config(
    page_title="AI Use Cases Arena",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

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
    st.rerun()


if not is_authenticated:
    pages.render_login()
    st.stop()

nav_pages = ADMIN_PAGES if is_admin else USER_PAGES
current = st.session_state.get("page", "Dashboard")
if current not in nav_pages and current != "Use Case Detail":
    st.session_state["page"] = "Dashboard"
    current = "Dashboard"

with st.sidebar:
    st.markdown("### ✨ AI Use Cases")
    st.caption("Arena · Invest-NL")

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

    with st.expander("About this tool"):
        st.write(
            "Collaborative arena to submit, vote on, and prioritize AI use cases "
            "across Invest-NL. Data is stored locally on the server for this demo instance."
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
