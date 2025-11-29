from typing import Annotated
import mimetypes
import requests
from google import genai
from google.genai import types  # <- for Part.from_bytes

API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY or GEMINI_API_KEY environment variable")

client = genai.Client(api_key=API_KEY)

def transcribe_audio(url: Annotated[str, "URL of the audio file"]) -> str:
    """
    Download an audio file from the given URL and return its transcript
    using Gemini's audio capabilities. Do NOT guess, always transcribe.
    """

    # 1. Download audio bytes
    resp = requests.get(url)
    resp.raise_for_status()
    audio_bytes = resp.content

    # 2. Guess MIME type (mp3/wav) from URL or fallback to audio/mpeg
    mime, _ = mimetypes.guess_type(url)
    if mime is None:
        mime = "audio/mpeg"  # safe default for mp3-ish

    # 3. Initialize Gemini client (uses GOOGLE_API_KEY or GEMINI_API_KEY from env)
    client = genai.Client()

    # 4. Build audio part from bytes
    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime)

    # 5. Ask Gemini to TRANSCRIBE, not summarize
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # same family as the rest of your project
        contents=[
            # Prompt: tell it to give only transcript with numbers as digits
            "Transcribe this audio. "
            "Return only the raw transcript of what is spoken, with any numbers written as digits.",
            audio_part,
        ],
    )

    # 6. Extract plain text
    try:
        transcript = response.text
    except AttributeError:
        # Fallback if shape is slightly different
        transcript = response.candidates[0].content.parts[0].text

    return transcript
