@echo off
setlocal EnableExtensions EnableDelayedExpansion

title CyberShield AI - Backend Server

echo ==============================================================================
echo   CYBERSHIELD AI - FASTAPI BACKEND ONE-CLICK LAUNCHER
echo   AI-Powered Web Threat Detection and Digital Trust Intelligence
echo ==============================================================================
echo.

:: ------------------------------------------------------------------------------
:: 1. Detect Project Directory and Backend Path
:: ------------------------------------------------------------------------------
set "PROJECT_ROOT=%~dp0"
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
set "BACKEND_DIR=%PROJECT_ROOT%\backend"

echo [1/6] Inspecting project environment...
echo       Project Root : %PROJECT_ROOT%
echo       Backend Dir  : %BACKEND_DIR%

if not exist "%BACKEND_DIR%\app\main.py" (
    echo.
    echo [ERROR] Backend entry point not found at "%BACKEND_DIR%\app\main.py".
    echo Please make sure CyberShield.bat is placed inside the project root folder.
    echo.
    pause
    exit /b 1
)

:: ------------------------------------------------------------------------------
:: 2. Detect Python Environment (VirtualEnv or System Python)
:: ------------------------------------------------------------------------------
echo [2/6] Detecting Python environment...

set "PYTHON_EXE="
set "VENV_DIR="

if exist "%PROJECT_ROOT%\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"
    set "VENV_DIR=%PROJECT_ROOT%\.venv"
) else if exist "%BACKEND_DIR%\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%BACKEND_DIR%\.venv\Scripts\python.exe"
    set "VENV_DIR=%BACKEND_DIR%\.venv"
) else if exist "%PROJECT_ROOT%\venv\Scripts\python.exe" (
    set "PYTHON_EXE=%PROJECT_ROOT%\venv\Scripts\python.exe"
    set "VENV_DIR=%PROJECT_ROOT%\venv"
) else if exist "%BACKEND_DIR%\venv\Scripts\python.exe" (
    set "PYTHON_EXE=%BACKEND_DIR%\venv\Scripts\python.exe"
    set "VENV_DIR=%BACKEND_DIR%\venv"
)

if not defined PYTHON_EXE (
    for /f "delims=" %%I in ('where python.exe 2^>nul') do (
        set "PYTHON_EXE=%%I"
        goto :python_found
    )
)

:python_found
if not defined PYTHON_EXE (
    echo.
    echo [ERROR] Python was not detected on your system or in a virtual environment.
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    echo During installation, be sure to check "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

if defined VENV_DIR (
    echo       Using Virtual Environment: %VENV_DIR%
) else (
    echo       Using System Python: %PYTHON_EXE%
)

:: Verify Python version (requires >= 3.10)
"%PYTHON_EXE%" -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>nul
if errorlevel 1 (
    echo [WARNING] Python 3.10 or higher is recommended for CyberShield AI.
)

:: ------------------------------------------------------------------------------
:: 3. Verify Required Dependencies
:: ------------------------------------------------------------------------------
echo [3/6] Verifying required backend dependencies...

"%PYTHON_EXE%" -c "import fastapi, uvicorn, pydantic, web3, sqlalchemy, httpx" 2>nul
if not errorlevel 1 goto :deps_ok

echo.
echo [WARNING] Some required dependencies are missing.
echo Installing dependencies from backend\requirements.txt...
"%PYTHON_EXE%" -m pip install -r "%BACKEND_DIR%\requirements.txt"
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install backend dependencies.
    echo Please run manually: pip install -r backend\requirements.txt
    echo.
    pause
    exit /b 1
)
echo       Dependencies successfully installed.

:deps_ok
echo       All core dependencies verified: fastapi, uvicorn, pydantic, web3, sqlalchemy.

:: ------------------------------------------------------------------------------
:: 4. Environment Configuration (.env check)
:: ------------------------------------------------------------------------------
echo [4/6] Checking application configuration...

if not exist "%BACKEND_DIR%\.env" (
    if exist "%BACKEND_DIR%\.env.example" (
        copy "%BACKEND_DIR%\.env.example" "%BACKEND_DIR%\.env" >nul
        echo       Created backend\.env from template with default local configuration.
    ) else (
        echo       No .env file found; using default built-in configuration.
    )
) else (
    echo       Configuration file backend\.env is present.
)

