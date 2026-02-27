@echo off
echo ========================================
echo Skill Credential Aggregator System
echo Starting Backend Server...
echo ========================================
echo.

:: Use the venv's Python directly to avoid pip installing to global Python
set VENV_PYTHON="%~dp0.venv\Scripts\python.exe"

echo Installing dependencies into virtual environment...
%VENV_PYTHON% -m pip install -r backend\requirements.txt

echo.
echo Starting Flask server...
echo Backend will run on http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

%VENV_PYTHON% backend\app.py

pause
