import threading
import time
import json
import os
import sys
import subprocess
from audio_capture import AudioCapture
from AppKit import NSApplication, NSApplicationActivationPolicyAccessory, NSWorkspace, NSApplicationActivateIgnoringOtherApps

# PREVENT FOCUS STEALING: Make app an 'Accessory' (no dock icon, doesn't take focus)
try:
    NSApplication.sharedApplication().setActivationPolicy_(NSApplicationActivationPolicyAccessory)
except Exception as e:
    print(f"Warning: Could not set accessory policy: {e}")

from transcriber import Transcriber
from hotkey_monitor import HotkeyMonitor
from text_injector import TextInjector
from text_cleaner import TextCleaner
from ui import WisprFlowUI
import rumps

class WisprFlowApp:
    def __init__(self):
        print("\n\n" + "="*50)
        print("WISPR FLOW STARTING - v7 (CLEAN RESTORE)")
        print("="*50 + "\n")
        self.load_config()
        
        self.audio_capture = AudioCapture()
        self.text_injector = TextInjector()
        self.text_cleaner = TextCleaner()
        
        # UI needs to run in main thread, so we start other things in threads or callbacks
        self.ui = WisprFlowUI(
            on_start_recording=self.start_recording,
            on_stop_recording=self.stop_recording
        )
        
        self.ui.update_status(False, initializing=True)
        threading.Thread(target=self.init_transcriber).start()
        
        self.hotkey_monitor = HotkeyMonitor(
            on_press_callback=self.start_recording,
            on_release_callback=self.stop_recording,
            hotkey=self.config.get("hotkey", "ctrl_l")
        )
        
        self.is_processing = False

    def init_transcriber(self):
        print("Initializing Transcriber...")
        self.transcriber = Transcriber(model_size=self.config.get("model_size", "base"))
        print("Transcriber ready.")
        self.ui.update_status(False, initializing=False)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller/py2app """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def load_config(self):
        config_path = self.resource_path("config.json")
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
            print(f"Loaded config from {config_path}")
        except:
            print(f"Config not found at {config_path}, using defaults")
            self.config = {}

    def start_recording(self):
        if self.is_processing or not hasattr(self, 'transcriber') or not self.transcriber.model:
            print("Not ready to record.")
            return
            
        # Capture the currently active application (where user wants text)
        self.last_active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        print(f"Targeting app: {self.last_active_app.localizedName()}")
            
        print("Start recording requested")
        self.ui.update_status(True)
        self.audio_capture.start_recording()

    def stop_recording(self):
        print("Stop recording requested")
        self.ui.update_status(False)
        audio_file = self.audio_capture.stop_recording()
        
        if audio_file:
            # Process in a separate thread so UI doesn't freeze
            threading.Thread(target=self.process_audio, args=(audio_file,)).start()

    def run(self):
        print("Starting Hotkey Monitor...")
        # Start hotkey monitor in background
        self.hotkey_monitor.start()
        
        print("Starting UI Event Loop...")
        # Run UI in main thread
        self.ui.run()

    def _restore_focus_applescript(self, app_name):
        if not app_name:
            return
        
        print(f"Force-activating '{app_name}' via AppleScript...")
        try:
            script = f'tell application "{app_name}" to activate'
            subprocess.run(['osascript', '-e', script])
            time.sleep(0.2) # Wait for animation
        except Exception as e:
            print(f"AppleScript focus error: {e}")

    def process_audio(self, audio_file):
        self.is_processing = True
        print(f"Processing {audio_file}...")
        
        try:
            text = self.transcriber.transcribe(audio_file)
            if text:
                cleaned_text = self.text_cleaner.clean(text)
                print(f"Final text: {cleaned_text}")
                
                # RESTORE FOCUS explicitly to the target app
                if hasattr(self, 'last_active_app') and self.last_active_app:
                    app_name = self.last_active_app.localizedName()
                    self._restore_focus_applescript(app_name)
                
                self.text_injector.inject(cleaned_text)
        except Exception as e:
            print(f"Processing error: {e}")
        finally:
            self.is_processing = False
            # Clean up audio file
            try:
                os.remove(audio_file)
            except:
                pass

if __name__ == "__main__":
    app = WisprFlowApp()
    app.run()
