import time
from AppKit import NSWorkspace
from pynput.keyboard import Controller

# Print active window
print("Switch to your target app (e.g. Notes) NOW! You have 3 seconds.")
time.sleep(3)

active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
print(f"Active App: {active_app.localizedName()}")

print("Typing 'Hello from test' in 2 seconds...")
time.sleep(2)

keyboard = Controller()
keyboard.type("Hello from test")
print("Done.")
