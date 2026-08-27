@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo JobHunterX is not installed yet.
  echo Running first-time installation...
  call install_windows.bat
)

call .venv\Scripts\activate.bat
python run_dashboard.py
pause
