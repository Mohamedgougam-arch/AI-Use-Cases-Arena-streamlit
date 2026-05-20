from __future__ import annotations

"""Invest-NL Arena theme — aligned with the Next.js dark UI."""

# Design tokens (dark theme from globals.css)
BG = "#071a1d"
CARD = "rgba(14, 42, 47, 0.82)"
PRIMARY = "#8DC63F"
PRIMARY_LIGHT = "#A8E063"
FOREGROUND = "#f5f7fa"
MUTED = "#b7c4c8"
SECONDARY = "#1f6f78"

BASE_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
  font-family: 'Inter', system-ui, sans-serif;
}}

.stApp {{
  background-color: {BG};
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(141, 198, 63, 0.14), transparent),
    radial-gradient(ellipse 60% 40% at 100% 0%, rgba(31, 111, 120, 0.12), transparent),
    linear-gradient(180deg, {BG} 0%, #0a2226 50%, {BG} 100%);
}}

/* Hide Streamlit chrome noise */
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{
  background: transparent;
}}

.block-container {{
  padding-top: 1.25rem;
  padding-bottom: 3rem;
  max-width: 72rem;
}}

h1, h2, h3, h4 {{
  color: {FOREGROUND} !important;
  font-weight: 700;
  letter-spacing: -0.02em;
}}

p, label, .stMarkdown, span {{
  color: {FOREGROUND};
}}

