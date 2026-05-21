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
  max-width: 100rem;
  padding-left: 2rem;
  padding-right: 2rem;
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

/* KPI stat cards (dashboard) */
.arena-stat-card {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.75rem;
  background: {CARD};
  background-image: radial-gradient(ellipse at top left, rgba(141, 198, 63, 0.06), transparent 50%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 0.5rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}}

.arena-stat-card:hover {{
  border-color: rgba(141, 198, 63, 0.35);
  box-shadow: 0 0 20px rgba(141, 198, 63, 0.12);
}}

.arena-stat-body {{
  flex: 1;
  min-width: 0;
}}

.arena-stat-label {{
  color: {MUTED};
  font-size: 0.875rem;
  margin: 0;
  line-height: 1.3;
}}

.arena-stat-value {{
  color: {FOREGROUND};
  font-size: 1.875rem;
  font-weight: 700;
  margin: 0.35rem 0 0 0;
  line-height: 1.1;
}}

.arena-stat-trend {{
  color: {PRIMARY};
  font-size: 0.75rem;
  margin: 0.35rem 0 0 0;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}}

.arena-stat-icon {{
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(141, 198, 63, 0.12);
  border-radius: 0.5rem;
  width: 2.5rem;
  height: 2.5rem;
  font-size: 1.15rem;
  line-height: 1;
}}

/* st.html iframe: remove extra chrome around stat cards */
div[data-testid="stHtml"] {{
  background: transparent !important;
}}

div[data-testid="stHtml"] iframe {{
  background: transparent !important;
}}

/* Use-case list cards (Vercel UseCaseCard layout) */
.uc-list-marker {{
  display: none;
}}

div[data-testid="stHorizontalBlock"]:has(.uc-list-marker) {{
  background: {CARD};
  background-image: radial-gradient(ellipse at top left, rgba(141, 198, 63, 0.06), transparent 55%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 0.85rem 1rem 0.85rem 0.65rem;
  margin-bottom: 0.75rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
  align-items: flex-start !important;
  transition: border-color 0.2s, box-shadow 0.2s;
}}

div[data-testid="stHorizontalBlock"]:has(.uc-list-marker):hover {{
  border-color: rgba(141, 198, 63, 0.3);
  box-shadow: 0 0 20px rgba(141, 198, 63, 0.1);
}}

div[data-testid="stHorizontalBlock"]:has(.uc-list-marker) div.stButton > button {{
  font-size: 0.75rem !important;
  padding: 0.35rem 0.65rem !important;
  min-height: 2rem !important;
}}

div[data-testid="column"]:has(.vote-box-marker) {{
  flex: 0 0 auto !important;
  min-width: 3.25rem !important;
  max-width: 3.5rem !important;
}}

div[data-testid="column"]:has(.vote-box-marker) div.stButton > button {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 3rem;
  min-height: 3.25rem;
  padding: 0.35rem 0.5rem;
  border-radius: 0.75rem !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  background: rgba(245, 247, 250, 0.05) !important;
  color: {MUTED} !important;
  font-size: 1rem !important;
  line-height: 1.1 !important;
}}

div[data-testid="column"]:has(.vote-box-marker) div.stButton > button:hover {{
  border-color: rgba(141, 198, 63, 0.4) !important;
  background: rgba(141, 198, 63, 0.1) !important;
  color: {PRIMARY} !important;
}}

div[data-testid="column"]:has(.vote-box-marker) div.stButton > button[kind="primary"] {{
  border-color: rgba(141, 198, 63, 0.5) !important;
  background: rgba(141, 198, 63, 0.2) !important;
  color: {PRIMARY} !important;
  box-shadow: 0 0 12px rgba(141, 198, 63, 0.15);
}}

