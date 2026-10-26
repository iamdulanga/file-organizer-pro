#!/usr/bin/env bash
# Linux Build Script for File Organizer Pro
set -e

echo "=== Building File Organizer for Linux ==="

# Ensure pyinstaller is installed
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pyinstaller

# Build standalone binary
pyinstaller --onefile --windowed --name "FileOrganizer" file_organizer.py

# Package into tar.gz for distribution
cd dist
tar -czvf "FileOrganizer-Linux-x64.tar.gz" "FileOrganizer"
cd ..

echo "=== Build Complete! Find the binary or tar.gz in the dist/ folder ==="
