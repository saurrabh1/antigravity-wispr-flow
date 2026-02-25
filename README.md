# Wispr Flow Clone (Local & Free) Made using Antigravity

[![Watch Demo Video](https://img.youtube.com/vi/vSL6EmNO-k8/0.jpg)](https://youtu.be/vSL6EmNO-k8)



This is a local macOS application that mimics the functionality of Wispr Flow. It allows you to dictate text into any application using a global hotkey (default: `Right Control`).

## Features
- **Global Hotkey:** Hold `Right Control` to record.
- **Local Transcription:** Uses OpenAI's Whisper model locally (no API keys, free forever).
- **Smart Injection:** Automatically pastes text into your focused application (Notes, Slack, Terminal, etc.).
- **Privacy First:** No audio leaves your machine.

## Prerequisites (For New Users)
To run this on a fresh Mac, you need:
1.  **Python 3.9+** installed.
2.  **Homebrew** installed (to install system dependencies).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd wispr_flow
    ```

2.  **Install System Dependencies:**
    Run this in your terminal to install audio and video libraries required by Whisper:
    ```bash
    brew install portaudio ffmpeg
    ```

3.  **Run the Setup Script:**
    We have provided a script that creates a virtual environment and installs all Python libraries automatically.
    *(You may need to make it executable first)*
    ```bash
    chmod +x start_wispr.command
    ./start_wispr.command
    ```
    *Note: The first run will take a few minutes to download the Whisper AI model (~500MB).*

## Critical First-Run Setup (Permissions)
Apple's security is strict. You **MUST** grant permissions for the app to hear you and type for you.

1.  **Microphone:** When you first record, macOS will ask to access the Microphone. Click **Allow**.
2.  **Accessibility (Typing):** When the app tries to paste text, you might see an error or a prompt.
    *   Go to **System Settings** -> **Privacy & Security** -> **Accessibility**.
    *   Find **Terminal** (or `iTerm`/`Python` depending on how you mistakenly ran it).
    *   **Toggle it ON**.
    *   *Pro Tip:* If it still fails, select the entry and click the `-` (minus) button to remove it, then restart the app to re-trigger the permission request.

## Configuration
You can edit `config.json` to change settings:
```json
{
    "hotkey": "ctrl_r",
    "model_size": "base"  // Options: tiny, base, small, medium (larger = more accurate but slower)
}
```

## Troubleshooting
- **App freezes on start:** It's likely downloading the model. Check your terminal output.
- **Text types in the terminal, not my app:** Make sure you clicked into your target app (e.g. Notes) *before* holding the hotkey.
- **"Process is not trusted":** This means you need to fix Accessibility permissions (see above).
