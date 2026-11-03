@echo off
title J.A.R.V.I.S. Local - Startup Protocol
color 0B
echo ==================================================
echo   INITIALIZING J.A.R.V.I.S. LOCAL (MIT STANDARD)
echo ==================================================

echo [1/3] Starting Python Backend (FastAPI / Uvicorn)...
start cmd /k "cd /d C:\Users\samud\projects\projeto_Comando_de_Voz\J.A.R.V.I.S_Local\jarvis-backend && call venv\Scripts\activate && python -m uvicorn main:app --host 127.0.0.1 --port 8000"

echo [2/3] Waiting for backend initialization...
timeout /t 4 /nobreak >nul

echo [3/3] Starting React Frontend HUD...
start cmd /k "cd /d C:\Users\samud\projects\projeto_Comando_de_Voz\J.A.R.V.I.S_Local\jarvis-frontend && npm run dev"

echo Waiting for HUD server...
timeout /t 3 /nobreak >nul

echo Opening Holographic HUD...
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --new-window "http://localhost:5173"
) else (
    start http://localhost:5173
)

echo ==================================================
echo   J.A.R.V.I.S. ONLINE. READY FOR VOICE AND TEXT.
echo ==================================================
pause
