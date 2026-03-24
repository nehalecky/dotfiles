"""Common utilities for Claude Code hook notification system.

Provides Backend, TranscriptParser, NotificationService, and log helpers
to eliminate duplicated logic across stop.py, notification.py, and
subagent_stop.py hook scripts.
"""

import json
import os
import random
import subprocess
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


FALLBACK_MESSAGES = [
    "Work complete!",
    "All done!",
    "Task finished!",
    "Job complete!",
    "Ready for next task!",
]

_GENERIC_NOTIFICATION = "Claude is waiting for your input"
_MAX_SPOKEN_CHARS = 200


@dataclass
class Backend:
    """Represents one TTS or LLM script-based backend.

    Each backend wraps a Python script that is invoked via ``uv run``.
    Availability is determined by the script existing on disk and, when
    ``env_key`` is set, the corresponding environment variable being
    present.
    """

    name: str
    script: Path
    env_key: Optional[str] = None
    timeout: int = 15

    def is_available(self) -> bool:
        """Return True when the backend can be used right now."""
        if not self.script.exists():
            return False
        if self.env_key and not os.getenv(self.env_key):
            return False
        return True

    def run(self, *args: str) -> Optional[str]:
        """Execute the backend script and return stripped stdout, or None on failure."""
        try:
            result = subprocess.run(
                ["uv", "run", str(self.script), *args],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        return None


def _shorten_path(path: str) -> str:
    """Shorten an absolute path to ~/last/two/parts for readability."""
    short = path.replace(os.path.expanduser("~"), "~")
    parts = short.split("/")
    return "/".join(parts[-2:]) if len(parts) > 2 else short


def append_to_log(log_path: str, data: dict) -> None:
    """Append data to a JSON array log file, creating it if needed."""
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        try:
            with open(log_path, "r") as f:
                log_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            log_data = []
        log_data.append(data)
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)
    except Exception:
        pass


def copy_transcript_to_chat(transcript_path: str, log_dir: str) -> None:
    """Convert a JSONL transcript to a JSON array at logs/chat.json."""
    try:
        chat_data = []
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        chat_data.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        chat_file = os.path.join(log_dir, "chat.json")
        with open(chat_file, "w") as f:
            json.dump(chat_data, f, indent=2)
    except Exception:
        pass


