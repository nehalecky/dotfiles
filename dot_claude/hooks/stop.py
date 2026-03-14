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
import random
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_completion_messages():
    """Return list of friendly completion messages."""
    return [
        "Work complete!",
        "All done!",
        "Task finished!",
        "Job complete!",
        "Ready for next task!"
    ]


def get_tts_script_path():
    """
    Determine which TTS script to use based on available API keys.
    Priority order: ElevenLabs > OpenAI > pyttsx3
    """
    # Get current script directory and construct utils/tts path
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"
    
    # Check for ElevenLabs API key (highest priority)
    if os.getenv('ELEVENLABS_API_KEY'):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)
    
    # Check for OpenAI API key (second priority)
    if os.getenv('OPENAI_API_KEY'):
        openai_script = tts_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script)
    
    # Fall back to pyttsx3 (no API key required)
    pyttsx3_script = tts_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)
    
    return None


def _shorten_path(path):
    """Shorten an absolute path to ~/last/two/parts for readability."""
    short = path.replace(os.path.expanduser('~'), '~')
    parts = short.split('/')
    return '/'.join(parts[-2:]) if len(parts) > 2 else short


def extract_transcript_context(transcript_path, max_entries=60):
    """Build a rich 3-part context summary from recent transcript activity.

    Returns a string with up to three sections:
      Request: <last user message>
      Actions: <deduplicated tool calls with key inputs>
      Outcome: <last assistant text>
    """
    try:
        entries = []
        with open(transcript_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

        recent = entries[-max_entries:]

        last_user_message = None
        tool_actions = []       # ordered list of action strings
        seen_action_keys = {}   # key -> count, for deduplication
        last_assistant_text = None

        for entry in recent:
            etype = entry.get('type')

            # Capture the last real user text message (skip tool results)
            if etype == 'user' and not entry.get('toolUseResult'):
                content = entry.get('message', {}).get('content', '')
                if isinstance(content, str) and content.strip():
                    last_user_message = content.strip()[:200]
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get('type') == 'text':
                            text = block.get('text', '').strip()
                            if text:
                                last_user_message = text[:200]

            # Capture tool calls and assistant text from assistant entries
            elif etype == 'assistant':
                for block in entry.get('message', {}).get('content', []):
                    if not isinstance(block, dict):
                        continue
                    btype = block.get('type')

                    if btype == 'text':
                        text = block.get('text', '').strip()
                        if text:
                            last_assistant_text = text[:300]

                    elif btype == 'tool_use':
                        name = block.get('name', '')
                        inp = block.get('input', {})

                        if name in ('Edit', 'Write', 'Read', 'MultiEdit'):
                            short = _shorten_path(inp.get('file_path', ''))
                            key = f"{name}:{short}"
                            if key in seen_action_keys:
                                seen_action_keys[key] += 1
                            else:
                                seen_action_keys[key] = 1
                                tool_actions.append(f"{name} {short}")

                        elif name == 'Bash':
                            cmd = inp.get('command', '').split('\n')[0].strip()[:60]
                            key = f"Bash:{cmd[:30]}"
                            if key not in seen_action_keys:
                                seen_action_keys[key] = 1
                                tool_actions.append(f"Bash({cmd})")

                        elif name == 'Agent':
                            desc = inp.get('description', '')[:60]
                            tool_actions.append(f"Agent({desc})")

                        elif name in ('Glob', 'Grep', 'WebFetch', 'WebSearch'):
                            key = name
                            if key not in seen_action_keys:
                                seen_action_keys[key] = 1
                                tool_actions.append(name)

        parts = []
        if last_user_message:
            parts.append(f"Request: {last_user_message}")
        if tool_actions:
            parts.append(f"Actions: {', '.join(tool_actions[-8:])}")
        if last_assistant_text:
            parts.append(f"Outcome: {last_assistant_text}")

        if not parts:
            return None
        return '\n'.join(parts)[:800]

    except Exception:
        return None


def get_llm_completion_message(transcript_path=None):
    """
    Generate completion message using available LLM services.
    Priority order: OpenAI > Anthropic > Ollama > fallback to random message

    Returns:
        str: Generated or fallback completion message
    """
    # Extract context from transcript if available
    context = None
    if transcript_path and os.path.exists(transcript_path):
        context = extract_transcript_context(transcript_path)

    # Get current script directory and construct utils/llm path
    script_dir = Path(__file__).parent
    llm_dir = script_dir / "utils" / "llm"

    def run_llm(script_path):
        cmd = ["uv", "run", str(script_path), "--completion"]
        if context:
            cmd += ["--context", context]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass
        return None

    # Try OpenAI first (highest priority)
    if os.getenv('OPENAI_API_KEY'):
        oai_script = llm_dir / "oai.py"
        if oai_script.exists():
            msg = run_llm(oai_script)
            if msg:
                return msg

    # Try Anthropic second
    if os.getenv('ANTHROPIC_API_KEY'):
        anth_script = llm_dir / "anth.py"
        if anth_script.exists():
            msg = run_llm(anth_script)
            if msg:
                return msg

    # Try Ollama third (local LLM)
    ollama_script = llm_dir / "ollama.py"
    if ollama_script.exists():
        msg = run_llm(ollama_script)
        if msg:
            return msg

    # Fallback to random predefined message
    messages = get_completion_messages()
    return random.choice(messages)

def announce_completion(transcript_path=None):
    """Announce completion using the best available TTS service."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available

        # Get completion message (LLM-generated with context, or fallback)
        completion_message = get_llm_completion_message(transcript_path=transcript_path)
        
        # Call the TTS script with the completion message
        subprocess.run([
            "uv", "run", tts_script, completion_message
        ], 
        capture_output=True,  # Suppress output
        timeout=10  # 10-second timeout
        )
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true', help='Copy transcript to chat.json')
        parser.add_argument('--notify', action='store_true', help='Enable TTS completion announcement')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract required fields
        session_id = input_data.get("session_id", "")
        stop_hook_active = input_data.get("stop_hook_active", False)

        # Ensure log directory exists
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "stop.json")

        # Read existing log data or initialize empty list
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Handle --chat switch
        if args.chat and 'transcript_path' in input_data:
            transcript_path = input_data['transcript_path']
            if os.path.exists(transcript_path):
                # Read .jsonl file and convert to JSON array
                chat_data = []
                try:
                    with open(transcript_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    chat_data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    pass  # Skip invalid lines
                    
                    # Write to logs/chat.json
                    chat_file = os.path.join(log_dir, 'chat.json')
                    with open(chat_file, 'w') as f:
                        json.dump(chat_data, f, indent=2)
                except Exception:
                    pass  # Fail silently

        # Announce completion via TTS (only if --notify flag is set)
        if args.notify:
            announce_completion(transcript_path=input_data.get('transcript_path'))

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)


if __name__ == "__main__":
    main()
