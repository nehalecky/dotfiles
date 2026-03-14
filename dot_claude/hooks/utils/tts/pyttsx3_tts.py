#!/usr/bin/env python3
"""
macOS say TTS Script

Uses macOS built-in `say` command for high-quality speech synthesis.
Replaced pyttsx3 which used the older, robotic NSSpeechSynthesizer API.

Usage:
- ./pyttsx3_tts.py                    # Uses default text
- ./pyttsx3_tts.py "Your custom text" # Uses provided text
"""

import sys
import random
import subprocess


def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        completion_messages = [
            "Work complete!",
            "All done!",
            "Task finished!",
            "Job complete!",
            "Ready for next task!"
        ]
        text = random.choice(completion_messages)

    try:
        subprocess.run(["say", text], check=True, capture_output=True)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
