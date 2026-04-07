import sys
import os


# Add project root to Python path to allow imports like:
# from app.services.audio_service import transcribe_audio
sys.path.append(os.path.abspath("."))

from app.services.audio_service import transcribe_audio

if __name__ == "__main__":

    # Path to the test audio file
    # Make sure this file exists before running the script
    audio_file = "tests/sample.wav"

     # Call the transcription service
    text = transcribe_audio(audio_file)

    print("Transcription:")
    print(text)