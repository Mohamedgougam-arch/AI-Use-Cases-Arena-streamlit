"""
AI Use Cases Arena — Streamlit application for Invest-NL.

Run: streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from arena.store import ArenaStore
from arena.ui import pages
from arena.ui.login import render_login
from arena.ui.shell import render_sidebar
from arena.ui.styles import inject_styles, set_login_body_class
from arena.ui.brand import LOGO_PATH

_page_icon = str(LOGO_PATH) if LOGO_PATH.is_file() else "✨"

st.set_page_config(
    page_title="AI Use Cases Arena",
    page_icon=_page_icon,
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
    render_sidebar(
        store,
        email=email,
        is_admin=is_admin,
        nav_pages=nav_pages,
        current=current,
        on_logout=logout,
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
