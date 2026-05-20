from __future__ import annotations

import time

import streamlit as st
import streamlit.components.v1 as st_components


def fire_confetti() -> None:
    """Invest-NL colored confetti (matches Vercel canvas-confetti)."""
    st_components.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
        <script>
        (function() {
          const doc = window.parent.document;
          const canvas = doc.createElement("canvas");
          canvas.style.cssText = "position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:99999;";
          doc.body.appendChild(canvas);
          const cf = confetti.create(canvas, { resize: true, useWorker: true });
          const colors = ["#8DC63F", "#1F6F78", "#A8E063"];
          cf({ particleCount: 120, spread: 70, origin: { y: 0.6 }, colors });
          setTimeout(function() {
            cf({ particleCount: 60, spread: 100, origin: { y: 0.5 }, colors });
          }, 200);
          setTimeout(function() { doc.body.removeChild(canvas); }, 4000);
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


def celebrate_submission(points: int, *, redirect_page: str = "Gallery", delay_s: float = 1.5) -> None:
    """Confetti, toast, success banner, then redirect (like Vercel setTimeout)."""
    show_submit_success(points)
    fire_confetti()
    st.balloons()
    st.toast(
        f"+{points} points — Your use case is live and linked to your email.",
        icon="🎉",
    )
    time.sleep(delay_s)
    st.session_state["page"] = redirect_page
    st.rerun()
