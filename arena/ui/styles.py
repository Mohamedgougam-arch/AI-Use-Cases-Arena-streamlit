CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
}

.stApp {
  background: linear-gradient(180deg, #0a0f0d 0%, #0d1411 50%, #0a0f0d 100%);
}

.block-container {
  padding-top: 1.5rem;
  max-width: 1200px;
}

h1, h2, h3 {
  color: #f0f4f2 !important;
}

[data-testid="stSidebar"] {
  background: rgba(12, 18, 15, 0.95);
  border-right: 1px solid rgba(141, 198, 63, 0.15);
}

[data-testid="stSidebar"] .stRadio label {
  color: #c8d4cc;
}

.stat-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(141, 198, 63, 0.2);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-bottom: 0.5rem;
}

.stat-card .label {
  color: #8a9a90;
  font-size: 0.85rem;
  margin: 0;
}

.stat-card .value {
  color: #8DC63F;
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0.25rem 0 0 0;
}

.glass-panel {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.badge-pill {
  display: inline-block;
  background: rgba(141, 198, 63, 0.15);
  color: #8DC63F;
  border-radius: 999px;
  padding: 0.15rem 0.6rem;
  font-size: 0.75rem;
  margin-right: 0.35rem;
}

.hero-title {
  background: linear-gradient(90deg, #8DC63F, #A8E063);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

div.stButton > button[kind="primary"] {
  background: #8DC63F;
  color: #0a0f0d;
  border: none;
  font-weight: 600;
}

div.stButton > button[kind="primary"]:hover {
  background: #A8E063;
  color: #0a0f0d;
}

.login-box {
  background: rgba(20, 28, 24, 0.9);
  border: 1px solid rgba(141, 198, 63, 0.25);
  border-radius: 16px;
  padding: 2rem;
}
</style>
"""


def inject_styles() -> None:
    import streamlit as st

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
