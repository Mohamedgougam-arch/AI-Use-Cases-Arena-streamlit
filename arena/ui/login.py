from __future__ import annotations

import streamlit as st

from arena.ui.styles import set_login_body_class

LOGO_SVG = """
<svg width="40" height="40" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect x="4" y="8" width="8" height="32" rx="2" fill="#8DC63F"/>
  <rect x="16" y="14" width="8" height="26" rx="2" fill="#1F6F78"/>
  <rect x="28" y="6" width="8" height="34" rx="2" fill="#8DC63F"/>
  <rect x="40" y="18" width="4" height="22" rx="1" fill="#A8E063"/>
</svg>
"""

HIGHLIGHTS = [
    ("📄", "Submit ideas", "Share AI use cases from your team at Invest-NL."),
    ("👍", "Vote and prioritize", "Vote or change your mind; click again to remove a vote."),
    ("🏆", "Track contribution", "See your impact on the leaderboard."),
]


def _highlights_html() -> str:
    items = []
    for icon, title, desc in HIGHLIGHTS:
        items.append(
            f'<div class="highlight-item">'
            f'<div class="highlight-icon">{icon}</div>'
            f'<div><p class="highlight-title">{title}</p>'
            f'<p class="highlight-desc">{desc}</p></div></div>'
        )
    return "\n".join(items)


def render_login() -> None:
    set_login_body_class(True)

    col_hero, col_form = st.columns([1.15, 0.85], gap="large")

    with col_hero:
        st.markdown(
            f"""
            <div class="login-hero">
              <div class="logo-box">{LOGO_SVG}</div>
              <p class="eyebrow">Invest-NL Innovation Arena</p>
              <h1>Shape the future of <span class="text-gradient">AI at Invest-NL</span></h1>
              <p class="lead">Submit, explore, vote, and prioritize the AI use cases that can
              transform our organization.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(_highlights_html(), unsafe_allow_html=True)

    with col_form:
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### Sign in to continue")
            st.markdown(
                '<p class="login-form-hint">Use your work email, or type '
                '<strong>Admin</strong> for administrator access.</p>',
                unsafe_allow_html=True,
            )
            email_input = st.text_input(
                "Work email or Admin",
                placeholder="you@invest-nl.nl or Admin",
                label_visibility="visible",
            )
            submitted = st.form_submit_button(
                "Continue to Arena",
                type="primary",
                use_container_width=True,
            )

        st.markdown(
            """
            <p class="gdpr-notice">GDPR notice: your email address is collected and used solely to
            operate the AI Use Cases Arena (identifying your submissions, votes, and comments within
            this tool). It is not used for marketing, is not sold to third parties, and is retained
            only for as long as needed for this initiative. You may request access to or deletion of
            your data by contacting your Invest-NL programme administrator.</p>
            """,
            unsafe_allow_html=True,
        )

        if submitted:
            from arena.auth import try_login
            from arena.store import ArenaStore

            ok, email, is_admin = try_login(email_input)
            if ok and email:
                st.session_state["auth_email"] = email
                st.session_state["auth_is_admin"] = is_admin
                store: ArenaStore = st.session_state["store"]
                if not is_admin:
                    store.register_login(email)
                set_login_body_class(False)
                st.session_state["page"] = "Dashboard"
                st.rerun()
            else:
                st.error("Enter a valid work email or Admin for administrator access.")

    st.markdown(
        """
        <section class="about-tool">
          <h3>About this tool</h3>
          <p>The AI Use Cases Arena is an internal Invest-NL application for collecting,
          discussing, and prioritizing AI ideas. Teams submit use cases, colleagues vote and
          comment, and leaderboards surface the most engaged contributors and ideas.</p>
          <p class="credit">Developed in-house at Invest-NL - Mohamed Gougam · May 2026</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
