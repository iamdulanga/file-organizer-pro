// ---------------------------------------------------------------------------
// File Organizer Pro — Interactive Showcase & Auto OS Detection
// ---------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
    initOSDetection();
    initDropdown();
    initInteractiveDemo();
});

// ---------------------------------------------------------------------------
// 1. Operating System Auto-Detection
// ---------------------------------------------------------------------------
function initOSDetection() {
    const downloadBtn = document.getElementById('primary-download-btn');
    const downloadLabel = document.getElementById('download-label');
    const downloadSubtext = document.getElementById('download-subtext');
    const osIcon = document.getElementById('os-icon');

    const userAgent = window.navigator.userAgent.toLowerCase();
    const platform = window.navigator.userAgentData?.platform?.toLowerCase() || window.navigator.platform?.toLowerCase() || '';

    const RELEASES_BASE = "https://github.com/iamdulanga/file-organizer-pro/releases/latest";

    // Icons
    const windowsIconSvg = `
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M0 3.449L9.75 2.1v9.451H0m10.949-9.602L24 0v11.4H10.949M0 12.6h9.75v9.451L0 20.699M10.949 12.6H24V24l-12.9-1.801"/>
        </svg>
    `;

    const appleIconSvg = `
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.61-.75 1.04-1.8 0.92-2.85-.9.04-2 .6-2.63 1.34-.56.64-1.04 1.71-.91 2.74 1.01.08 2.02-.48 2.62-1.23z"/>
        </svg>
    `;

    const linuxIconSvg = `
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M12 2a5 5 0 0 0-5 5v3a5 5 0 0 0 10 0V7a5 5 0 0 0-5-5zm0 14c-4.42 0-8 2.24-8 5v1h16v-1c0-2.76-3.58-5-8-5z"/>
        </svg>
    `;

    if (platform.includes('mac') || userAgent.includes('macintosh') || userAgent.includes('mac os x')) {
        downloadLabel.textContent = "Download for macOS";
        downloadSubtext.textContent = "Standalone .zip • Native Apple App";
        osIcon.innerHTML = appleIconSvg;
        downloadBtn.href = `${RELEASES_BASE}`;
    } else if (platform.includes('linux') || userAgent.includes('linux') || userAgent.includes('x11')) {
        downloadLabel.textContent = "Download for Linux";
        downloadSubtext.textContent = "Standalone .tar.gz • Universal Binary";
        osIcon.innerHTML = linuxIconSvg;
        downloadBtn.href = `${RELEASES_BASE}`;
    } else {
        // Default to Windows
        downloadLabel.textContent = "Download for Windows";
        downloadSubtext.textContent = "Standalone .exe • No install required";
        osIcon.innerHTML = windowsIconSvg;
        downloadBtn.href = `${RELEASES_BASE}`;
    }
}

// ---------------------------------------------------------------------------
// 2. Dropdown Menu for Alternative OS
// ---------------------------------------------------------------------------
function initDropdown() {
    const dropdownBtn = document.getElementById('os-dropdown-btn');
    const dropdownMenu = document.getElementById('os-menu');

    if (!dropdownBtn || !dropdownMenu) return;

    dropdownBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownMenu.classList.toggle('show');
    });

    document.addEventListener('click', () => {
        dropdownMenu.classList.remove('show');
    });
}

// ---------------------------------------------------------------------------
// 3. Interactive Desktop Simulator Demo
// ---------------------------------------------------------------------------
function initInteractiveDemo() {
    const organizeBtn = document.getElementById('demo-organize-btn');
    const undoBtn = document.getElementById('demo-undo-btn');
    const resetBtn = document.getElementById('demo-reset-btn');

    const statusLabel = document.getElementById('demo-status');
    const percentLabel = document.getElementById('demo-percent');
    const progressBar = document.getElementById('demo-progress-bar');
    const detailsLabel = document.getElementById('demo-details');
    const chips = Array.from(document.querySelectorAll('.mock-file-chip'));

    const initialFiles = [
        { name: 'design_mockup.png', category: 'Images', icon: '🖼️' },
        { name: 'financial_report.pdf', category: 'Documents', icon: '📄' },
        { name: 'screencast_demo.mp4', category: 'Videos', icon: '🎬' },
        { name: 'podcast_episode.mp3', category: 'Music', icon: '🎵' },
        { name: 'backup_data.zip', category: 'Archives', icon: '📦' },
        { name: 'automation_task.py', category: 'Code', icon: '💻' }
    ];

    let isOrganizing = false;

    organizeBtn.addEventListener('click', () => {
        if (isOrganizing) return;
        isOrganizing = true;
        organizeBtn.disabled = true;
        undoBtn.disabled = true;

        statusLabel.textContent = "Scanning directory...";
        detailsLabel.textContent = "Found 6 candidate files to sort...";

        let step = 0;
        const total = chips.length;

        const interval = setInterval(() => {
            if (step < total) {
                const chip = chips[step];
                const fileInfo = initialFiles[step];
                const pct = Math.round(((step + 1) / total) * 100);

                // Update UI state
                progressBar.style.width = `${pct}%`;
                percentLabel.textContent = `${pct}%`;
                statusLabel.textContent = `Organizing (${step + 1}/${total})...`;
                detailsLabel.textContent = `Moved ${fileInfo.name} → ${fileInfo.category}/`;

                // Animate chip
                chip.classList.add('organized');
                const nameSpan = chip.querySelector('.file-name');
                nameSpan.textContent = `${fileInfo.category}/${fileInfo.name}`;

                step++;
            } else {
                clearInterval(interval);
                isOrganizing = false;
                organizeBtn.disabled = true;
                undoBtn.disabled = false;
                statusLabel.textContent = "Finished! 6 files organized.";
                detailsLabel.textContent = "All files safely categorized. 0 errors.";
            }
        }, 380);
    });

    undoBtn.addEventListener('click', () => {
        if (isOrganizing) return;
        
        chips.forEach((chip, i) => {
            chip.classList.remove('organized');
            const nameSpan = chip.querySelector('.file-name');
            nameSpan.textContent = initialFiles[i].name;
        });

        progressBar.style.width = "0%";
        percentLabel.textContent = "0%";
        statusLabel.textContent = "Undo completed";
        detailsLabel.textContent = "6 files restored back to original folder.";

        organizeBtn.disabled = false;
        undoBtn.disabled = true;
    });

    resetBtn.addEventListener('click', () => {
        chips.forEach((chip, i) => {
            chip.classList.remove('organized');
            const nameSpan = chip.querySelector('.file-name');
            nameSpan.textContent = initialFiles[i].name;
        });

        progressBar.style.width = "0%";
        percentLabel.textContent = "0%";
        statusLabel.textContent = "Ready to organize";
        detailsLabel.textContent = "Click 'Organize' below to test the live simulator";

        organizeBtn.disabled = false;
        undoBtn.disabled = true;
    });
}
