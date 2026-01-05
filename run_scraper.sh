#!/bin/bash

echo ""
echo "========================================"
echo "POKEMON EVENTS SCRAPER"
echo "========================================"
echo ""
echo "This will scrape Pokemon events and"
echo "update your GitHub repository."
echo ""
echo "The browser will open - this is normal!"
echo ""
read -p "Press Enter to continue..."

echo ""
echo "Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Python not found!"
    echo "Please install Python 3"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""
echo "Installing/updating required packages..."
pip3 install selenium webdriver-manager

echo ""
echo "Starting scraper..."
echo ""

python3 scraper_local.py

echo ""
echo "========================================"
echo "SCRAPER FINISHED"
echo "========================================"
echo ""
read -p "Press Enter to exit..."
