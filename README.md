# Acrylic Glass Music Player

A sleek, modern, and lightweight desktop music player built with Python and PySide6. Designed with an aesthetic-first approach, it features native Windows Acrylic glass transparency blur, a collapsible mini-player mode, and smart state management so your music never ruins your desktop workflow or aesthetic.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySide6](https://img.shields.io/badge/PySide6-Qt6-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

---

## 📋 Table of Contents
- [🖼️ Preview](#%EF%B8%8F-preview)
- [Key Features](#key-features)
- [Built With](#built-with)
- [Installation & Usage](#installation--usage)
  - [Option 1: Run the Executable (Recommended for End-Users)](#option-1-run-the-executable-recommended-for-end-users)
  - [Option 2: Run from Source (For Developers)](#option-2-run-from-source-for-developers)
  - [Building to .EXE](#building-to-exe)
- [⚠️ Windows Defender, SmartScreen & Smart App Control](#%EF%B8%8F-windows-defender-smartscreen--smart-app-control)
  - [Why does this happen?](#why-does-this-happen)
  - [How to Run the App (Bypass Defender & SAC)](#how-to-run-the-app-bypass-defender--sac)
  - [Creating a Local Self-Signed Certificate (Optional)](#creating-a-local-self-signed-certificate-optional)
  - [Solutions for Developers / Distribution](#solutions-for-developers--distribution)
- [📄 License](#-license)

---

## 🖼️ Preview

<img width="496" height="157" alt="image" src="https://github.com/user-attachments/assets/41a13ab2-785f-4a13-a116-f663d7d862b3" />
<img width="133" height="145" alt="image" src="https://github.com/user-attachments/assets/1ab48c75-599b-4a2a-9326-febe6c492921" />
<img width="547" height="310" alt="image" src="https://github.com/user-attachments/assets/100989ae-6cde-460f-a3a1-a34a10ac16a3" />

---

## Key Features

* **Aesthetic Acrylic Glass UI:** Native Windows blur effect with a translucent dark theme designed to blend seamlessly into modern desktop environments without cluttering your screen.
* **Collapsible Mini-Player:** Transforms into a compact, floating interactive disk and tray control panel that stays out of your way while you work.
* **Always-on-Top & Frameless Controls:** Stays accessible while remaining completely borderless and lightweight.
* **Embedded Metadata & Album Art:** Automatically extracts track titles and album cover art using Mutagen.
* **Smart State Memory:** Automatically remembers your last played folder, track index, and exact playback position so you can seamlessly resume where you left off.

---

## Built With

* **Python**
* **PySide6 (Qt for Python)** - For the high-performance GUI and multimedia handling.
* **Mutagen** - For parsing audio metadata and album art.
* **PyInstaller** - For compiling into a standalone executable.

---

## Installation & Usage

### Option 1: Run the Executable (Recommended for End-Users)
1. Go to the [Releases](../../releases) section of this repository.
2. Download the latest `player.exe`.
3. Double-click to launch—no Python installation required.

### Option 2: Run from Source (For Developers)
1. Clone this repository:
```bash
   git clone [https://github.com/itsvrtx/music_player.git](https://github.com/itsvrtx/music_player.git)
   cd music_player
```

2. Install the required dependencies:
```bash
pip install PySide6 mutagen
```

4. Run the application:
```bash
python player.py

```



### Building to .EXE

To compile the source code into a standalone executable with a custom icon, use PyInstaller:

```bash
pyinstaller --noconfirm --onefile --windowed --icon="logo.ico" "player.py"

```

---

## ⚠️ Windows Defender, SmartScreen & Smart App Control

When running the standalone executable (`.exe`) on Windows, you may encounter security prompts from **Windows SmartScreen**, **Windows Defender**, or **Smart App Control (SAC)** stating that the file is unknown or untrusted.

### Why does this happen?

This is a standard false positive. Because this application is compiled into a standalone `.exe` without an expensive commercial Code Signing Certificate, Windows automatically flags new or unrecognized executables as unknown until they build up global reputation.

---

### How to Run the App (Bypass Defender & SAC)

#### Option 1: Bypass SmartScreen (Quickest)

1. When the blue **"Windows protected your PC"** pop-up appears, click **"More info"**.
2. Click **"Run anyway"** at the bottom right.

#### Option 2: Unblock the File

1. Right-click the `.exe` file and select **Properties**.
2. Under the **General** tab, look at the bottom section labeled **Security**.
3. Check the box next to **Unblock**.
4. Click **Apply** -> **OK**, then double-click the file to launch.

#### Option 3: Bypass Smart App Control (SAC)

Windows 11 Smart App Control may block the `.exe` without displaying a "Run anyway" option:

1. Open **Start** -> Search for **Windows Security**.
2. Go to **App & browser control** -> **Smart App Control settings**.
3. Toggle Smart App Control to **Evaluation** mode or turn it **Off**.
*(Alternatively, unblocking the file via **Properties** as shown in Option 2 will allow it to run in most environments).*

#### Option 4: Add an Exclusion in Windows Defender

If Windows Defender actively blocks, flags, or quarantines the file:

1. Open **Start** -> Search for **Windows Security**.
2. Go to **Virus & threat protection**.
3. Under **Virus & threat protection settings**, click **Manage settings**.
4. Scroll down to **Exclusions** and click **Add or remove exclusions**.
5. Click **Add an exclusion** -> **File** (or **Folder**), and select your application `.exe` or folder.

---

### Creating a Local Self-Signed Certificate (Optional)

If you are compiling or running the app locally, you can create and sign the executable with a self-signed certificate to prevent repeated Windows Security prompts on your machine.

> **Note:** A self-signed certificate trusts the application on your local machine only. Other PCs will still require unblocking unless they trust your local root authority.

1. **Generate the Certificate in PowerShell (Run as Administrator):**
```powershell
New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=AcrylicMusicPlayer" -CertStoreLocation "Cert:\CurrentUser\My"

```


2. **Export to a `.pfx` File:**
```powershell
$cert = Get-ChildItem -Path Cert:\CurrentUser\My \vert{} Where-Object {$_.Subject -like "*AcrylicMusicPlayer*" }
$password = ConvertTo-SecureString -String "YourPassword123" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "my_cert.pfx" -Password $password

```


3. **Sign the Executable using `signtool`:**
*(Included with Windows SDK or Visual Studio Build Tools)*
```cmd
signtool sign /f "my_cert.pfx" /p "YourPassword123" /fd SHA256 "dist\player.exe"

```



---

### Solutions for Developers / Distribution

If you are distributing this app to other users:

* **Submit a False Positive Report:** Submit your executable to the [Microsoft Security Intelligence Portal](https://www.microsoft.com/en-us/wdsi/filesubmission) as a software developer. Microsoft usually verifies clean files within a few hours.
* **Package with an Installer:** Wrapping the executable with **Inno Setup** or **NSIS** helps reduce heuristic flags.
* **Digital Code Signing:** Sign the `.exe` using an **OV/EV Code Signing Certificate** with `signtool`.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](https://www.google.com/search?q=LICENSE) for more information.

---
