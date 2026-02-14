#!/usr/bin/env python3
"""
MacOS Supported
Voice-to-Claude Code with Global Hotkeys
Right shift (or configured hotkey) to start/stop recording
Transcription is automatically sent to Claude Code
"""

import subprocess
import os
import sys
import signal
from pathlib import Path
from pynput import keyboard
import pyautogui

# Configuration
MODEL_NAME = "large-v3-turbo"
MODEL_PATH = Path.home() / ".whisper_models" / f"ggml-{MODEL_NAME}.bin"
WHISPER_BIN = "whisper-cli"
TEMP_AUDIO = "/tmp/voice_raw.wav"
CONVERTED_AUDIO = "/tmp/voice_16k.wav"

# Language Configuration
# Set to specific language code or "auto" for auto-detection
# Top languages: en, es, fr, de, it, pt, zh, ja, ru, hr (Croatian)
LANGUAGE = "hr"  # Default: English

# Hotkey configuration - Change this to your preferred key
# Options: keyboard.Key.shift_r (right Shift), keyboard.Key.shift_l (left Shift)
HOTKEY = keyboard.Key.shift_r

# State
recording = False
rec_process = None


def download_model_if_needed():
    """Download Whisper model if not present"""
    if not MODEL_PATH.exists():
        print("📥 Downloading Whisper model...")
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        url = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin"
        subprocess.run(["curl", "-L", url, "-o", str(MODEL_PATH)], check=True)
        print("✅ Model downloaded")


def start_recording():
    """Start audio recording"""
    global recording, rec_process

    if recording:
        return

    print("🔴 Recording started... (Press hotkey again to stop)")
    recording = True

    rec_process = subprocess.Popen(
        ["rec", "-q", TEMP_AUDIO, "remix", "1"],
        stderr=subprocess.DEVNULL
    )


def stop_recording():
    """Stop recording and process transcription"""
    global recording, rec_process

    if not recording or rec_process is None:
        return

    print("⏹️  Recording stopped. Processing...")
    recording = False

    rec_process.terminate()
    rec_process.wait()
    rec_process = None

    # Convert to 16kHz mono
    subprocess.run(
        ["sox", TEMP_AUDIO, "-r", "16000", "-c", "1", "-b", "16", CONVERTED_AUDIO],
        stderr=subprocess.DEVNULL,
        check=True
    )

    whisper_cmd = [WHISPER_BIN, "-m", str(MODEL_PATH), "-f", CONVERTED_AUDIO, "-nt", "-p", "4"]

    if LANGUAGE != "auto":
        whisper_cmd.extend(["-l", LANGUAGE])

    result = subprocess.run(
        whisper_cmd,
        capture_output=True,
        text=True
    )

    transcription = result.stdout.strip()

    import re
    clean_text = re.sub(r'\[.*?\]', '', transcription).strip()
    clean_text = ' '.join(clean_text.split())

    if clean_text and clean_text != "null":
        print(f"🗣️  {clean_text}")
        send_text_to_cursor_or_clipboard(clean_text)
    else:
        print("⚠️  No speech detected")

    # Cleanup
    for f in [TEMP_AUDIO, CONVERTED_AUDIO]:
        if os.path.exists(f):
            os.remove(f)


def send_text_to_cursor_or_clipboard(text):
    """
    Sends transcription to the current cursor position using pyautogui,
    and also copies it to the clipboard as a fallback.
    """
    try:
        pyautogui.write(text)
        print("✅ Sent to cursor.")
    except Exception as e:
        print(f"⚠️  Could not send to cursor: {e}. Copying to clipboard instead.")
    
    # Always copy to clipboard as a reliable fallback/alternative
    subprocess.run(["pbcopy"], input=text.encode(), check=True)
    print("📋 Copied to clipboard.")


def on_press(key):
    """Handle key press events"""
    global recording

    if key == HOTKEY:
        if not recording:
            start_recording()
        else:
            stop_recording()


def cleanup(signum=None, frame=None):
    """Cleanup on exit"""
    global rec_process

    if rec_process is not None:
        rec_process.terminate()
        rec_process.wait()

    for f in [TEMP_AUDIO, CONVERTED_AUDIO]:
        if os.path.exists(f):
            os.remove(f)

    print("\n👋 Stopped")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    download_model_if_needed()

    print("🎙️  Voice-to-Text via Cursor/Clipboard Ready")
    print("Press Right Shift ⇧ to start/stop recording")
    print("Ctrl+C to quit\n")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