.vote-count-caption {{
  text-align: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: {FOREGROUND};
  margin: 0.15rem 0 0 0;
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

/* Dashboard hero (one glass row: text + CTA buttons) */
.hero-panel-marker {{
  display: none;
}}

div[data-testid="stHorizontalBlock"]:has(.hero-panel-marker) {{
  background: {CARD};
  background-image: radial-gradient(ellipse at top left, rgba(141, 198, 63, 0.1), transparent 50%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.25rem 1.5rem 1.25rem 1.75rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  align-items: center !important;
  gap: 1rem !important;
}}

div[data-testid="stHorizontalBlock"]:has(.hero-panel-marker) div.stButton > button[kind="secondary"] {{
  background: transparent !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: {FOREGROUND} !important;
}}

.dashboard-hero {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1.5rem 2rem !important;
  margin-bottom: 1.5rem;
}}

.hero-welcome {{
  color: {MUTED};
  font-size: 0.875rem;
  margin: 0;
}}

.hero-title-main {{
  font-size: 1.75rem !important;
  margin: 0.25rem 0 0 0 !important;
  color: {FOREGROUND} !important;
}}

.hero-email {{
  color: {MUTED};
  font-size: 0.875rem;
  margin: 0.35rem 0 0 0;
}}

/* Glass panels via column marker */
.panel-glass-start {{
  display: none;
}}

[data-testid="stColumn"]:has(.panel-glass-start) > div > div {{
  background: {CARD};
  background-image: radial-gradient(ellipse at top left, rgba(141, 198, 63, 0.06), transparent 55%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.25rem 1.5rem 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
}}

.section-heading {{
  font-size: 1.125rem;
  font-weight: 700;
  color: {FOREGROUND};
  margin: 0 0 0.85rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  letter-spacing: -0.01em;
}}

.section-icon {{
  font-size: 1.1rem;
}}

.section-icon-primary {{
  filter: none;
}}

.section-icon-orange {{
  color: #fb923c;
}}

.muted-copy {{
  color: {MUTED};
  font-size: 0.875rem;
  margin: 0;
}}

.panel-sub {{
  margin-top: -0.75rem !important;
  margin-bottom: 1rem !important;
}}

.empty-state {{
  text-align: center;
  padding: 2.5rem 1rem;
}}

.empty-state-icon {{
  font-size: 2.5rem;
  opacity: 0.45;
  margin-bottom: 0.75rem;
}}

.empty-state-title {{
  font-size: 1.125rem;
  font-weight: 600;
  color: {FOREGROUND};
  margin: 0 0 0.35rem 0;
}}

.empty-state-desc {{
  font-size: 0.875rem;
  color: {MUTED};
  margin: 0 auto;
  max-width: 22rem;
  line-height: 1.5;
}}

.momentum-card {{
  padding: 1.5rem !important;
  margin-top: 0.5rem;
}}

.momentum-title {{
  font-size: 1.125rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: {FOREGROUND};
}}

.momentum-value {{
  font-size: 1.875rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.1;
}}

.momentum-caption {{
  color: {MUTED};
  font-size: 0.875rem;
  margin: 0.35rem 0 0 0;
}}

.dept-list {{
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}}

.dept-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: {FOREGROUND};
}}

.dept-row strong {{
  color: {PRIMARY};
  font-weight: 700;
}}

.qw-title {{
  font-size: 0.875rem;
  font-weight: 600;
  color: {FOREGROUND};
  margin: 0.75rem 0 0.15rem 0;
}}

.qw-score {{
  font-size: 0.75rem;
  color: {PRIMARY};
  margin: 0 0 0.25rem 0;
}}

.heatmap-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
}}

.heatmap-cell {{
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 0.5rem;
  padding: 1rem 0.75rem;
  text-align: center;
}}

.heatmap-dept {{
  font-size: 0.7rem;
  font-weight: 600;
  margin: 0;
  color: {FOREGROUND};
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}}

.heatmap-count {{
  font-size: 1.125rem;
  font-weight: 700;
  margin: 0.35rem 0 0 0;
  color: {FOREGROUND};
}}

.use-case-card {{
  padding: 1rem 1.25rem !important;
  margin-bottom: 0.75rem !important;
}}

.uc-title {{
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 700;
  color: {FOREGROUND};
}}

.uc-desc {{
  font-size: 0.875rem;
  color: {MUTED};
  margin: 0.35rem 0;
}}

.uc-meta {{
  font-size: 0.75rem;
  color: {MUTED};
  margin: 0.35rem 0 0 0;
}}

.uc-meta .uc-votes {{
  color: {PRIMARY};
  font-weight: 600;
}}

.page-header-icon {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  background: rgba(141, 198, 63, 0.12);
  margin-bottom: 0.75rem;
  font-size: 1.25rem;
}}

.page-header-title {{
  margin: 0 0 0.35rem 0;
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: {FOREGROUND} !important;
}}

.page-header-sub {{
  margin: 0;
  color: {MUTED};
  font-size: 0.9rem;
  line-height: 1.5;
  max-width: 42rem;
}}

.field-label {{
  color: {MUTED};
  font-size: 0.8rem;
  font-weight: 500;
  margin: 0 0 0.35rem 0;
}}

.result-count {{
  color: {MUTED};
  font-size: 0.8rem;
  margin: 0 0 1rem 0;
}}

.form-error {{
  color: #f87171;
  font-size: 0.875rem;
  margin: 0.5rem 0 0 0;
}}

