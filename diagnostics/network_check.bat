@echo off
echo ========================================
echo IGUS ROBOT - NETWORK DIAGNOSTICS
echo ========================================
echo.
echo Laptop network configuration:
ipconfig
echo.
echo Testing controller ping at 192.168.3.11
ping -n 4 192.168.3.11
echo.
echo Checking whether TCP port 3920 is reachable...
powershell -NoProfile -Command "Test-NetConnection 192.168.3.11 -Port 3920"
echo.
pause