.stCaption, small {{
  color: {MUTED} !important;
}}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {{
  background-color: rgba(7, 26, 29, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 0.5rem !important;
  color: {FOREGROUND} !important;
}}

.stTextInput input:focus, .stTextArea textarea:focus {{
  border-color: rgba(141, 198, 63, 0.5) !important;
  box-shadow: 0 0 0 1px rgba(141, 198, 63, 0.25) !important;
}}

/* Primary buttons */
div.stButton > button[kind="primary"],
form button[kind="primaryFormSubmit"] {{
  background: linear-gradient(180deg, {PRIMARY} 0%, #6fa82e 100%) !important;
  color: {BG} !important;
  border: none !important;
  font-weight: 600 !important;
  border-radius: 0.5rem !important;
  padding: 0.65rem 1.25rem !important;
  box-shadow: 0 0 20px rgba(141, 198, 63, 0.25) !important;
}}

div.stButton > button[kind="primary"]:hover,
form button[kind="primaryFormSubmit"]:hover {{
  background: linear-gradient(180deg, {PRIMARY_LIGHT} 0%, {PRIMARY} 100%) !important;
}}

div.stButton > button[kind="secondary"] {{
  background: rgba(255, 255, 255, 0.06) !important;
  color: {FOREGROUND} !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
}}

/* Sidebar (authenticated app) */
[data-testid="stSidebar"] {{
  background: rgba(14, 42, 47, 0.95) !important;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}}

[data-testid="stSidebar"] .stRadio label {{
  color: {MUTED};
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
}}

[data-testid="stSidebar"] .stRadio label:hover {{
  color: {FOREGROUND};
  background: rgba(255, 255, 255, 0.05);
}}

[data-testid="stMetric"] {{
  background: {CARD};
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 0.75rem 1rem;
}}

[data-testid="stMetricValue"] {{
  color: {PRIMARY} !important;
}}

/* Glass panels */
.glass-card, .glass-panel {{
  background: {CARD};
  background-image: radial-gradient(ellipse at top left, rgba(141, 198, 63, 0.08), transparent 55%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(12px);
}}

.glass-card-hover {{
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}}

.glass-card-hover:hover {{
  border-color: rgba(141, 198, 63, 0.35);
  box-shadow: 0 0 20px rgba(141, 198, 63, 0.12);
}}

.text-gradient {{
  background: linear-gradient(90deg, {PRIMARY}, {PRIMARY_LIGHT});
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}

.eyebrow {{
  color: {PRIMARY};
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin: 0 0 0.75rem 0;
}}

.stat-card {{
  background: {CARD};
  background-image: radial-gradient(ellipse at top left, rgba(141, 198, 63, 0.06), transparent 50%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 0.5rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
}}

.stat-card .label {{
  color: {MUTED};
  font-size: 0.85rem;
  margin: 0;
}}

.stat-card .value {{
  color: {PRIMARY};
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0.25rem 0 0 0;
}}

.badge-pill {{
  display: inline-block;
  background: rgba(141, 198, 63, 0.15);
  color: {PRIMARY};
  border-radius: 999px;
  padding: 0.2rem 0.65rem;
  font-size: 0.75rem;
  margin-right: 0.35rem;
  border: 1px solid rgba(141, 198, 63, 0.2);
}}

.page-hero {{
  background: {CARD};
  background-image: radial-gradient(ellipse at top left, rgba(141, 198, 63, 0.1), transparent 50%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem 2rem;
  margin-bottom: 1.5rem;
}}

.highlight-item {{
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}}

.highlight-icon {{
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  background: rgba(141, 198, 63, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 1.1rem;
}}

.highlight-title {{
  font-weight: 600;
  font-size: 0.9rem;
  color: {FOREGROUND};
  margin: 0 0 0.15rem 0;
}}

.highlight-desc {{
  font-size: 0.8rem;
  color: {MUTED};
  margin: 0;
  line-height: 1.45;
}}

.divider {{
  border: none;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  margin: 1rem 0;
}}

.section-title {{
  font-size: 1.15rem;
  font-weight: 700;
  color: {FOREGROUND};
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}

/* In-app forms (submit, etc.) */
body:not(.arena-login-active) div[data-testid="stForm"] {{
  background: {CARD};
  background-image: radial-gradient(ellipse at top left, rgba(141, 198, 63, 0.06), transparent 55%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem 1.75rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25);
}}
</style>
"""

LOGIN_CSS = f"""
<style>
/* Login page: full-width, no sidebar */
body.arena-login-active section[data-testid="stSidebar"] {{
  display: none !important;
}}

body.arena-login-active .block-container {{
  max-width: 80rem;
  padding-top: 2rem;
}}

body.arena-login-active [data-testid="stAppViewContainer"] > section.main {{
  padding-left: 2rem;
  padding-right: 2rem;
}}

/* Animated particles */
body.arena-login-active .stApp::before {{
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background-image:
    radial-gradient(circle at 15% 20%, rgba(141, 198, 63, 0.15) 0px, transparent 2px),
    radial-gradient(circle at 85% 30%, rgba(141, 198, 63, 0.1) 0px, transparent 2px),
    radial-gradient(circle at 45% 70%, rgba(31, 111, 120, 0.12) 0px, transparent 2px),
    radial-gradient(circle at 70% 80%, rgba(141, 198, 63, 0.08) 0px, transparent 2px);
  background-size: 100% 100%;
  opacity: 0.9;
}}

body.arena-login-active .main .block-container {{
  position: relative;
  z-index: 1;
}}

.logo-box {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
  padding: 0.5rem;
  border-radius: 1rem;
  background: #fff;
  box-shadow: 0 0 20px rgba(141, 198, 63, 0.15);
  margin-bottom: 1.5rem;
}}

.logo-box img {{
  display: block;
  max-width: 100%;
  max-height: 100%;
}}

.logo-box-fallback {{
  font-weight: 800;
  font-size: 1.1rem;
  color: #3d4548;
  letter-spacing: -0.05em;
}}

.sidebar-logo {{
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin-bottom: 0.75rem;
}}

.sidebar-logo .logo-box {{
  width: 2.5rem;
  height: 2.5rem;
  padding: 0.35rem;
  margin-bottom: 0;
}}

.login-hero h1 {{
  font-size: clamp(1.75rem, 4vw, 3.25rem);
  line-height: 1.15;
  margin: 0 0 1rem 0;
  color: {FOREGROUND} !important;
}}

.login-hero .lead {{
  font-size: 1.125rem;
  color: {MUTED};
  line-height: 1.6;
  max-width: 36rem;
  margin: 0;
}}

/* Sign-in card (form column) */
body.arena-login-active div[data-testid="stForm"] {{
  background: {CARD} !important;
  background-image: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(141, 198, 63, 0.18), transparent) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 1rem !important;
  padding: 2rem 2.25rem !important;
  box-shadow: 0 0 20px rgba(141, 198, 63, 0.1), 0 4px 24px rgba(0, 0, 0, 0.35) !important;
}}

body.arena-login-active div[data-testid="stForm"] h3 {{
  font-size: 1.25rem !important;
  margin-bottom: 0.25rem !important;
}}

body.arena-login-active .login-form-hint {{
  color: {MUTED};
  font-size: 0.875rem;
  margin: 0 0 1.25rem 0;
}}

body.arena-login-active .login-form-hint strong {{
  color: {FOREGROUND};
  font-weight: 600;
}}

body.arena-login-active .gdpr-notice {{
  color: {MUTED};
  font-size: 0.68rem;
  line-height: 1.5;
  margin-top: 1rem;
}}

.about-tool {{
  background: {CARD};
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
  margin-top: 2.5rem;
  max-width: 48rem;
  margin-left: auto;
  margin-right: auto;
}}

.about-tool h3 {{
  font-size: 1rem;
  margin: 0 0 0.75rem 0;
}}

.about-tool p {{
  color: {MUTED};
  font-size: 0.875rem;
  line-height: 1.6;
  margin: 0;
}}

.about-tool .credit {{
  margin-top: 1rem;
  font-size: 0.75rem;
  color: rgba(183, 196, 200, 0.7);
}}
</style>
"""


def inject_styles(*, login: bool = False) -> None:
    import streamlit as st

    st.markdown(BASE_CSS, unsafe_allow_html=True)
    if login:
        st.markdown(LOGIN_CSS, unsafe_allow_html=True)


def set_login_body_class(active: bool) -> None:
    """Add/remove body class for login-specific CSS (Streamlit runs in iframe)."""
    import streamlit.components.v1 as components

    flag = "true" if active else "false"
    components.html(
        f"""
        <script>
        (function() {{
          const doc = window.parent.document;
          if ({flag}) doc.body.classList.add('arena-login-active');
          else doc.body.classList.remove('arena-login-active');
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
