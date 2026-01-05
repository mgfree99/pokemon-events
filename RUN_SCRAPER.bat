@echo off
title Pokemon Events Scraper

echo.
echo ========================================
echo POKEMON EVENTS SCRAPER
echo ========================================
echo.
echo This will scrape Pokemon events and
echo update your GitHub repository.
echo.
echo The browser will open - this is normal!
echo.
pause

echo.
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    pause
    exit
)

echo.
echo Installing/updating required packages...
pip install selenium webdriver-manager

echo.
echo Starting scraper...
echo.

python scraper_local.py

echo.
echo ========================================
echo SCRAPER FINISHED
echo ========================================
echo.
pause
