#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

from utils.common import append_to_log, build_service, copy_transcript_to_chat


def main():
    try:
        # Recursion guard: bail if we're inside a hook-generating subprocess.
        # Prevents infinite loop when claude -p fires its own Stop hook.
        if os.getenv("_CLAUDE_HOOK_GENERATING"):
            sys.exit(0)

        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true', help='Copy transcript to chat.json')
        parser.add_argument('--notify', action='store_true', help='Enable TTS completion announcement')
        args = parser.parse_args()

        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Log the event
        log_dir = os.path.join(os.path.expanduser("~"), ".claude", "logs")
        append_to_log(os.path.join(log_dir, "stop.json"), input_data)

        # Handle --chat switch
        if args.chat and 'transcript_path' in input_data:
            copy_transcript_to_chat(input_data['transcript_path'], log_dir)

        # Announce completion via TTS (only if --notify flag is set)
        if args.notify:
            build_service().speak_completion(transcript_path=input_data.get('transcript_path'))

        sys.exit(0)

    except (json.JSONDecodeError, Exception):
        sys.exit(0)


if __name__ == "__main__":
    main()
