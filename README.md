# AI Skin Specialist

A local Gradio application that transcribes a voice description with Whisper and
uses Gemini to provide general information from a skin image or video. It is not
a medical diagnostic tool.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- A Gemini API key

## Setup

From the project directory, install the locked dependencies:

```powershell
uv sync
```

Copy `.env.example` to `.env` and add your Gemini API key:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace the example value for `GEMINI_API_KEY`.

## Run

```powershell
uv run ai-skindoctor
```

Open the local URL printed by Gradio (normally `http://127.0.0.1:7860`). You can
also start the app with `uv run python main.py`.

## Deploy to Vercel

Import the GitHub repository into Vercel and set `GEMINI_API_KEY` in the
project's environment variables. Keep the project root at the repository root;
Vercel uses `main.py`, which exposes the Gradio interface as a FastAPI app.

The microphone recording is transcribed locally. The image and/or video is sent
to the Gemini API for analysis; uploaded video files are deleted from Gemini
after the request. Do not submit media unless you have permission to share it.
The first voice analysis downloads the Whisper `base` model and may take longer.
For diagnosis or urgent symptoms, contact a licensed healthcare professional.
