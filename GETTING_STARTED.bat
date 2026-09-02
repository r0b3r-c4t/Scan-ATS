@echo off
echo ==========================================
echo Scan-ATS - Full Stack Application
echo ==========================================
echo.
echo This script helps you run both backend and frontend
echo.
echo Requirements:
echo - Python 3.8+
echo - Node.js 18+
echo - pnpm
echo - MongoDB (for backend)
echo.
echo To run the application:
echo.
echo Terminal 1 - Start Backend:
echo   cd backend
echo   python -m uvicorn app.main:app --reload
echo.
echo Terminal 2 - Start Frontend:
echo   cd frontend
echo   pnpm dev
echo.
echo Then open: http://localhost:5173
echo.
echo API Documentation: http://localhost:8000/docs
echo.
echo ==========================================
pause
