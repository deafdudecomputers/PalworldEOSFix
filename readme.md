# PalworldEOSFix

A Windows utility designed to resolve **Epic Online Services (EOS)** login failures and Co-op connection issues in Palworld. This tool enforces a local Documents folder, synchronizes system time, removes conflicting mods, and acts as a continuous watchdog.

---

## 🛠️ The Problem

Many Palworld players encounter errors such as `ULoginEOSAsyncFunction::Activate() Failed`, `EOS Login Timeout`, or generic Connection Timeouts. These issues typically occur because:

1.  **Folder Redirection:** Palworld and EOS require the Documents folder to be on a local NTFS disk. Cloud services like OneDrive often redirect this to a network path, breaking the handshake.
2.  **Clock Desync:** If your system time (specifically the Host's clock) is out of sync by even a few minutes, SSL/TLS encryption handshakes fail, preventing friends from joining Co-op sessions.
3.  **Persistent Mods:** Outdated mods often remain in the game directory even after a "clean" reinstall, causing crashes or connection drops.

---

## ✨ Features

This is a **self-healing watchdog**, not a one-time patch. It actively restores and enforces the environment EOS expects:

* **Registry Enforcement:** Forces the Windows Documents shell folder back to a local `%USERPROFILE%` path.
* **Time Synchronization:** Automatically forces a Windows Time sync (`w32tm`) to ensure hosting and P2P handshakes don't fail due to clock drift.
* **Mod Purging:** Automatically cleans Palworld mods, injected DLLs (`dwmapi.dll`), and modified PAK files.
* **Cache Clearing:** Wipes Palworld/EOS AppData logs and configuration caches.
* **Continuous Watchdog:** Re-applies fixes every 60 seconds to prevent cloud services or system policies from reverting changes.
* **Audit Logging:** Live console output and file logging to `documents_eos_audit.log`.

---

## ⚙️ Technical Overview

### 1. Shell Folder Correction
The script monitors and updates `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders`, resetting the `Personal` value to `%USERPROFILE%\Documents` and broadcasting shell change notifications.

### 2. Time Sync
The tool executes `w32tm /resync /force` to align the local clock with internet time servers. This is critical for Co-op hosts; if the host's time is wrong, guests cannot join.

### 3. Conflict Removal
The script locates the Palworld installation via the registry and deletes the root `Mods` directory, `UE4SS` injector folders, injected `dwmapi.dll` files, and all non-core `.pak` files.

---

## 🚀 How To Use

1.  **Download** `PalworldEOSFix.exe` from the [Releases](https://github.com/deafdudecomputers/PalworldEOSFix/releases) page.
2.  **Run as Administrator** (required to modify registry and sync system time).
3.  **Keep the window open** while launching Palworld.
4.  Join or host multiplayer normally.

---

## ⚠️ Important Notes

* **Registry Changes:** This modifies Windows registry settings.
* **Mod Uninstallation:** This **will remove** your mods to ensure a clean EOS handshake.
* **Antivirus:** If Windows blocks it, click **"More Info"** -> **"Run Anyway"** (False positive due to Registry/Time repair).
* **Windows Only:** Designed specifically for Windows environments.

---

## 🔍 Visual Error Guide (Which fix do I need?)

<details>
<summary><b>❌ EOS Activation / Login Timeout Errors</b></summary>

<img width="608" height="302" alt="EOS Activation Error" src="https://github.com/user-attachments/assets/b711c8c3-8a22-4f53-ab3e-3f21b89ff3d5" />
<img width="605" height="309" alt="EOS Login Timeout" src="https://github.com/user-attachments/assets/bb658fd0-e5e2-4b73-9016-cd29301c7b17" />

**The Cause:** This typically means your Documents path was misconfigured. This tool will reset the Documents path to the correct local directory on your behalf.
</details>

<details>
<summary><b>❌ Connection Timed Out / Co-op Failures</b></summary>

<img width="972" height="478" alt="image" src="https://github.com/user-attachments/assets/81622145-0f06-455e-ad9d-e442948aab81" />

**The Cause:** Often occurs due to outdated mods OR system clock desync. If you are hosting and your clock is wrong, friends cannot join. This tool cleans mods and syncs your clock automatically.
</details>

<details>
<summary><b>❌ Pal Crash Reporter</b></summary>

<img width="746" height="600" alt="image" src="https://github.com/user-attachments/assets/439801c1-978e-4f6f-9269-02f1d8f01ba3" />

**The Cause:** Persistent mods or corrupted saves. If the error persists after using this fix to clear mods, your save file may be corrupted. Refer to the [Save Cleaning Tool](https://github.com/deafdudecomputers/PalworldSaveTools/releases/latest) for further assistance.
</details>

---

## 📄 License

This project is licensed under the **MIT License**.