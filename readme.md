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

1.  **Download** the latest `PalworldEOSFix.exe` from the [Releases](https://github.com/deafdudecomputers/PalworldEOSFix/releases) page.
2.  **Run as Administrator** (required to modify registry and system shell settings).
3.  **Keep the window open** while launching Palworld.
4.  Join multiplayer normally.

---

## ⚠️ Important Notes

* **Registry Changes:** This modifies Windows registry settings.
* **Mod Uninstallation:** This **will remove** your Palworld mods and injected files to ensure a clean EOS handshake.
* **Workflow Impact:** If you rely on redirected Documents for enterprise or NAS workflows, this tool will override those settings while active.
* **Antivirus:** If Windows blocks it, click **"More Info"** -> **"Run Anyway"** (False positive due to Registry repair).

---

## 🔍 Visual Error Guide (Which fix do I need?)

<details>
<summary><b>❌ EOS Activation / Login Timeout Errors</b></summary>

<img width="608" height="302" alt="EOS Activation Error" src="https://github.com/user-attachments/assets/b711c8c3-8a22-4f53-ab3e-3f21b89ff3d5" />
<img width="605" height="309" alt="EOS Login Timeout" src="https://github.com/user-attachments/assets/bb658fd0-e5e2-4b73-9016-cd29301c7b17" />

**The Cause:** This typically means your Documents path was misconfigured. This tool will reset the Documents path to the correct local directory on your behalf.
</details>

<details>
<summary><b>❌ Connection Timed Out</b></summary>

<img width="972" height="478" alt="image" src="https://github.com/user-attachments/assets/81622145-0f06-455e-ad9d-e442948aab81" />

**The Cause:** This typically occurs due to outdated mods. Because mods often persist even after a clean uninstallation and reinstallation, they usually require manual removal. This tool will automatically identify and remove all mods on your behalf.
</details>

<details>
<summary><b>❌ Pal Crash Reporter</b></summary>

<img width="746" height="600" alt="image" src="https://github.com/user-attachments/assets/439801c1-978e-4f6f-9269-02f1d8f01ba3" />

**The Cause:** Often caused by outdated mods or corrupted saves. If the error persists after using this fix to clear your mods, your save file may be corrupted. Refer to the [Save Cleaning Tool](https://github.com/deafdudecomputers/PalworldSaveTools/releases/latest) for further assistance.
</details>

---

## 📄 License

This project is licensed under the **MIT License**.