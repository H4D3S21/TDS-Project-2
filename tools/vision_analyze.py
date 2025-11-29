from typing import Annotated
import mimetypes
import requests
from google import genai
from google.genai import types

def vision_analyze(
    url: Annotated[str, "URL of the image (chart, screenshot, etc.)"],
    prompt: Annotated[str, "Exact question to ask about the image"],
) -> str:
    """
    Download an image and analyze it with Gemini Vision.
    Returns ONLY the answer text.
    """
    resp = requests.get(url)
    resp.raise_for_status()
    img_bytes = resp.content

    mime, _ = mimetypes.guess_type(url)
    if mime is None:
        mime = "image/png"

    client = genai.Client()
    img_part = types.Part.from_bytes(data=img_bytes, mime_type=mime)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            prompt,
            img_part,
        ],
    )

    try:
        return response.text.strip()
    except AttributeError:
        return response.candidates[0].content.parts[0].text.strip()
