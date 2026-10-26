#!/usr/bin/env bash
# macOS Build Script for File Organizer Pro
set -e

echo "=== Building File Organizer for macOS ==="

# Ensure pyinstaller is installed
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pyinstaller

# Build macOS app bundle and standalone binary
pyinstaller --onefile --windowed --name "FileOrganizer" file_organizer.py

# Package into zip for easy distribution
cd dist
if [ -d "FileOrganizer.app" ]; then
    zip -r "FileOrganizer-macOS.zip" "FileOrganizer.app"
else
    zip "FileOrganizer-macOS.zip" "FileOrganizer"
fi
cd ..

echo "=== Build Complete! Find the binary or zip in the dist/ folder ==="
