@echo off
setlocal EnableExtensions EnableDelayedExpansion

title Stop CyberShield AI Backend

echo ==============================================================================
echo   CYBERSHIELD AI - SAFE BACKEND SHUTDOWN
echo ==============================================================================
echo.

set "PORT=8000"
set "KILLED_COUNT=0"

echo [1/3] Searching for CyberShield AI process listening on port %PORT%...

for /f "tokens=4,5" %%A in ('netstat -ano -p tcp ^| findstr ":%PORT%"') do (
    if "%%A"=="LISTENING" (
        set "PID_TO_KILL=%%B"
        if defined PID_TO_KILL (
            echo [2/3] Terminating backend process with PID: !PID_TO_KILL!...
            taskkill /F /PID !PID_TO_KILL! >nul 2>&1
            if not errorlevel 1 (
                set /a KILLED_COUNT+=1
                echo       Successfully stopped process !PID_TO_KILL!.
            )
        )
    )
)

:: Also close the dedicated server terminal window if still open
echo [3/3] Closing any active CyberShield server terminal windows...
taskkill /F /FI "WINDOWTITLE eq CyberShield AI - Backend Server*" >nul 2>&1

ping 127.0.0.1 -n 2 >nul

:: Verify port is freed
set "STILL_BUSY=0"
for /f "tokens=4,5" %%A in ('netstat -ano -p tcp ^| findstr ":%PORT%"') do (
    if "%%A"=="LISTENING" (
        set "STILL_BUSY=1"
    )
)

echo.
echo ==============================================================================
if "!STILL_BUSY!"=="0" (
    echo   [SUCCESS] CyberShield AI backend has been completely stopped.
    echo   Port %PORT% is now free.
) else (
    echo   [WARNING] Port %PORT% still appears to be occupied.
    echo   You may need to manually inspect Task Manager for PID !PID_TO_KILL!.
)
echo ==============================================================================
echo.
ping 127.0.0.1 -n 2 >nul
exit /b 0
