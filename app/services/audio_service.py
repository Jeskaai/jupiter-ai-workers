import whisper
import os

# Load Whisper model once at startup to avoid reloading on every request
# This improves performance significantly in production environments
model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes an audio file using OpenAI Whisper.

    This service is designed to support:
    - filler word detection
    - speech speed analysis
    - vocabulary analysis
    """

    # Validate that the audio file exists before processing
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

  
    try:
        # Perform transcription using Whisper
        result = model.transcribe(audio_path)

         # Return clean text output (remove leading/trailing spaces)
        return result["text"].strip()
        
 # Return clean text output (remove leading/trailing spaces)
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""