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

Voice is controlled by the KOKORO_VOICE environment variable.
Default: af_heart (warm American female, closest to "Her" aesthetic).

American female: af_heart, af_bella, af_sky, af_nova, af_sarah
British female:  bf_emma, bf_alice, bf_isabella, bf_lily

Usage:
    ./kokoro_tts.py "Text to speak"
    KOKORO_VOICE=bf_emma ./kokoro_tts.py "Text to speak"
"""

import os
import sys

_DEFAULT_VOICE = "af_heart"

# lang_code is determined by voice prefix: a=American, b=British
_LANG_CODE = {"a": "a", "b": "b"}


def main():
    text = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else "Task complete!"
    if not text:
        sys.exit(1)

    try:
        from kokoro import KPipeline
        import sounddevice as sd
        import numpy as np

        voice = os.getenv("KOKORO_VOICE", _DEFAULT_VOICE)
        lang_code = _LANG_CODE.get(voice[0], "a")  # derive from voice prefix

        pipeline = KPipeline(lang_code=lang_code)

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