set "APP_HOST=127.0.0.1"
set "APP_PORT=8000"

:: ------------------------------------------------------------------------------
:: 5. Port Conflict and Existing Instance Check
:: ------------------------------------------------------------------------------
echo [5/6] Checking port availability on %APP_HOST%:%APP_PORT%...

set "PORT_IN_USE=0"
set "EXISTING_PID="
for /f "tokens=4,5" %%A in ('netstat -ano -p tcp ^| findstr ":%APP_PORT%"') do (
    if "%%A"=="LISTENING" (
        set "PORT_IN_USE=1"
        set "EXISTING_PID=%%B"
    )
)

if "!PORT_IN_USE!"=="0" goto :port_is_free

echo.
echo ==============================================================================
echo [WARNING] Port %APP_PORT% is already in use by PID !EXISTING_PID!.
echo An instance of CyberShield AI may already be running.
echo ==============================================================================
echo.
echo Options:
echo   [1] Open API documentation in browser for the running instance [Default]
echo   [2] Stop existing instance and restart CyberShield AI
echo   [3] Cancel and exit
echo.
set /p "PORT_CHOICE=Enter choice [1/2/3, default: 1]: "
if "!PORT_CHOICE!"=="" set "PORT_CHOICE=1"

if "!PORT_CHOICE!"=="1" (
    start "" "http://%APP_HOST%:%APP_PORT%/docs"
    exit /b 0
)
if "!PORT_CHOICE!"=="2" (
    echo Stopping PID !EXISTING_PID!...
    taskkill /F /PID !EXISTING_PID! >nul 2>&1
    ping 127.0.0.1 -n 3 >nul
    goto :port_is_free
)
exit /b 0

:port_is_free
echo       Port %APP_PORT% is available.

:: ------------------------------------------------------------------------------
:: 6. Blockchain Operating Mode Detection
:: ------------------------------------------------------------------------------
echo [6/6] Inspecting blockchain configuration and RPC status...

set "BLOCKCHAIN_MODE=TRANSPARENT SIMULATION [Local Off-Chain]"
set "BLOCKCHAIN_DETAIL=Threat reports are cryptographically fingerprinted and verified off-chain."

for /f "tokens=4,5" %%A in ('netstat -ano -p tcp ^| findstr ":8545"') do (
    if "%%A"=="LISTENING" (
        set "BLOCKCHAIN_MODE=LIVE EVM NODE DETECTED [http://127.0.0.1:8545]"
        set "BLOCKCHAIN_DETAIL=Real EVM node connected. Threat report hashes will be committed on-chain."
    )
)

echo       Blockchain Mode : !BLOCKCHAIN_MODE!
echo       Note            : !BLOCKCHAIN_DETAIL!
echo.

:: ------------------------------------------------------------------------------
:: 7. Start FastAPI Backend & Open Browser Documentation
:: ------------------------------------------------------------------------------
echo ==============================================================================
echo   CYBERSHIELD AI BACKEND IS STARTING!
echo ==============================================================================
echo.
echo   API Base URL      : http://%APP_HOST%:%APP_PORT%
echo   Swagger Web UI    : http://%APP_HOST%:%APP_PORT%/docs
echo   ReDoc Web UI      : http://%APP_HOST%:%APP_PORT%/redoc
echo   Health Endpoint   : http://%APP_HOST%:%APP_PORT%/health
echo   API v1 Health     : http://%APP_HOST%:%APP_PORT%/api/v1/health
echo   Blockchain Status : !BLOCKCHAIN_MODE!
echo.
echo   Opening Swagger Documentation in your default web browser...
start "" "http://%APP_HOST%:%APP_PORT%/docs"
echo.
echo ==============================================================================
echo   Streaming live server request logs below. Press CTRL+C to stop.
echo   To stop the server from another terminal, run STOP_CyberShield.bat
echo ==============================================================================
echo.

cd /d "%BACKEND_DIR%"
if defined VENV_DIR call "%VENV_DIR%\Scripts\activate.bat" 2>nul
"%PYTHON_EXE%" -m uvicorn app.main:app --host %APP_HOST% --port %APP_PORT%

if errorlevel 1 (
    echo.
    echo [ERROR] CyberShield AI backend terminated with an error.
    pause
)