.success-celebration {{
  text-align: center;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  border-radius: 0.75rem;
  border: 1px solid rgba(141, 198, 63, 0.35);
  background: rgba(141, 198, 63, 0.12);
  animation: celebrate-in 0.45s ease-out;
}}

.success-celebration-title {{
  color: {PRIMARY};
  font-size: 1.35rem;
  font-weight: 700;
  margin: 0 0 0.35rem 0;
}}

.success-celebration-desc {{
  color: {MUTED};
  font-size: 0.875rem;
  margin: 0;
}}

@keyframes celebrate-in {{
  from {{ opacity: 0; transform: translateY(12px) scale(0.96); }}
  to {{ opacity: 1; transform: translateY(0) scale(1); }}
}}

body:has(.page-submit-marker) .block-container {{
  max-width: 48rem;
}}

div[data-testid="stForm"] label {{
  color: {MUTED} !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
}}

div[data-testid="stForm"] [data-testid="stFormSubmitButton"] button {{
  min-height: 2.75rem !important;
  font-size: 1rem !important;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
  width: 18rem !important;
  min-width: 18rem !important;
}}

[data-testid="stSidebar"] > div {{
  padding: 1rem 1rem 1.5rem;
}}

.sidebar-brand {{
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}}

.sidebar-brand-icon .logo-box {{
  width: 2.5rem;
  height: 2.5rem;
  padding: 0.35rem;
  margin-bottom: 0;
}}

.sidebar-brand-title {{
  margin: 0;
  font-weight: 700;
  font-size: 0.85rem;
  color: {FOREGROUND};
}}

.sidebar-brand-sub {{
  margin: 0;
  color: {PRIMARY};
  font-size: 0.7rem;
  font-weight: 600;
}}

[data-testid="stSidebar"] div.stButton > button {{
  background: transparent !important;
  border: 1px solid transparent !important;
  color: {MUTED} !important;
  text-align: left !important;
  justify-content: flex-start !important;
  font-weight: 500 !important;
  font-size: 0.875rem !important;
  padding: 0.55rem 0.75rem !important;
  margin-bottom: 0.15rem !important;
  box-shadow: none !important;
  width: 100%;
}}

[data-testid="stSidebar"] div.stButton > button:hover {{
  background: rgba(255, 255, 255, 0.05) !important;
  color: {FOREGROUND} !important;
}}

[data-testid="stSidebar"] div.stButton > button[kind="primary"] {{
  background: rgba(141, 198, 63, 0.1) !important;
  border: 1px solid rgba(141, 198, 63, 0.22) !important;
  color: {PRIMARY} !important;
}}

.sidebar-score-panel {{
  margin-top: 1.25rem;
  padding: 1rem;
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(7, 26, 29, 0.55);
}}

.sidebar-score-label {{
  color: {MUTED};
  font-size: 0.7rem;
  margin: 0 0 0.2rem 0;
}}

.sidebar-score-value {{
  color: {PRIMARY};
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
}}

.sidebar-score-value span {{
  font-size: 0.85rem;
  font-weight: 600;
}}

.sidebar-score-detail {{
  color: rgba(183, 196, 200, 0.75);
  font-size: 0.62rem;
  line-height: 1.4;
  margin: 0.4rem 0 0 0;
}}

.sidebar-email {{
  color: rgba(183, 196, 200, 0.7);
  font-size: 0.62rem;
  margin: 0.35rem 0 0 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}}

.leader-badge {{
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  color: #fbbf24;
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin: 0 0 0.35rem 0;
}}

[data-testid="stSidebar"] div.stButton > button[key="sign_out_btn"] {{
  background: transparent !important;
  border: none !important;
  color: {MUTED} !important;
  text-decoration: underline !important;
  font-size: 0.75rem !important;
  padding: 0.5rem 0 !important;
  margin-top: 0.5rem !important;
}}

.about-tool-compact {{
  margin-top: 1rem;
  padding: 0.65rem 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(7, 26, 29, 0.35);
}}

.about-title {{
  font-size: 0.65rem;
  font-weight: 600;
  color: rgba(183, 196, 200, 0.85);
  margin: 0 0 0.25rem 0;
}}

.about-body {{
  font-size: 0.58rem;
  color: rgba(183, 196, 200, 0.55);
  line-height: 1.4;
  margin: 0;
}}

.about-credit {{
  font-size: 0.55rem;
  color: rgba(183, 196, 200, 0.45);
  line-height: 1.35;
  margin: 0.35rem 0 0 0;
}}

/* Hide default blue info boxes */
div[data-testid="stAlert"] {{
  background: {CARD} !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: {MUTED} !important;
}}

[data-testid="stMetric"] {{
  display: none;
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
