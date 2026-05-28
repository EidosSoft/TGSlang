@echo off
setlocal enabledelayedexpansion

:: TGS Launcher v1.0.0
:: Usage: tgs [options] [file.tgs]

set "PYTHON_CMD=python"

:: Проверка наличия Python
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.6+
    pause
    exit /b 1
)

:: Если нет аргументов - показать help
if "%1"=="" (
    %PYTHON_CMD% main.py -h
    exit /b 0
)

:: Обработка специальных флагов
if "%1"=="-v" goto :version
if "%1"=="--version" goto :version
if "%1"=="-h" goto :help
if "%1"=="--help" goto :help
if "%1"=="--install" goto :install

:: Запуск интерпретатора
%PYTHON_CMD% main.py %*
exit /b %errorlevel%

:version
%PYTHON_CMD% main.py --version
exit /b 0

:help
%PYTHON_CMD% main.py --help
echo.
echo Additional Windows-specific options:
echo   tgs --install    - Add TGS to PATH (Admin rights may be required)
exit /b 0

:install
echo Installing TGS to system...
set "BAT_DIR=%~dp0"
set "TARGET_DIR=%USERPROFILE%\tgs"
mkdir "%TARGET_DIR%" 2>nul
copy "%BAT_DIR%\*.*" "%TARGET_DIR%" >nul
echo Created %TARGET_DIR%
setx PATH "%TARGET_DIR%;%PATH%" >nul
echo TGS added to PATH. Please restart your command prompt.
echo Now you can use: tgs script.tgs
exit /b 0