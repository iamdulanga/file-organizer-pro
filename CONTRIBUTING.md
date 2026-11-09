# Contributing to File Organizer Pro

First off, thank you for considering contributing to **File Organizer Pro**! 🎉

Whether you are fixing a bug, adding new file format rules, improving the user interface, or refining documentation, your help is warmly welcomed and appreciated.

---

## 📜 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How Can I Contribute?](#-how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Adding File Categories or Extensions](#adding-file-categories-or-extensions)
  - [Pull Requests](#pull-requests)
- [Development Setup](#-development-setup)
  - [Prerequisites](#prerequisites)
  - [Getting the Code](#getting-the-code)
  - [Running Locally](#running-locally)
- [Code Style & Architecture Guidelines](#-code-style--architecture-guidelines)
- [Testing Your Changes](#-testing-your-changes)
- [Building Standalone Executables](#-building-standalone-executables)
- [Submitting a Pull Request](#-submitting-a-pull-request)

---

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainer.

---

## 💡 How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check existing [Issues](https://github.com/iamdulanga/file-organizer-pro/issues) to ensure the issue has not already been reported.

When creating a bug report, please include as much detail as possible:
* **Operating System & Version** (e.g., Windows 11 23H2, macOS 14 Sonoma, Ubuntu 22.04 LTS).
* **Python version** (e.g., `python --version` if running from source) or executable version.
* **Steps to Reproduce**: Clear, step-by-step instructions.
* **Expected vs. Actual Behavior**: What did you expect to happen, and what happened instead?
* **Log Output**: Check `~/file_organizer.log` (in your user home directory) and attach relevant log messages.
* **Screenshots**: If applicable, visual captures of UI errors or anomalies.

### Suggesting Enhancements

Feature requests are very welcome! When opening an issue for an enhancement, please describe:
* The problem you are trying to solve.
* Your proposed solution or desired feature.
* Any alternative solutions you've considered.

### Adding File Categories or Extensions

If you want to add support for new file extensions:
1. Locate `get_category_rules()` in `file_organizer.py`.
2. Ensure the extension belongs to the appropriate category, starts with a dot (`.`), and is in lowercase (e.g., `".webp"`).
3. If introducing a new category, ensure it is mirrored in the documentation and website (`index.html`).

### Pull Requests

We actively review pull requests. Please follow these simple steps:
1. Keep PRs focused on a single change or feature.
2. Ensure the code conforms to our coding standards.
3. Verify that all existing functionality (scanning, moving, collision renaming, undo, cancellation) continues to work properly.

---

## 💻 Development Setup

### Prerequisites

* **Python**: Version 3.10 or higher.
* **Tkinter**: Bundled with standard Python installers on Windows and macOS. On Debian/Ubuntu Linux, install via:
  ```bash
  sudo apt-get install python3-tk
  ```
* **Git**: Installed and configured on your system.

> [!NOTE]
> File Organizer Pro intentionally relies exclusively on Python standard library modules (`tkinter`, `pathlib`, `shutil`, `threading`, `queue`, `logging`, `dataclasses`). **Do not introduce heavy third-party dependencies** for the core sorting engine without prior discussion.

### Getting the Code

1. Fork the repository on GitHub: [https://github.com/iamdulanga/file-organizer-pro/fork](https://github.com/iamdulanga/file-organizer-pro/fork)
2. Clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/file-organizer-pro.git
   cd file-organizer-pro
   ```
3. Create a descriptive branch for your work:
   ```bash
   git checkout -b feature/my-new-feature
   # or
   git checkout -b fix/issue-description
   ```

### Running Locally

Run the application directly using Python:

```bash
# Windows
python file_organizer.py

# macOS / Linux
python3 file_organizer.py
```

---

## 📐 Code Style & Architecture Guidelines

* **PEP 8**: Follow standard Python code style guidelines.
* **Type Annotations**: Use Python type hints where applicable (`Dict`, `List`, `Path`, `Tuple`, etc.).
* **Non-Blocking Architecture**: Never perform file I/O or long-running scans directly on the main Tkinter thread. Always use `threading.Thread` and communicate back to the UI via `self.msg_queue`.
* **Zero Data Loss Guarantee**: Always preserve the collision protection behavior:
  * Never overwrite existing files.
  * Use `_generate_unique_destination()` for conflicts.
* **Self-Protection**: Always ensure the app itself and project files (`PROJECT_PROTECTED_FILES`) are excluded from organization.
* **Cross-Platform Compatibility**: Do not use OS-specific hardcoded paths. Always use `pathlib.Path`.

---

## 🧪 Testing Your Changes

Before submitting your changes, perform manual verification:
1. **Empty Folder**: Test organizing an empty directory; ensure an appropriate notice is shown.
2. **Duplicate Files**: Test sorting files where identical filenames already exist in the target subfolder; ensure files are indexed as `name (1).ext` without overwriting.
3. **Undo Operation**: Sort a test folder and trigger "Undo Last Action"; ensure all files are cleanly restored and empty category directories are pruned.
4. **Cancel Operation**: Organize a large test folder and hit "Cancel"; ensure the operation halts safely and partial moves can still be undone.
5. **Protected Files**: Place a test file named `file_organizer.py` or `readme.md` in the target folder; verify it is safely skipped.

---

## 📦 Building Standalone Executables

If you make changes to build scripts or want to verify standalone binaries:

```bash
# Install PyInstaller
pip install pyinstaller

# Windows
build_exe.bat
# Output: dist/FileOrganizer.exe

# macOS
chmod +x build_mac.sh && ./build_mac.sh
# Output: dist/FileOrganizer-macOS.zip

# Linux
chmod +x build_linux.sh && ./build_linux.sh
# Output: dist/FileOrganizer-Linux-x64.tar.gz
```

---

## 🚀 Submitting a Pull Request

1. Commit your changes with clear, concise commit messages:
   ```bash
   git add .
   git commit -m "feat: add support for .heic image extension"
   ```
2. Push your branch to GitHub:
   ```bash
   git push origin feature/my-new-feature
   ```
3. Open a Pull Request from your branch to `main` on the upstream repository.
4. Fill out the PR description with details of what was changed, why, and how it was tested.

Thank you for helping make File Organizer Pro better! ❤️

