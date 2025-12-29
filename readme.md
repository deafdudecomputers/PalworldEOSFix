# PalworldEOSFix

A Windows GUI utility designed to resolve **Epic Online Services (EOS)** login failures and Co-op connection issues in Palworld. This tool enforces a local Documents folder, synchronizes system time, removes conflicting mods, and handles file locks by automatically managing the game process.

---

## 🛠️ The Problem

Many Palworld players encounter errors such as `ULoginEOSAsyncFunction::Activate() Failed`, `EOS Login Timeout`, or generic Connection Timeouts. These issues typically occur because:

1.  **Folder Redirection:** Palworld and EOS require the Documents folder to be on a local NTFS disk. Cloud services like OneDrive often redirect this to a network path (UNC), breaking the handshake.
2.  **Clock Desync:** If your system time is out of sync by even a few minutes, SSL/TLS encryption handshakes fail, preventing players from joining Co-op sessions.
3.  **Persistent Mods:** Outdated mods or injectors (UE4SS) often remain in the game directory even after a "clean" reinstall, causing crashes or connection drops.
4.  **File Locks:** Attempting to fix these environment variables while the game is running often fails because the game holds active handles on the registry and folders.

---

## ✨ Features

This tool provides a **clean-slate environment** for Palworld to launch into:

* **GUI-Driven Interface:** A clean, dark-themed Windows interface for manual or automated fixes.
* **Automatic Game Management:** Automatically detects and terminates `Palworld-Win64-Shipping.exe` before applying fixes to ensure registry and folder changes are accepted.
* **Registry Enforcement:** Forces the Windows Documents shell folder back to a local `%USERPROFILE%\Documents` path.
* **Time Synchronization:** Forces a Windows Time sync (`w32tm`) to fix P2P handshake failures caused by clock drift.
* **Mod Purging:** Deep-cleans the `Mods` directory, `UE4SS` injectors, `dwmapi.dll` hooks, and all non-core `.pak` files.
* **Silent Execution:** Runs without a flashing console window; all operations are performed in the background with real-time feedback in the GUI.
* **Audit Logging:** Live UI logging and persistent file logging to `documents_eos_audit.log`.

---

## ⚙️ Technical Overview

### 1. Smart Process Termination
Using PowerShell-based detection, the tool identifies even elevated game processes. It performs a "Tree Kill" (`taskkill /T`) to ensure the launcher and the game binary are fully closed before modifying the environment.

### 2. Shell Folder Correction
The script updates `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders`, resetting the `Personal` value and broadcasting shell change notifications via `SHChangeNotify` to update Windows Explorer instantly.

### 3. Conflict Removal
The script locates the Steam installation path via the registry and wipes the `Pal\Binaries\Win64` hooks and `Pal\Content\Paks` modifications, leaving only the official `pal-windows.pak`.

---

## 🚀 How To Use

1.  **Download** `PalworldEOSFix.exe` from the [Releases](https://github.com/deafdudecomputers/PalworldEOSFix/releases) page.
2.  **Run as Administrator** (required to modify registry, sync system time, and terminate elevated game processes).
3.  **Click the Fix Buttons:** Use the GUI to apply the necessary repairs. The game will automatically close if it is currently open.
4.  **Launch Palworld** via Steam once the log shows "Success."

---

## ⚠️ Important Notes

* **No Console Window:** The tool is a pure GUI application. If you see no window, check your Task Manager for `PalworldEOSFix.exe`.
* **Mod Uninstallation:** This **will remove** your mods. Back them up if you intend to keep them, though they are usually the cause of the connection error.
* **Antivirus:** Since the tool modifies the Registry and system time, Windows Defender may flag it. This is a false positive.

---

## 🔍 Visual Error Guide (Which fix do I need?)

<details>
<summary><b>❌ EOS Activation / Login Timeout Errors</b></summary>

<img width="608" height="302" alt="EOS Activation Error" src="https://github.com/user-attachments/assets/b711c8c3-8a22-4f53-ab3e-3f21b89ff3d5" />
<img width="605" height="309" alt="EOS Login Timeout" src="https://github.com/user-attachments/assets/bb658fd0-e5e2-4b73-9016-cd29301c7b17" />

**The Cause:** Typically a misconfigured Documents path (OneDrive/Network Share). Click **"Fix Documents Path"** to reset it.
</details>

<details>
<summary><b>❌ Connection Timed Out / Co-op Failures</b></summary>

<img width="972" height="478" alt="image" src="https://github.com/user-attachments/assets/81622145-0f06-455e-ad9d-e442948aab81" />

**The Cause:** Usually system clock desync or outdated mods. Click **"Sync System Time"** and **"Remove Mods"**.
</details>

---

## 📄 License

This project is licensed under the **MIT License**.