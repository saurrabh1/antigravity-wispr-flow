import pyaudio
import wave
import tempfile
import threading
import time
import os

class AudioCapture:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.temp_filename = None

    def start_recording(self):
        if self.is_recording:
            return

        self.frames = []
        self.is_recording = True
        
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024,
                stream_callback=self._callback
            )
            self.stream.start_stream()
            print("Recording started...")
        except Exception as e:
            print(f"Error starting recording: {e}")
            self.is_recording = False

    def _callback(self, in_data, frame_count, time_info, status):
        if self.is_recording:
            self.frames.append(in_data)
            return (in_data, pyaudio.paContinue)
        return (in_data, pyaudio.paComplete)

    def stop_recording(self):
        if not self.is_recording:
            return None

        print("Stopping recording...")
        self.is_recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        return self._save_audio()

    def _save_audio(self):
        if not self.frames:
            return None

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        self.temp_filename = temp_file.name
        
        with wave.open(self.temp_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(self.frames))
            
        print(f"Audio saved to {self.temp_filename}")
        return self.temp_filename

    def cleanup(self):
        if self.temp_filename and os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)
        self.audio.terminate()
