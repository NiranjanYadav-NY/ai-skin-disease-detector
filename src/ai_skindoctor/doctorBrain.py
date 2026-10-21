import mimetypes
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-2.5-flash"
VIDEO_PROCESSING_TIMEOUT = 180


def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to .env or your environment."
        )
    return genai.Client(api_key=api_key)


def _image_part(image_path: str | Path) -> types.Part:
    path = Path(image_path)
    mime_type, _ = mimetypes.guess_type(path.name)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Unsupported image file type: {path.name}")
    return types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_type)


def _wait_for_video(client: genai.Client, video_file: types.File) -> types.File:
    deadline = time.monotonic() + VIDEO_PROCESSING_TIMEOUT
    while video_file.state == types.FileState.PROCESSING:
        if time.monotonic() >= deadline:
            raise TimeoutError("Timed out while Gemini processed the uploaded video.")
        time.sleep(2)
        video_file = client.files.get(name=video_file.name)

    if video_file.state != types.FileState.ACTIVE:
        raise RuntimeError(f"Gemini could not process the uploaded video: {video_file.name}")
    return video_file


def brain_of_the_doctor(
    patient_text: str,
    image_filepath: str | Path | None = None,
    video_filepath: str | Path | None = None,
) -> str:
    if not image_filepath and not video_filepath:
        raise ValueError("Provide a skin image or video for analysis.")

    client = _get_client()
    contents: list[types.Part | types.File | str] = []
    if image_filepath:
        contents.append(_image_part(image_filepath))

    uploaded_video = None
    if video_filepath:
        uploaded_video = client.files.upload(file=str(video_filepath))

    try:
        if uploaded_video:
            uploaded_video = _wait_for_video(client, uploaded_video)
            contents.append(uploaded_video)

        contents.append(
            "You are an AI assistant providing general skin-health information, not a "
            "doctor. Review the supplied media and the patient's description. Explain "
            "what may be visible without claiming a definitive diagnosis, mention "
            "important uncertainty, and recommend seeing a licensed clinician for "
            "diagnosis or concerning symptoms. Do not prescribe medication.\n\n"
            f"Patient description: {patient_text}"
        )
        response = client.models.generate_content(model=MODEL, contents=contents)
        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")
        return response.text
    finally:
        if uploaded_video:
            client.files.delete(name=uploaded_video.name)
