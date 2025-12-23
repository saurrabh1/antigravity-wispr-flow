import rumps

class WisprFlowUI(rumps.App):
    def __init__(self, on_start_recording, on_stop_recording):
        super(WisprFlowUI, self).__init__("Wispr", icon=None)
        self.on_start_recording = on_start_recording
        self.on_stop_recording = on_stop_recording
        self.is_recording = False
        self.menu = ["Status: Ready", "Quit"]
        self.title = "🎤"

    def update_status(self, recording, initializing=False):
        if initializing:
            self.title = "⏳"
            self.menu["Status: Ready"].title = "Status: Loading Model..."
            return

        self.is_recording = recording
        if recording:
            self.title = "🔴"
            self.menu["Status: Ready"].title = "Status: Recording..."
        else:
            self.title = "🎤"
            self.menu["Status: Ready"].title = "Status: Ready"

    @rumps.clicked("Quit")
    def quit(self, _):
        rumps.quit_application()
