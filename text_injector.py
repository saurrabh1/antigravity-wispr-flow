import Quartz
import time
from AppKit import NSPasteboard, NSStringPboardType

class TextInjector:
    def inject(self, text):
        if not text:
            return

        print(f"Injecting text via Clipboard: {text}")
        
        # 1. Get the general pasteboard
        pb = NSPasteboard.generalPasteboard()
        
        # 2. Save current contents (optional/advanced, skipping for speed/MVp)
        # 3. Clear and set new string
        pb.clearContents()
        pb.setString_forType_(text, NSStringPboardType)
        
        # 4. Simulate Command+V (Paste)
        self._send_cmd_v()
            
    def _send_cmd_v(self):
        # Create Command key down event
        cmd_down = Quartz.CGEventCreateKeyboardEvent(None, 0x37, True) # 0x37 is Command
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, cmd_down)
        
        # Create 'V' key down event
        v_down = Quartz.CGEventCreateKeyboardEvent(None, 0x09, True) # 0x09 is 'v'
        Quartz.CGEventSetFlags(v_down, Quartz.kCGEventFlagMaskCommand) # Add Command flag
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, v_down)
        
        # Create 'V' key up event
        v_up = Quartz.CGEventCreateKeyboardEvent(None, 0x09, False)
        Quartz.CGEventSetFlags(v_up, Quartz.kCGEventFlagMaskCommand)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, v_up)
        
        # Create Command key up event
        cmd_up = Quartz.CGEventCreateKeyboardEvent(None, 0x37, False)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, cmd_up)

