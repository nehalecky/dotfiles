#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "kokoro>=0.9.4",
#     "sounddevice",
# ]
# ///

"""
Kokoro TTS backend — local neural speech synthesis, no API key required.

Downloads the Kokoro-82M v1.0 model from Hugging Face on first run;
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


def main():
    text = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else "Task complete!"
    if not text:
        sys.exit(1)

    try:
        from kokoro import KPipeline
        import sounddevice as sd
        import numpy as np

        pipeline = KPipeline(lang_code="a")  # 'a' = American English
        voice = random.choice(_VOICES)

        samples = []
        for _, _, audio in pipeline(text, voice=voice, speed=1.0):
            samples.append(audio)

        if samples:
            audio_out = np.concatenate(samples)
            sd.play(audio_out, samplerate=24000)
            sd.wait()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
