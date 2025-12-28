# PalworldEOSFix

A Windows utility designed to resolve **Epic Online Services (EOS)** login failures in Palworld. This tool enforces a local Documents folder, removes conflicting mods, and acts as a continuous watchdog to prevent regressions that break multiplayer functionality.

---

## 🛠️ The Problem

Many Palworld players encounter errors such as `ULoginEOSAsyncFunction::Activate() Failed` or `EOS Login Timeout`. These issues typically occur because **Palworld (Unreal Engine) and EOS assume the Documents folder is on a local NTFS disk.**

Authentication often fails or times out when Documents are redirected to:
* A NAS or SMB share (UNC paths like `\\server\Documents`)
* OneDrive or other cloud-sync configurations
* Network-mapped drives

---

## ✨ Features

This is a **self-healing watchdog**, not a one-time patch. It actively restores and enforces the environment EOS expects:

* **Registry Enforcement:** Forces the Windows Documents shell folder back to a local `%USERPROFILE%` path.
* **Mod Purging:** Automatically cleans Palworld mods, injected DLLs (`dwmapi.dll`), and modified PAK files.
* **Cache Clearing:** Wipes Palworld/EOS AppData logs and configuration caches.
* **Continuous Watchdog:** Re-applies the fix every 60 seconds to prevent OneDrive or System Policies from reverting changes.
* **Audit Logging:** Live console output and file logging to `documents_eos_audit.log`.

---

## ⚙️ Technical Overview

### 1. Shell Folder Correction
The script monitors and updates the following registry key:  
`HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders`

It resets the `Personal` value to `%USERPROFILE%\Documents` and broadcasts shell change notifications so Windows recognizes the change immediately without a reboot.

### 2. Conflict Removal
The script locates the Palworld installation via the registry and deletes:
* The root `Mods` directory
* `UE4SS` injector folders
* Injected `dwmapi.dll` files
* All non-core `.pak` files

### 3. Loop Enforcement
Every 60 seconds, the utility verifies the path exists, re-applies the registry value, and logs the current status to ensure stability while the game is running.

---

## 🚀 How To Use

1.  **Download** or clone this repository.
2.  **Run as Administrator** (required to modify registry and system shell settings).
3.  **Keep the window open** while launching Palworld.
4.  Join multiplayer normally.

---

## ⚠️ Important Notes

* **Registry Changes:** This modifies Windows registry settings.
* **Mod Uninstallation:** This **will remove** your Palworld mods and injected files to ensure a clean EOS handshake.
* **Workflow Impact:** If you rely on redirected Documents for enterprise or NAS workflows, this tool will override those settings while active.
* **Windows Only:** Designed specifically for Windows environments.

### What This Does NOT Fix
* Official EOS server outages
* General internet connectivity issues
* Steam "Offline Mode" issues
* Corrupt save files or game version mismatches

---

## 📄 License

This project is licensed under the **MIT License**.