import os
import sys
import shutil
import logging
import threading
import queue
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ---------------------------------------------------------------------------
# High-DPI Scaling (Windows)
# ---------------------------------------------------------------------------
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------
LOG_FILE_PATH = Path.home() / "file_organizer.log"

logging.basicConfig(
    filename=str(LOG_FILE_PATH),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------
@dataclass
class MoveRecord:
    original_path: Path
    new_path: Path

# ---------------------------------------------------------------------------
# File Organizer Logic & GUI
# ---------------------------------------------------------------------------
class FileOrganizerApp:
    # Operating system specific files and directories to ignore
    SYSTEM_FILES = {
        "desktop.ini", "thumbs.db", "iconcache.db",       # Windows
        ".ds_store", ".localized",                        # macOS
        ".directory"                                      # Linux
    }

    # Core project files to protect from being organized
    PROJECT_PROTECTED_FILES = {
        "file_organizer.py", "build_exe.bat", "build_mac.sh", "build_linux.sh",
        "readme.md", ".gitignore", "fileorganizer.exe", "fileorganizer"
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("File Organizer Pro")
        self.root.geometry("680x520")
        self.root.minsize(620, 480)

        # State variables
        default_folder = str(Path.home() / "Downloads")
        self.directory = tk.StringVar(value=default_folder if Path(default_folder).exists() else str(Path.home()))
        self.status_var = tk.StringVar(value="Ready to organize files")
        self.percent_var = tk.StringVar(value="0%")
        self.details_var = tk.StringVar(value="")
        self.is_processing = False
        self.cancel_requested = False
        self.history: List[List[MoveRecord]] = []
        self.msg_queue: queue.Queue = queue.Queue()

        self.rules = self.get_category_rules()

        self.apply_theme()
        self.build_ui()
        self.poll_queue()

    @staticmethod
    def get_category_rules() -> Dict[str, List[str]]:
        return {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff", ".ico", ".webp", ".heif", ".avif"],
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".ppt", ".xls", ".xlsx", ".csv", ".rtf", ".odt", ".ods", ".odp"],
            "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".opus"],
            "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".mpeg", ".3gp"],
            "Archives": [".zip", ".rar", ".tar", ".gz", ".7z", ".bz2", ".xz", ".cab", ".iso"],
            "Scripts": [".py", ".js", ".sh", ".bat", ".rb", ".php", ".pl", ".lua", ".swift", ".ps1"],
            "Executables": [".exe", ".msi", ".dmg", ".apk", ".appimage"],
            "Source Code": [".c", ".cpp", ".h", ".hpp", ".java", ".cs", ".go", ".ts", ".rs", ".kt", ".dart", ".html", ".css", ".json", ".xml", ".sql"],
            "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
            "Disk Images": [".img", ".bin", ".vhd", ".vmdk"],
            "Databases": [".sqlite", ".db", ".mdb", ".accdb"],
            "3D Models": [".obj", ".stl", ".fbx", ".gltf", ".blend"],
            "Torrents": [".torrent"],
            "Others": []
        }

    def _get_system_font(self) -> str:
        if sys.platform == "darwin":
            return "Helvetica Neue"
        elif sys.platform == "win32":
            return "Segoe UI"
        else:
            return "DejaVu Sans"

    def apply_theme(self):
        style = ttk.Style(self.root)
        available_themes = style.theme_names()

        if sys.platform == "darwin" and "aqua" in available_themes:
            style.theme_use("aqua")
        elif sys.platform == "win32" and "vista" in available_themes:
            style.theme_use("vista")
        elif "clam" in available_themes:
            style.theme_use("clam")

        font_family = self._get_system_font()
        bg_main = "#F3F4F6"
        self.root.configure(bg=bg_main)

        # Custom ttk styles
        style.configure("Header.TLabel", font=(font_family, 16, "bold"), background=bg_main, foreground="#111827")
        style.configure("Subheader.TLabel", font=(font_family, 9), background=bg_main, foreground="#6B7280")
        style.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        style.configure("CardHeader.TLabel", font=(font_family, 10, "bold"), background="#FFFFFF", foreground="#374151")
        style.configure("CardText.TLabel", font=(font_family, 9), background="#FFFFFF", foreground="#4B5563")
        style.configure("Status.TLabel", font=(font_family, 9, "bold"), background="#FFFFFF", foreground="#2563EB")
        style.configure("Percent.TLabel", font=(font_family, 9, "bold"), background="#FFFFFF", foreground="#4B5563")

    def build_ui(self):
        font_family = self._get_system_font()
        main_container = tk.Frame(self.root, bg="#F3F4F6", padx=20, pady=16)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = tk.Frame(main_container, bg="#F3F4F6")
        header_frame.pack(fill=tk.X, pady=(0, 14))

        title_label = ttk.Label(header_frame, text="File Organizer Pro", style="Header.TLabel")
        title_label.pack(anchor=tk.W)

        subtitle_label = ttk.Label(
            header_frame,
            text="Clean, sort, and organize folders into categorized directories safely and automatically.",
            style="Subheader.TLabel"
        )
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))

        # Folder Selection Card
        dir_card = tk.Frame(main_container, bg="#FFFFFF", padx=16, pady=14)
        dir_card.configure(highlightbackground="#E5E7EB", highlightcolor="#E5E7EB", highlightthickness=1, bd=0)
        dir_card.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(dir_card, text="Target Directory", style="CardHeader.TLabel").pack(anchor=tk.W, pady=(0, 6))

        dir_input_frame = tk.Frame(dir_card, bg="#FFFFFF")
        dir_input_frame.pack(fill=tk.X)

        self.dir_entry = ttk.Entry(dir_input_frame, textvariable=self.directory, font=(font_family, 9))
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        browse_btn = tk.Button(
            dir_input_frame,
            text="Browse...",
            command=self.browse_directory,
            bg="#F3F4F6",
            fg="#1F2937",
            activebackground="#E5E7EB",
            font=(font_family, 9),
            relief="groove",
            bd=1,
            padx=12,
            pady=4,
            cursor="hand2"
        )
        browse_btn.pack(side=tk.RIGHT)

        # Progress & Status Card
        progress_card = tk.Frame(main_container, bg="#FFFFFF", padx=16, pady=14)
        progress_card.configure(highlightbackground="#E5E7EB", highlightcolor="#E5E7EB", highlightthickness=1, bd=0)
        progress_card.pack(fill=tk.X, pady=(0, 14))

        status_header_frame = tk.Frame(progress_card, bg="#FFFFFF")
        status_header_frame.pack(fill=tk.X, pady=(0, 6))

        status_lbl = ttk.Label(status_header_frame, textvariable=self.status_var, style="Status.TLabel")
        status_lbl.pack(side=tk.LEFT)

        percent_lbl = ttk.Label(status_header_frame, textvariable=self.percent_var, style="Percent.TLabel")
        percent_lbl.pack(side=tk.RIGHT)

        self.progress_bar = ttk.Progressbar(progress_card, orient=tk.HORIZONTAL, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=(0, 6))

        details_lbl = ttk.Label(progress_card, textvariable=self.details_var, style="CardText.TLabel")
        details_lbl.pack(anchor=tk.W)

        # Action Buttons Area
        btn_frame = tk.Frame(main_container, bg="#F3F4F6")
        btn_frame.pack(fill=tk.X, pady=(0, 14))

        self.organize_btn = tk.Button(
            btn_frame,
            text="Organize Files",
            command=self.start_organize,
            bg="#2563EB",
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            font=(font_family, 10, "bold"),
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2"
        )
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.cancel_organize,
            bg="#EF4444",
            fg="#FFFFFF",
            activebackground="#DC2626",
            activeforeground="#FFFFFF",
            font=(font_family, 9, "bold"),
            relief="flat",
            padx=12,
            pady=8,
            state=tk.DISABLED,
            cursor="arrow"
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.undo_btn = tk.Button(
            btn_frame,
            text="Undo Last Action",
            command=self.undo_last_action,
            bg="#F97316",
            fg="#FFFFFF",
            activebackground="#EA580C",
            activeforeground="#FFFFFF",
            font=(font_family, 9, "bold"),
            relief="flat",
            padx=12,
            pady=8,
            state=tk.DISABLED,
            cursor="arrow"
        )
        self.undo_btn.pack(side=tk.LEFT, padx=(0, 8))

        log_btn = tk.Button(
            btn_frame,
            text="View Log",
            command=self.open_log_file,
            bg="#E5E7EB",
            fg="#374151",
            activebackground="#D1D5DB",
            font=(font_family, 9),
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        log_btn.pack(side=tk.LEFT, padx=(0, 8))

        exit_btn = tk.Button(
            btn_frame,
            text="Exit",
            command=self.root.quit,
            bg="#E5E7EB",
            fg="#374151",
            activebackground="#D1D5DB",
            font=(font_family, 9),
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2"
        )
        exit_btn.pack(side=tk.RIGHT)

        # Categories Overview Card
        cat_card = tk.Frame(main_container, bg="#FFFFFF", padx=16, pady=12)
        cat_card.configure(highlightbackground="#E5E7EB", highlightcolor="#E5E7EB", highlightthickness=1, bd=0)
        cat_card.pack(fill=tk.BOTH, expand=True)

        ttk.Label(cat_card, text="Supported Categories & Extensions", style="CardHeader.TLabel").pack(anchor=tk.W, pady=(0, 4))
        
        info_text = (
            "• Images (.jpg, .png, .webp, .svg, .gif)\n"
            "• Documents (.pdf, .docx, .txt, .xlsx, .pptx, .csv)\n"
            "• Music & Audio (.mp3, .wav, .flac, .aac, .m4a)\n"
            "• Videos (.mp4, .mkv, .mov, .avi, .webm)\n"
            "• Archives (.zip, .rar, .7z, .tar, .gz, .iso)\n"
            "• Scripts & Source Code (.py, .js, .ts, .java, .cpp, .sh, .bat)\n"
            "• Executables (.exe, .msi, .appimage, .dmg) & Others (unrecognized extensions)"
        )
        cat_info = tk.Label(cat_card, text=info_text, justify=tk.LEFT, font=(font_family, 8), bg="#FFFFFF", fg="#6B7280")
        cat_info.pack(anchor=tk.W)

    def browse_directory(self):
        chosen = filedialog.askdirectory(initialdir=self.directory.get() or str(Path.home()))
        if chosen:
            self.directory.set(chosen)
            self.status_var.set(f"Selected: {chosen}")
            self.details_var.set("")
            self.progress_bar["value"] = 0
            self.percent_var.set("0%")

    def _get_category_folder(self, extension: str) -> str:
        ext_lower = extension.lower()
        for category, extensions in self.rules.items():
            if ext_lower in extensions:
                return category
        return "Others"

    @staticmethod
    def _generate_unique_destination(dest_dir: Path, filename: str) -> Path:
        target = dest_dir / filename
        if not target.exists():
            return target

        stem = Path(filename).stem
        suffix = Path(filename).suffix
        counter = 1
        while True:
            candidate = dest_dir / f"{stem} ({counter}){suffix}"
            if not candidate.exists():
                return candidate
            counter += 1

    def start_organize(self):
        target_dir = Path(self.directory.get().strip())
        if not target_dir.exists() or not target_dir.is_dir():
            messagebox.showerror("Invalid Directory", "Please select a valid existing directory.")
            return

        self.is_processing = True
        self.cancel_requested = False
        self.set_ui_state(processing=True)
        self.status_var.set("Scanning directory...")
        self.details_var.set("Looking for files to organize...")
        self.progress_bar["value"] = 0
        self.percent_var.set("0%")

        worker = threading.Thread(target=self._organize_worker, args=(target_dir,), daemon=True)
        worker.start()

    def cancel_organize(self):
        if self.is_processing:
            self.cancel_requested = True
            self.status_var.set("Cancelling operation...")
            self.cancel_btn.config(state=tk.DISABLED)

    def _is_self_or_protected(self, item: Path) -> bool:
        """Self-protection: avoid moving the running app or core repo files."""
        name_lower = item.name.lower()
        if name_lower in self.PROJECT_PROTECTED_FILES:
            return True
        if name_lower.startswith("."):
            return True

        # Check against running executable/script path
        try:
            current_exec = Path(sys.executable).resolve()
            if item.resolve() == current_exec:
                return True
        except Exception:
            pass

        try:
            if "__file__" in globals():
                script_path = Path(__file__).resolve()
                if item.resolve() == script_path:
                    return True
        except Exception:
            pass

        return False

    def _organize_worker(self, target_dir: Path):
        logging.info(f"Starting organization for directory: {target_dir}")
        try:
            category_names = set(self.rules.keys())
            category_names.add("Others")

            candidate_files: List[Path] = []
            for item in target_dir.iterdir():
                try:
                    if item.is_file():
                        name_lower = item.name.lower()
                        if name_lower in self.SYSTEM_FILES or name_lower.startswith("._"):
                            logging.debug(f"Skipping system file: {item.name}")
                            continue

                        if self._is_self_or_protected(item):
                            logging.info(f"Skipping protected/self file: {item.name}")
                            continue

                        candidate_files.append(item)
                except (PermissionError, OSError) as e:
                    logging.warning(f"Error accessing item {item.name}: {e}")

            total_files = len(candidate_files)
            if total_files == 0:
                self.msg_queue.put(("empty", "No files found to organize in the selected folder."))
                return

            moved_records: List[MoveRecord] = []
            errors_count = 0

            for index, file_path in enumerate(candidate_files, start=1):
                if self.cancel_requested:
                    logging.info("Organization cancelled by user.")
                    self.msg_queue.put(("cancelled", moved_records))
                    return

                try:
                    category = self._get_category_folder(file_path.suffix)
                    category_dir = target_dir / category
                    category_dir.mkdir(exist_ok=True)

                    destination = self._generate_unique_destination(category_dir, file_path.name)
                    shutil.move(str(file_path), str(destination))
                    moved_records.append(MoveRecord(original_path=file_path, new_path=destination))
                    logging.info(f"Moved: {file_path.name} -> {category}/{destination.name}")

                except Exception as err:
                    errors_count += 1
                    logging.error(f"Failed to move {file_path.name}: {err}")

                self.msg_queue.put(("progress", index, total_files, file_path.name))

            self.msg_queue.put(("complete", moved_records, errors_count, total_files, target_dir))

        except Exception as e:
            logging.exception(f"Unexpected worker failure: {e}")
            self.msg_queue.put(("fatal_error", str(e)))

    def undo_last_action(self):
        if not self.history:
            messagebox.showinfo("Undo", "No previous actions available to undo.")
            return

        last_batch = self.history.pop()
        undone_count = 0
        error_count = 0
        touched_parents = set()

        for record in reversed(last_batch):
            try:
                if record.new_path.exists():
                    safe_restore = record.original_path
                    if safe_restore.exists():
                        safe_restore = self._generate_unique_destination(record.original_path.parent, record.original_path.name)
                    shutil.move(str(record.new_path), str(safe_restore))
                    undone_count += 1
                    touched_parents.add(record.new_path.parent)
                    logging.info(f"Undid move: {record.new_path} -> {safe_restore}")
            except Exception as err:
                error_count += 1
                logging.error(f"Error undoing {record.new_path}: {err}")

        # Clean up empty category folders if left behind
        for folder in touched_parents:
            try:
                if folder.is_dir() and not any(folder.iterdir()):
                    folder.rmdir()
                    logging.info(f"Removed empty category folder after undo: {folder.name}")
            except OSError:
                pass

        # Update Undo button state
        if not self.history:
            self.undo_btn.config(state=tk.DISABLED, cursor="arrow")

        self.status_var.set(f"Undo completed: {undone_count} file(s) restored.")
        self.details_var.set(f"Errors during undo: {error_count}" if error_count > 0 else "")
        messagebox.showinfo("Undo Finished", f"Restored {undone_count} file(s) back to their original location.")

    def open_log_file(self):
        if not LOG_FILE_PATH.exists():
            messagebox.showinfo("Log File", f"No log file has been created yet at:\n{LOG_FILE_PATH}")
            return
        try:
            if sys.platform == "win32":
                os.startfile(str(LOG_FILE_PATH))
            elif sys.platform == "darwin":
                subprocess.run(["open", str(LOG_FILE_PATH)], check=False)
            else:
                subprocess.run(["xdg-open", str(LOG_FILE_PATH)], check=False)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open log file: {e}")

    def poll_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                msg_type = msg[0]

                if msg_type == "progress":
                    _, current, total, filename = msg
                    pct = int((current / total) * 100)
                    self.progress_bar["value"] = pct
                    self.percent_var.set(f"{pct}%")
                    self.status_var.set(f"Organizing ({current}/{total})...")
                    self.details_var.set(f"Processing: {filename}")

                elif msg_type == "complete":
                    _, moved_records, errors, total, _ = msg
                    if moved_records:
                        self.history.append(moved_records)
                        self.undo_btn.config(state=tk.NORMAL, cursor="hand2")

                    self.progress_bar["value"] = 100
                    self.percent_var.set("100%")
                    success_count = len(moved_records)
                    self.status_var.set(f"Finished! Organized {success_count} of {total} files.")
                    self.details_var.set(f"Errors encountered: {errors} (check log file for details)" if errors else "All files organized successfully.")
                    self.set_ui_state(processing=False)
                    messagebox.showinfo("Organization Complete", f"Successfully organized {success_count} file(s).\nErrors: {errors}")

                elif msg_type == "cancelled":
                    _, moved_records = msg
                    if moved_records:
                        self.history.append(moved_records)
                        self.undo_btn.config(state=tk.NORMAL, cursor="hand2")

                    self.status_var.set("Operation cancelled by user.")
                    self.details_var.set(f"Files organized before cancellation: {len(moved_records)}")
                    self.set_ui_state(processing=False)
                    messagebox.showwarning("Cancelled", f"Operation was cancelled.\n{len(moved_records)} files were organized before stopping.")

                elif msg_type == "empty":
                    _, message = msg
                    self.status_var.set(message)
                    self.details_var.set("")
                    self.progress_bar["value"] = 0
                    self.percent_var.set("0%")
                    self.set_ui_state(processing=False)
                    messagebox.showinfo("Nothing to Organize", message)

                elif msg_type == "fatal_error":
                    _, err_msg = msg
                    self.status_var.set("An unexpected error occurred.")
                    self.details_var.set(err_msg)
                    self.set_ui_state(processing=False)
                    messagebox.showerror("Error", f"Failed to organize directory:\n{err_msg}")

        except queue.Empty:
            pass

        self.root.after(100, self.poll_queue)

    def set_ui_state(self, processing: bool):
        self.is_processing = processing
        if processing:
            self.organize_btn.config(state=tk.DISABLED, cursor="arrow")
            self.cancel_btn.config(state=tk.NORMAL, cursor="hand2")
            self.dir_entry.config(state=tk.DISABLED)
        else:
            self.organize_btn.config(state=tk.NORMAL, cursor="hand2")
            self.cancel_btn.config(state=tk.DISABLED, cursor="arrow")
            self.dir_entry.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
