from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as st_components


def _purge_legacy_confetti() -> None:
    """Remove any leftover confetti canvases from older deploys (no CDN load)."""
    st_components.html(
        """
        <script>
        (function() {
          const doc = window.parent.document;
          doc.querySelectorAll("canvas[data-arena-confetti]").forEach(function(c) {
            c.remove();
          });
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def show_submit_success(points: int) -> None:
    st.markdown(
        f"""
        <div class="success-celebration" role="status">
          <p class="success-celebration-title">+{points} points</p>
          <p class="success-celebration-desc">Your use case is live and linked to your email.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def celebrate_submission(points: int, *, redirect_page: str = "Gallery") -> None:
    """Redirect immediately; toast and banner show on the next page (no blocking sleep)."""
    st.session_state["submit_toast_points"] = points
    st.session_state["page"] = redirect_page
    st.rerun()


def show_post_submit_feedback() -> bool:
    """Call once at top of Gallery/Dashboard after redirect. Returns True if shown."""
    points = st.session_state.pop("submit_toast_points", None)
    if points is None:
        return False
    _purge_legacy_confetti()
    show_submit_success(points)
    st.toast(
        f"+{points} points — Your use case is live and linked to your email.",
        icon="🎉",
    )
    return True
