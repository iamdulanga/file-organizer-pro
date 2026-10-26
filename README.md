# 📁 File Organizer Pro

A modern, fast, cross-platform desktop application for **Windows, macOS, and Linux** that automatically organizes files into categorized folders based on their file extensions.

Designed with reliability, performance, and simplicity in mind, the application features native system interfaces, non-blocking background processing, duplicate file collision protection, undo support, and detailed logging.

---

## ✨ Features

- 📂 **Organize files automatically** by extension into structured category folders.
- 🖥️ **Cross-Platform & Native Look**:
  - **Windows**: Modern Windows native styling (Segoe UI + high-DPI awareness).
  - **macOS**: Native Aqua theme and system font support.
  - **Linux**: Clean Clam / GTK desktop integration.
- ⚡ **Background Processing**: UI never freezes during scans or moves (`threading` + `queue`).
- 📊 **Real-time Live Progress Bar**: Live percentage indicator, item counter, and filename display.
- ↩️ **Undo Last Organization**: Restores moved files back to their exact original locations.
- 🛑 **Cancel Anytime**: Halts the operation safely without corrupting ongoing work.
- 🛡️ **Safe Duplicate Collision Protection**: Automatically renames collisions to `file (1).ext` — never overwrites files.
- 🔒 **Self-Protection**: Automatically skips program scripts, executables, and project files.
- 📝 **Automatic Logging**: Detailed error tracking to `~/file_organizer.log` with a one-click "View Log" button.
- 🧹 **Skips System Files**: Ignores `desktop.ini`, `thumbs.db`, `.DS_Store`, and `.directory`.
- 📦 **Standalone Executables**: Runs without needing Python installed on Windows, macOS, or Linux.

---

## 🗂️ File Categories

The organizer automatically sorts files into folders:

- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.tiff`, `.ico`, `.webp`, `.heif`, `.avif`
- **Documents**: `.pdf`, `.docx`, `.doc`, `.txt`, `.pptx`, `.ppt`, `.xls`, `.xlsx`, `.csv`, `.rtf`, `.odt`, `.ods`, `.odp`
- **Music**: `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.m4a`, `.wma`, `.opus`
- **Videos**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.flv`, `.wmv`, `.webm`, `.mpeg`, `.3gp`
- **Archives**: `.zip`, `.rar`, `.tar`, `.gz`, `.7z`, `.bz2`, `.xz`, `.cab`, `.iso`
- **Scripts**: `.py`, `.js`, `.sh`, `.bat`, `.rb`, `.php`, `.pl`, `.lua`, `.swift`, `.ps1`
- **Source Code**: `.c`, `.cpp`, `.h`, `.hpp`, `.java`, `.cs`, `.go`, `.ts`, `.rs`, `.kt`, `.dart`, `.html`, `.css`, `.json`, `.xml`, `.sql`
- **Executables**: `.exe`, `.msi`, `.dmg`, `.apk`, `.appimage`
- **Fonts**: `.ttf`, `.otf`, `.woff`, `.woff2`
- **Disk Images**: `.img`, `.bin`, `.vhd`, `.vmdk`
- **Databases**: `.sqlite`, `.db`, `.mdb`, `.accdb`
- **3D Models**: `.obj`, `.stl`, `.fbx`, `.gltf`, `.blend`
- **Torrents**: `.torrent`
- **Others**: Unrecognized file extensions

---

## 📋 Requirements

- **Python**: 3.10+
- Built with Python standard libraries (`tkinter`, `pathlib`, `threading`, `queue`, `logging`, `dataclasses`, `shutil`).
- No external Python dependencies required for running from source.

---

## 🚀 Running from Source

```bash
git clone https://github.com/iamdulanga/file-organizer-pro.git
cd file-organizer-pro
python file_organizer.py
```

*(On macOS/Linux, use `python3 file_organizer.py`)*

---

## 🔨 Building Standalone Executables Locally

### Windows
Double-click `build_exe.bat` or run:
```cmd
pyinstaller --onefile --windowed --name "FileOrganizer" file_organizer.py
```
Output: `dist/FileOrganizer.exe`

### macOS
Run the build script:
```bash
chmod +x build_mac.sh
./build_mac.sh
```
Output: `dist/FileOrganizer-macOS.zip` (contains `.app` bundle)

### Linux
Run the build script:
```bash
chmod +x build_linux.sh
./build_linux.sh
```
Output: `dist/FileOrganizer-Linux-x64.tar.gz`

---

## 🤖 Automated Multi-Platform GitHub Actions

This repository includes automated CI/CD (`.github/workflows/build.yml`):

1. **On every push or pull request**: Builds are automatically tested on Windows, macOS, and Linux runners.
2. **On release tag (e.g. `v1.0.0`)**: Automatically builds and uploads all three distribution packages to **GitHub Releases**:
   - `FileOrganizer-Windows-x64.exe`
   - `FileOrganizer-macOS.zip`
   - `FileOrganizer-Linux-x64.tar.gz`

---

## 🛡️ Safety & Reliability

- **Non-Destructive**: Never overwrites existing destination files; resolves conflicts safely.
- **Self-Protecting**: Prevents moving the application itself or essential project files.
- **Graceful Error Handling**: Skips and logs locked/permission-restricted files instead of crashing.
- **Full Undo**: Move history is tracked in memory, allowing complete reversal of changes.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

Developed by **Dulanga Dasanayake**  
GitHub: [@iamdulanga](https://github.com/iamdulanga)