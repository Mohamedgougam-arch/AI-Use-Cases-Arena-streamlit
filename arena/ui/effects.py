from __future__ import annotations

import time

import streamlit as st
import streamlit.components.v1 as st_components


def clear_celebration_effects() -> None:
    """Remove confetti canvases and balloon nodes left in the Streamlit parent document."""
    st_components.html(
        """
        <script>
        (function() {
          const doc = window.parent.document;
          doc.querySelectorAll("canvas[data-arena-confetti]").forEach(function(c) {
            c.remove();
          });
          doc.querySelectorAll('[data-testid="stBalloons"]').forEach(function(el) {
            el.remove();
          });
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def fire_confetti() -> None:
    """Invest-NL colored confetti (matches Vercel canvas-confetti)."""
    st_components.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
        <script>
        (function() {
          const doc = window.parent.document;
          doc.querySelectorAll("canvas[data-arena-confetti]").forEach(function(c) {
            c.remove();
          });
          const canvas = doc.createElement("canvas");
          canvas.setAttribute("data-arena-confetti", "1");
          canvas.style.cssText = "position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:99999;";
          doc.body.appendChild(canvas);
          const cf = confetti.create(canvas, { resize: true, useWorker: true });
          const colors = ["#8DC63F", "#1F6F78", "#A8E063"];
          cf({ particleCount: 120, spread: 70, origin: { y: 0.6 }, colors, ticks: 160 });
          setTimeout(function() {
            cf({ particleCount: 60, spread: 100, origin: { y: 0.5 }, colors, ticks: 120 });
          }, 200);
          setTimeout(function() {
            if (canvas.parentNode) canvas.parentNode.removeChild(canvas);
          }, 2200);
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
    st.toast(
        f"+{points} points — Your use case is live and linked to your email.",
        icon="🎉",
    )
    time.sleep(delay_s)
    st.session_state["page"] = redirect_page
    st.session_state.pop("_celebration_active", None)
    st.rerun()
