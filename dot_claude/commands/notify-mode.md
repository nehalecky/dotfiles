Switch the Claude Code notification delivery mode.

Modes control how hook notifications are delivered after task completion:
- **tts** — audio only (ElevenLabs → OpenAI → Kokoro → macOS say)
- **macos** — macOS Notification Center only, silent TTS (ideal for meetings)
- **both** — audio + visual notifications (default)
- **silent** — log only, no audio or visual delivery

Run the shell command to switch:

```bash
claude-notify $ARGUMENTS
```

If no mode argument is given, show current status. After switching, confirm the new mode by running `claude-notify` with no arguments.
