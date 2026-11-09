# Security Policy

The **File Organizer Pro** team takes the security, integrity, and privacy of your files and system very seriously. This document outlines our security policies, supported versions, and how to report any security vulnerabilities responsibly.

---

## 🛡️ Core Security Principles

File Organizer Pro is designed with safety and privacy at its core:

* **100% Offline & Zero Telemetry**: The application runs entirely locally on your computer. It performs zero external network requests, collects no analytics, and does not send any telemetry or file metadata to the cloud.
* **Non-Destructive Operations**: Built-in duplicate collision protection guarantees that files with identical names are never overwritten or deleted. Colliding files are automatically renamed with an indexed suffix (e.g., `file (1).ext`).
* **Self & Project Protection**: The application identifies and excludes itself, executables, scripts, and repository files from being moved or reorganized.
* **Controlled Scope**: Operations are strictly confined to the directory explicitly selected by the user. The app will never traverse or organize system folders without explicit target selection.

---

## 📦 Supported Versions

Security updates are actively applied to the latest stable release:

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.x.x   | :x:                |

We strongly encourage all users to always use the [latest release](https://github.com/iamdulanga/file-organizer-pro/releases/latest).

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability or have reason to believe you have found a potential security risk in File Organizer Pro, please report it **responsibly and privately**.

> [!CAUTION]
> **Please do not report security vulnerabilities through public GitHub issues, discussions, or social media.**

### How to Report Privately

1. **GitHub Security Advisory (Preferred)**:
   * Navigate to the [Security Advisories tab](https://github.com/iamdulanga/file-organizer-pro/security/advisories) on GitHub.
   * Click **"Report a vulnerability"** to open a private advisory draft.

2. **Direct Contact**:
   * Contact the maintainer **Dulanga Dasanayake** directly on GitHub at [@iamdulanga](https://github.com/iamdulanga).

### What to Include in Your Report

To help us investigate and resolve the issue quickly, please provide as much context as possible:
* A clear description of the vulnerability and its potential impact.
* Detailed, step-by-step instructions to reproduce the issue.
* A minimal proof of concept (PoC) or sample files/scripts, if applicable.
* Affected operating system(s) and version(s) (Windows, macOS, Linux).
* The application version or commit hash where the vulnerability was observed.

---

## ⏱️ Response & Disclosure Timeline

When a vulnerability is reported:

1. **Acknowledgment**: We will acknowledge receipt of your vulnerability report within **48 hours**.
2. **Investigation & Assessment**: We will verify the issue, assess its severity, and determine the scope of impact.
3. **Remediation**: We will prepare and test a fix across supported operating systems (Windows, macOS, Linux).
4. **Coordinated Disclosure**: Once a patch is released, we will publish a security advisory and credit the reporter (unless you request to remain anonymous).

---

Thank you for helping keep File Organizer Pro and its users safe! ❤️

