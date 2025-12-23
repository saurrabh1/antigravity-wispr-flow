from pynput import keyboard
import threading
import time

class HotkeyMonitor:
    def __init__(self, on_press_callback, on_release_callback, hotkey='ctrl_l'):
        self.on_press_callback = on_press_callback
        self.on_release_callback = on_release_callback
        self.listener = None
        self.hotkey_char = keyboard.Key.ctrl_l # Default default
        
        if hotkey == 'cmd':
            self.hotkey_char = keyboard.Key.cmd
        elif hotkey == 'alt':
            self.hotkey_char = keyboard.Key.alt
        
        self.is_pressed = False

    def start(self):
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        print("Hotkey monitor started.")

    def stop(self):
        if self.listener:
            self.listener.stop()

    def _on_press(self, key):
        if key == self.hotkey_char:
            if not self.is_pressed:
                self.is_pressed = True
                self.on_press_callback()

    def _on_release(self, key):
        if key == self.hotkey_char:
            if self.is_pressed:
                self.is_pressed = False
                self.on_release_callback()
