@echo off

:: Überprüfe, ob Python installiert ist
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python ist nicht installiert. Es wird heruntergeladen und installiert.
    
    :: Download the latest Python installer (Windows)
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe -OutFile python_installer.exe"
    
    :: Installiere Python ohne Benutzerinteraktion
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Lösche die Installer-Datei nach der Installation
    del python_installer.exe
    
    :: Überprüfe erneut, ob Python installiert wurde
    python --version >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo Python konnte nicht installiert werden. Bitte manuell installieren.
        pause
        exit /b
    )
)

:: Stelle sicher, dass pip auf dem neuesten Stand ist
python -m ensurepip --upgrade
python -m pip install --upgrade pip

:: Installiere die notwendigen Pakete (dash, plotly, pandas)
python -m pip install dash plotly pandas --user

:: Starte das Python-Skript für das Dashboard
python Dashboard_Code.py

:: Halte das Konsolenfenster nach der Ausführung offen
pause
