# Step1: Create API keys

# Step2: Create Client and send request
# from deepgram import DeepgramClient
import os
from pathlib import Path
import pyttsx3

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DOCTOR_AUDIO = BASE_DIR / "doctor_response.mp3"

def convert_text_to_doctor_audio(text, output_filepath="doctor_response.wav"):

    output_path = Path(output_filepath).resolve()
    engine = pyttsx3.init()
    engine.save_to_file(str(text), str(output_path))
    engine.runAndWait()
    engine.stop()

    if not output_path.exists():
        raise RuntimeError("Audio generation failed")

    return str(output_path)

import platform
import subprocess

def play_audio(audio_filepath):
    audio_filepath = str(audio_filepath)

    if platform.system() == "Darwin":
        subprocess.run(["afplay", audio_filepath], check=False)
    elif platform.system() == "Windows":
        os.startfile(audio_filepath)
    else:
        subprocess.run(["xdg-open", audio_filepath], check=False)
