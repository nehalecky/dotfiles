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

from utils.common import append_to_log, build_service


def main():
    try:
        # Recursion guard: bail if we're inside a hook-generating subprocess.
        if os.getenv("_CLAUDE_HOOK_GENERATING"):
            sys.exit(0)

        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--notify', action='store_true', help='Enable TTS notifications')
        args = parser.parse_args()

        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())

        # Log the event
        log_dir = os.path.join(os.getcwd(), 'logs')
        append_to_log(os.path.join(log_dir, 'notification.json'), input_data)

        if args.notify:
            build_service().speak_notification(message=input_data.get('message'))

        sys.exit(0)

    except (json.JSONDecodeError, Exception):
        sys.exit(0)

if __name__ == '__main__':
    main()
