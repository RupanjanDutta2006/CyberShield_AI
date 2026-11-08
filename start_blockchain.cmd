@echo off
setlocal
title CyberShield AI - Hardhat Blockchain Node
echo ==============================================================================
echo   CYBERSHIELD AI - HARDHAT LOCAL EVM NODE
echo ==============================================================================
echo.
cd /d "%~dp0blockchain"
if not exist "node_modules" (
    echo [INFO] Installing blockchain dependencies...
    call npm install
)
echo [INFO] Starting local Hardhat EVM node on port 8545...
call npx hardhat node
pause
