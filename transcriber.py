import whisper
import os

class Transcriber:
    def __init__(self, model_size="base"):
        print(f"Loading Whisper model: {model_size}...")
        try:
            self.model = whisper.load_model(model_size)
            print("Whisper model loaded successfully.")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            self.model = None

    def transcribe(self, audio_file_path):
        if not self.model:
            print("Model not loaded.")
            return None
        
        if not os.path.exists(audio_file_path):
            print(f"Audio file not found: {audio_file_path}")
            return None

        print(f"Transcribing {audio_file_path}...")
        try:
            result = self.model.transcribe(audio_file_path)
            text = result["text"].strip()
            print(f"Transcription: {text}")
            return text
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None