class TranscriptParser:
    """Parses Claude Code JSONL transcripts into a context summary.

    The summary has three sections:
      Request:  the last user message
      Actions:  deduplicated tool calls with key inputs (last 8)
      Outcome:  the last assistant text
    """

    @staticmethod
    def parse(transcript_path: Optional[str], max_entries: int = 60) -> Optional[str]:
        """Parse a transcript file and return a context summary string, or None."""
        if not transcript_path:
            return None

        try:
            recent: deque[dict] = deque(maxlen=max_entries)
            with open(transcript_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            recent.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass

            if not recent:
                return None

            last_user_message: Optional[str] = None
            tool_actions: list[str] = []
            seen_action_keys: set[str] = set()
            last_assistant_text: Optional[str] = None

            for entry in recent:
                etype = entry.get("type")

                if etype == "user" and not entry.get("toolUseResult"):
                    content = entry.get("message", {}).get("content", "")
                    if isinstance(content, str) and content.strip():
                        last_user_message = content.strip()[:200]
                    elif isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                text = block.get("text", "").strip()
                                if text:
                                    last_user_message = text[:200]

                elif etype == "assistant":
                    for block in entry.get("message", {}).get("content", []):
                        if not isinstance(block, dict):
                            continue
                        btype = block.get("type")

                        if btype == "text":
                            text = block.get("text", "").strip()
                            if text:
                                last_assistant_text = text[:300]

                        elif btype == "tool_use":
                            name = block.get("name", "")
                            inp = block.get("input", {})

                            if name in ("Edit", "Write", "Read", "MultiEdit"):
                                short = _shorten_path(inp.get("file_path", ""))
                                key = f"{name}:{short}"
                                if key not in seen_action_keys:
                                    seen_action_keys.add(key)
                                    tool_actions.append(f"{name} {short}")

                            elif name == "Bash":
                                cmd = inp.get("command", "").split("\n")[0].strip()[:60]
                                key = f"Bash:{cmd[:30]}"
                                if key not in seen_action_keys:
                                    seen_action_keys.add(key)
                                    tool_actions.append(f"Bash({cmd})")

                            elif name == "Agent":
                                desc = inp.get("description", "")[:60]
                                tool_actions.append(f"Agent({desc})")

                            elif name in ("Glob", "Grep", "WebFetch", "WebSearch"):
                                if name not in seen_action_keys:
                                    seen_action_keys.add(name)
                                    tool_actions.append(name)

            parts: list[str] = []
            if last_user_message:
                parts.append(f"Request: {last_user_message}")
            if tool_actions:
                parts.append(f"Actions: {', '.join(tool_actions[-8:])}")
            if last_assistant_text:
                parts.append(f"Outcome: {last_assistant_text}")

            if not parts:
                return None
            return "\n".join(parts)[:800]

        except Exception:
            return None


class NotificationService:
    """Orchestrates TTS and LLM backends for hook notifications.

    Tries backends in priority order, falling back gracefully when
    a backend is unavailable or returns no output.
    """

    def __init__(
        self,
        tts_backends: list[Backend],
        llm_backends: list[Backend],
        fallback_messages: list[str],
    ) -> None:
        self.tts_backends = tts_backends
        self.llm_backends = llm_backends
        self.fallback_messages = fallback_messages

    def _first_available_tts(self) -> Optional[Backend]:
        """Return the first available TTS backend, or None."""
        for b in self.tts_backends:
            if b.is_available():
                return b
        return None

    def _generate_message(self, transcript_path: Optional[str] = None) -> str:
        """Generate a completion message via LLM, with transcript context."""
        available_llms = [b for b in self.llm_backends if b.is_available()]
        context = TranscriptParser.parse(transcript_path) if available_llms else None

        for backend in available_llms:
            args = ["--completion"]
            if context:
                args += ["--context", context]
            result = backend.run(*args)
            if result:
                return result

        return random.choice(self.fallback_messages)

    def speak_completion(self, transcript_path: Optional[str] = None) -> None:
        """Generate an LLM completion message and speak it via TTS."""
        tts = self._first_available_tts()
        if not tts:
            return

        message = self._generate_message(transcript_path)
        tts.run(message)

    def speak_notification(self, message: Optional[str] = None) -> None:
        """Speak a notification message verbatim, or a generic fallback."""
        tts = self._first_available_tts()
        if not tts:
            return

        if message and message.strip() and message.strip() != _GENERIC_NOTIFICATION:
            spoken = message.strip()[:_MAX_SPOKEN_CHARS]
        else:
            engineer_name = os.getenv("ENGINEER_NAME", "").strip()
            if engineer_name and random.random() < 0.3:
                spoken = f"{engineer_name}, your input is needed"
            else:
                spoken = "Your input is needed"

        tts.run(spoken)


def build_service(hooks_dir: Optional[Path] = None) -> NotificationService:
    """Factory that creates a NotificationService with default backends.

    TTS priority:  ElevenLabs -> OpenAI -> pyttsx3
    LLM priority:  claude_cli -> OpenAI -> Anthropic -> Ollama
    """
    if hooks_dir is None:
        hooks_dir = Path(__file__).parent.parent

    tts_dir = hooks_dir / "utils" / "tts"
    llm_dir = hooks_dir / "utils" / "llm"

    tts_backends = [
        Backend("elevenlabs", tts_dir / "elevenlabs_tts.py", env_key="ELEVENLABS_API_KEY", timeout=10),
        Backend("openai", tts_dir / "openai_tts.py", env_key="OPENAI_API_KEY", timeout=10),
        Backend("pyttsx3", tts_dir / "pyttsx3_tts.py", timeout=10),
    ]

    llm_backends = [
        Backend("claude_cli", llm_dir / "claude_cli.py", timeout=15),
        Backend("openai", llm_dir / "oai.py", env_key="OPENAI_API_KEY", timeout=15),
        Backend("anthropic", llm_dir / "anth.py", env_key="ANTHROPIC_API_KEY", timeout=15),
        Backend("ollama", llm_dir / "ollama.py", timeout=15),
    ]

    return NotificationService(
        tts_backends=tts_backends,
        llm_backends=llm_backends,
        fallback_messages=FALLBACK_MESSAGES,
    )
