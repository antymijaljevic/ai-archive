# Voice-to-Claude Code with Global Hotkeys

Record voice with a keyboard shortcut and automatically send transcriptions to Claude Code.

## Features

- 🎙️ **Global hotkey** to start/stop recording (default: Right Shift ⇧)
- 🤖 **Auto-transcription** using Whisper (offline, fast)
- 📝 **Auto-inserts** text to Claude Code in iTerm2 (without submitting - you can review first!)
- 🌍 **Multilingual** support for 99 languages (English default)
- 🔄 **Toggle recording** with the same key
- 🚀 **Works from any app** - no need to switch windows!

## Requirements

- macOS
- iTerm2
- SoX (`brew install sox`)
- whisper-cli (`brew install whisper-cpp`)
- Python 3.7+ (`python3 --version`)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Install system dependencies (if not already installed):**
   ```bash
   brew install sox whisper-cpp
   ```

3. **Grant Accessibility permissions:**
   - Go to **System Settings > Privacy & Security > Accessibility**
   - Add your terminal app (iTerm2, Terminal, etc.)
   - This allows the script to listen for global hotkeys

4. **Grant Microphone permissions:**
   - Go to **System Settings > Privacy & Security > Microphone**
   - Enable iTerm2 (or your terminal app)

5. **Make the script executable:**
   ```bash
   chmod +x stt_hotkey.py
   ```

## Usage

### Start the hotkey daemon:
```bash
./stt_hotkey.py
```

You should see:
```
🎙️  Voice-to-Claude Code Ready
Press Right Shift ⇧ to start/stop recording
Ctrl+C to quit
```

### Recording workflow:
1. Make sure Claude Code is running in iTerm2
2. Press **Right Shift** from ANY app
3. Speak your prompt
4. Press **Right Shift** again to stop and transcribe
5. Transcription is inserted into Claude Code (review it, then press Enter to submit)

### Stop the daemon:
Press **Ctrl+C** in the terminal running the script

## Customizing the Hotkey

Edit `stt_hotkey.py` and change the `HOTKEY` variable (line 25):

### Single key options:
```python
HOTKEY = keyboard.Key.shift_r  # Right Shift (default)
HOTKEY = keyboard.Key.shift_l  # Left Shift
HOTKEY = keyboard.Key.caps_lock  # Caps Lock
```

**Tip**: Right Shift is convenient because it's easy to reach and rarely used alone. If you need Right Shift for typing, consider using Caps Lock or F13-F19 keys instead.

## Language Configuration

The script supports 99 languages with **English as default**. Edit `stt_hotkey.py` and change the `LANGUAGE` variable (line 22):

### Top 10 supported languages:
```python
LANGUAGE = "en"    # 🇺🇸 English (default)
LANGUAGE = "es"    # 🇪🇸 Spanish
LANGUAGE = "fr"    # 🇫🇷 French
LANGUAGE = "de"    # 🇩🇪 German
LANGUAGE = "it"    # 🇮🇹 Italian
LANGUAGE = "pt"    # 🇵🇹 Portuguese
LANGUAGE = "zh"    # 🇨🇳 Chinese
LANGUAGE = "ja"    # 🇯🇵 Japanese
LANGUAGE = "ru"    # 🇷🇺 Russian
LANGUAGE = "hr"    # 🇭🇷 Croatian
LANGUAGE = "auto"  # 🌍 Auto-detect (works with any language)
```

**Note**: Setting a specific language improves accuracy for that language. Use `"auto"` for multilingual conversations.

## Running as Background Service

To run automatically on login, create a LaunchAgent:

1. **Create the plist file** (update YOUR_USERNAME and path):
   ```bash
   cat > ~/Library/LaunchAgents/com.user.stt-hotkey.plist << 'EOF'
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.user.stt-hotkey</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/local/bin/python3</string>
           <string>/Users/YOUR_USERNAME/repositories/toolbox/scripts/cluade-code-stt/stt_hotkey.py</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
       <key>StandardErrorPath</key>
       <string>/tmp/stt-hotkey.err</string>
       <key>StandardOutPath</key>
       <string>/tmp/stt-hotkey.out</string>
   </dict>
   </plist>
   EOF
   ```

2. **Load it**:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.user.stt-hotkey.plist
   ```

3. **Check if running**:
   ```bash
   launchctl list | grep stt-hotkey
   ```

## Troubleshooting

### "Accessibility permissions denied"
- Grant permissions in System Settings > Privacy & Security > Accessibility
- Restart terminal after granting permissions

### "No speech detected"
- Check microphone permissions (System Settings > Privacy & Security > Microphone)
- Speak louder or closer to microphone
- Test microphone: `rec test.wav` then `Ctrl+C`, then `play test.wav`

### Transcription not appearing in Claude Code
- Make sure iTerm2 window is open with Claude Code running
- Transcription is inserted (not auto-submitted) - press Enter to send
- Falls back to clipboard if iTerm2 not found
- Check console for errors

### Hotkey not working
- Ensure Accessibility permissions are granted
- Try a different key (F14, F15, etc.)
- Check if another app is using the same hotkey

## Files

- `stt_hotkey.py` - **NEW**: Main script with global hotkey support ⭐
- `stt.sh` - Original press-Enter version (still works)
- `requirements.txt` - Python dependencies

---