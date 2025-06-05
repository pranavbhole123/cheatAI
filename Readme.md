# CheatAI

> **“Fuck OA’s Relevel—may the best candidate be selected.”**

---

## 🚀 Introduction

**CheatAI** is a powerful system designed to bypass any browser-based proctoring for online assessments. By running coordinated scripts inside a Windows virtual machine (VM) and displaying answers on an undetectable overlay in your host OS, CheatAI ensures that your responses remain hidden from any screen-capture or monitoring tools running within the VM.

---

## 🔍 What It Is

* **`client.py`**: Executes inside a Windows VM and captures screenshots when prompted.
* **`combined.py`**: Executes on your host OS, intercepting screenshot data and rendering answers on a semi-transparent, toggleable overlay.

The overlay is:

* **Undetectable** by VM-based screen-capture or sharing.
* **Semi-transparent**, so it never obstructs your view.
* **Toggleable** using the <kbd>Esc</kbd> key.

---

## 🎯 How It Works

1. **Boot a Windows VM**

   * Download an ISO image of any Windows operating system from the official Microsoft website.
   * Create a new VM in your virtualization software (VirtualBox, VMware, etc.) using the downloaded ISO.

2. **Inside the VM: Run `client.py`**

   * This script listens for a specific keypress (e.g., <kbd>Print Screen</kbd>).
   * When triggered, it captures the VM’s screen and sends the image data to the host.

3. **On Your Host OS: Run `combined.py`**

   * Receives screenshot data from the VM.
   * Extracts answers (via OCR or a predefined lookup).
   * Displays answers on a floating, semi-transparent overlay positioned over the VM window.
   * Because the overlay is rendered outside the VM, it is invisible to any monitoring software inside the VM.

4. **Toggle the Overlay Visibility**

   * Press <kbd>Esc</kbd> to show or hide the answer overlay instantly.

---

## 📝 Requirements

* **Virtualization Software**

  * VirtualBox, VMware, or any VM platform capable of running a Windows ISO.
* **Windows ISO**

  * Download from Microsoft’s official site (e.g., Windows 10, Windows 11).
* **Python 3.x** installed on both host and guest (VM).
* **Python Packages** (install via `pip`):

  ```
  pillow
  opencv-python
  keyboard
  pygetwindow
  pywin32
  numpy
  ```

---

## ⚙️ Installation & Setup

1. **Clone the Repository Locally**

   ```bash
   git clone https://github.com/pranavbhole123/cheatAI.git
   cd cheatAI
   ```

2. **Inside the Windows VM**

   * Copy or clone the same repository into your VM’s filesystem.
   * Ensure Python 3.x is installed.
   * Install dependencies:

     ```bash
     pip install pillow opencv-python keyboard pygetwindow pywin32 numpy
     ```
   * Run:

     ```bash
     python client.py
     ```

3. **On Your Host OS**

   * From the same project directory, install dependencies (if not already done):

     ```bash
     pip install pillow opencv-python keyboard pygetwindow pywin32 numpy
     ```
   * Run:

     ```bash
     python combined.py
     ```

---

## 💡 Usage

1. **Launch Your VM**

   * Start Windows in your VM.
   * Ensure `client.py` is running and ready to capture screenshots.

2. **Start the Host Script**

   * Switch back to your host OS.
   * Launch `combined.py` before beginning the assessment.

3. **During the Assessment**

   * Press <kbd>Print Screen</kbd> (or your configured key) inside the VM.
   * CheatAI processes the screenshot on the host and renders answers on the semi-transparent overlay.
   * The overlay cannot be recorded or detected inside the VM.

4. **Toggle Visibility**

   * Press <kbd>Esc</kbd> to show or hide the overlay at any time.

---

## 🔥 Features

* **Stealth Mode**: Overlay is invisible to any VM-based screen capture.
* **Real-Time Answers**: Processes screenshots on-the-fly and displays answers instantly.
* **Easy Toggle**: Press <kbd>Esc</kbd> to show or hide the overlay.
* **Cross-Platform Support**: Client script runs inside any Windows VM; host script runs on any OS with Python 3.x.

---

## ⚠️ Disclaimer

* This software is provided **“as-is”** without any warranty.
* Use at your own risk.
* The author is not responsible for any consequences arising from misuse.

---

## 🤖 License

Feel free to clone, modify, or redistribute for educational or personal use only.
