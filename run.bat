@echo off
echo Starting ArchiGenie Backend...
set PYTHONPATH=%cd%
start cmd /k "uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload --log-level debug"
timeout /t 3
echo Starting ArchiGenie Frontend...
start cmd /k "streamlit run frontend/main.py"
echo All services started successfully!
exit
