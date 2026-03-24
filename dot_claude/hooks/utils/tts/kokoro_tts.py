#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "kokoro-onnx>=0.4.0",
#     "huggingface_hub",
#     "sounddevice",
# ]
# ///

"""
Kokoro TTS backend — local neural speech synthesis, no API key required.

Downloads the Kokoro-82M ONNX model (~90MB) from Hugging Face on first run;
subsequent runs use the local HF cache. Produces higher-quality, more varied
speech than macOS `say`.

Usage:
    ./kokoro_tts.py "Text to speak"
"""

import random
import sys

_VOICES = [
    "af_heart",
    "af_bella",
    "af_sky",
    "am_adam",
    "am_michael",
]

_REPO_ID = "hexgrad/Kokoro-82M"
_MODEL_FILE = "kokoro-v0_19.onnx"
_VOICES_FILE = "voices.bin"


def main():
    text = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else "Task complete!"
    if not text:
        sys.exit(1)

    try:
        from huggingface_hub import hf_hub_download
        from kokoro_onnx import Kokoro
        import sounddevice as sd

        model_path = hf_hub_download(repo_id=_REPO_ID, filename=_MODEL_FILE)
        voices_path = hf_hub_download(repo_id=_REPO_ID, filename=_VOICES_FILE)

        kokoro = Kokoro(model_path, voices_path)
        voice = random.choice(_VOICES)
        samples, sample_rate = kokoro.create(text, voice=voice, speed=1.0, lang="en-us")

        sd.play(samples, sample_rate)
        sd.wait()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
