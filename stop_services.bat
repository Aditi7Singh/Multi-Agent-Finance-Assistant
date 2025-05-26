@echo off
echo Stopping Multi-Agent Finance Assistant Services...

:: Kill all Python processes running on our ports
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 :8001 :8002 :8003 :8004 :8005 :8006 :8501"') do (
    taskkill /F /PID %%a
)

echo All services have been stopped!