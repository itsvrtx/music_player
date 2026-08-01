# Acrylic Glass Music Player

A sleek, modern, and lightweight desktop music player built with Python and PySide6. Designed with an aesthetic-first approach, it features native Windows Acrylic glass transparency blur, a collapsible mini-player mode, and smart state management so your music never ruins your desktop workflow or aesthetic.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySide6](https://img.shields.io/badge/PySide6-Qt6-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

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
   git clone https://github.com/itsvrtx/music_player.git
   cd music_player

Install the required dependencies:
   ```bash
   pip install PySide6 mutagen
```
Run the application:

```bash
python player.py
```

Building to .EXE
To compile the source code into a standalone executable with a custom icon, use PyInstaller:

```bash
pyinstaller --noconfirm --onefile --windowed --icon="logo.ico" "player.py"
```

---

## ⚠️ Windows Defender / SmartScreen Warning

When running the standalone executable (`.exe`) on a new PC, Windows SmartScreen or Windows Defender may display a warning such as:
> *"Windows protected your PC"* or *"The app is dangerous / untrusted"*.

### Why does this happen?
This is a standard false positive. Because this application is packaged into a standalone `.exe` without an expensive commercial Code Signing Certificate, Windows automatically flags new or unrecognized executables as unknown until they build up reputation.

---

### How to Run the App (For Users)

#### Option 1: Bypass SmartScreen (Quickest)
1. When the blue **"Windows protected your PC"** pop-up appears, click **"More info"**.
2. Click **"Run anyway"** at the bottom right.

#### Option 2: Unblock the File
1. Right-click the `.exe` file and select **Properties**.
2. Under the **General** tab, look at the bottom section labeled **Security**.
3. Check the box next to **Unblock**.
4. Click **Apply** $\rightarrow$ **OK**, then double-click the file to launch.

#### Option 3: Add an Exclusion in Windows Defender
If Windows Defender actively blocks or quarantines the file:
1. Open **Start** $\rightarrow$ Search for **Windows Security**.
2. Go to **Virus & threat protection**.
3. Under **Virus & threat protection settings**, click **Manage settings**.
4. Scroll down to **Exclusions** and click **Add or remove exclusions**.
5. Click **Add an exclusion** $\rightarrow$ **File** (or **Folder**), and select your application `.exe` or folder.

---

### Solutions for Developers / Distribution

If you are distributing this app to other users:
* **Submit a False Positive Report:** Submit your executable to the [Microsoft Security Intelligence Portal](https://www.microsoft.com/en-us/wdsi/filesubmission) as a software developer. Microsoft usually verifies clean files within a few hours.
* **Package with an Installer:** Wrapping the executable with **Inno Setup** or **NSIS** helps reduce heuristic flags.
* **Digital Code Signing:** Sign the `.exe` using an **OV/EV Code Signing Certificate** with `signtool`.
