@echo off
cd /d "%~dp0"
set PYTHONPATH=%~dp0
echo ============================================================
echo   Starting ClimaCare AI FastAPI Backend
echo   API Server: http://localhost:5000
echo   Swagger UI: http://localhost:5000/docs
echo ============================================================
call ".\venv\Scripts\python.exe" app.py
pause
