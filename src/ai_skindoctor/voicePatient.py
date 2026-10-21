
import logging
from io import BytesIO
from pathlib import Path

import speech_recognition as sr
from pydub import AudioSegment
from faster_whisper import WhisperModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

_model = None


def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        logging.info("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        logging.info("Start speaking now...")

        audio_data = recognizer.listen(
            source,
            timeout=timeout,
            phrase_time_limit=phrase_time_limit
        )

    wav_data = audio_data.get_wav_data()
    audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
    audio_segment.export(file_path, format="mp3", bitrate="128k")

    logging.info("Audio saved to %s", file_path)
    return file_path


def transcribe_patient_voice(audio_filepath):
    global _model

    audio_path = Path(audio_filepath)
    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if _model is None:
        _model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    segments, _ = _model.transcribe(str(audio_path))
    return " ".join(segment.text.strip() for segment in segments)
