# WinSPY - Advanced Keylogger/Logger for Windows

> [!WARNING]
> THIS PROJECT SHOULD BE USED FOR AUTHORIZED TESTING OR EDUCATIONAL PURPOSES ONLY. YOU ARE FREE TO COPY, MODIFY AND REUSE THE SOURCE CODE AT YOUR OWN RISK.

### **Uses**

Some use cases for a keylogger and system monitor:

- Security Testing — improving protection against hidden keyloggers and monitoring software
- Business Administration — monitor what employees are doing (with their consent)
- School / Institutions — track keystrokes and log activity for authorized supervision
- Personal Control — make sure no one is using your computer when you are away
- Parental Control — track what your children are doing on a shared device
- Research & Self-analysis — study how input monitoring and system enumeration work at a low level

---

### Features

- Global keyboard event hook using pynput — captures all keystrokes including On-Screen Keyboard input
- Active window and process tracking — logs which application and window title was active at the time of each keystroke
- Multi-language keyboard layout support — correctly logs characters in their actual layout; Cyrillic keyboard layouts are fully implemented
- Layout transliteration — when switching layouts mid-session, characters are mapped back to their equivalent in the initial layout
- Full upper-/lowercase detection — correct character casing via Caps Lock state + Shift key tracking

---

**System monitoring running in parallel:**

  - Microphone audio recording (20 sec, stereo WAV)
  - Full multi-monitor screenshot capture
  - Windows systeminfo dump
  - Full hardware device enumeration via PowerShell
  - Parallel execution of all monitoring tasks via `multiprocessing.Pool`


---

## **Getting Started**

### System Requirements

- OS: Windows 10 / 11 only (Linux and macOS are not supported)
- Python: 3.10+ (tested on 3.14)


  Windows-only because WinSPY relies on ctypes.WinDLL, the Win32 API (win32gui, win32process, GetKeyboardLayout, GetKeyState), and PowerShell cmdlets (Get-PnpDevice) that do not exist on other platforms.


### **Installation**

```bash
git clone https://github.com/th0truth/WinSPY.git
cd WinSPY

pip install -r requirements.txt
```


### **Usage**

```bash
python main.py
```

---

### **License**

Distributed under the MIT license. See `LICENSE` for more information.