@echo off
setlocal
cd /d %~dp0
call .venv\Scripts\activate.bat
streamlit run jobbot\ui\dashboard.py
