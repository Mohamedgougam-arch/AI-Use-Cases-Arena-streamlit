@echo off
cd /d "%~dp0"
if exist .venv\Scripts\python.exe (
  .venv\Scripts\streamlit run app.py
) else (
  py -3 -m streamlit run app.py 2>nul || python -m streamlit run app.py
)
