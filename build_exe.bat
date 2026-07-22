@echo off
REM Run this on Windows, in the same folder as file_organizer.py

python -m pip install --upgrade pyinstaller
pyinstaller --onefile --windowed --name "FileOrganizer" file_organizer.py

echo.
echo Done. Find FileOrganizer.exe inside the "dist" folder.
pause
