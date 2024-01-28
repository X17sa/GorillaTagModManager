@echo off

REM Check if Python is installed
py -c "exit()" 2>nul
if %errorlevel% neq 0 (
    REM Python is not installed
    echo Python is not installed. Downloading and installing now...
    
    REM Download Python installer
    bitsadmin.exe /transfer "Downloading Python" https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe %TEMP%\python-3.9.7-amd64.exe
    
    REM Install Python silently
    %TEMP%\python-3.9.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    REM Check if Python installation was successful
    py -c "exit()" 2>nul
    if %errorlevel% neq 0 (
        echo Failed to install Python. Please install Python manually.
        pause
        exit /b 1
    ) else (
        echo Python has been successfully installed.
    )
)

REM Install required Python packages using pip
echo Installing required Python packages...
py -m pip install pyttsx3 requests

echo Setup complete.
pause
