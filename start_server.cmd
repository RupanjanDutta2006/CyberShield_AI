@echo off
setlocal
title CyberShield AI - Backend Server
echo ==============================================================================
echo   CYBERSHIELD AI - FASTAPI BACKEND SERVER
echo ==============================================================================
echo.
cd /d "%~dp0backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
