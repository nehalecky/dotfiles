---
description: Morning briefing with weather, recent work, and task suggestions
allowed-tools: Bash, Read, TodoWrite
---

# Morning Brief

Please invoke the **executive-assistant** agent to provide a comprehensive morning brief.

The brief should include:

1. **Weather Forecast** (run: `~/.local/bin/weather`)
   - Current conditions for La Lucila
   - Temperature and forecast

2. **Recent Work** (run: `git log --oneline -5` in current directory)
   - Last 5 commits
   - Current branch
   - Any uncommitted changes (`git status --short`)

3. **Pending Tasks**
   - Check `~/.claude/todos/` for incomplete tasks
   - List top 5 priorities

4. **Suggested Next Steps**
   - Based on recent work and pending tasks
   - Clear actionable items

Format as a concise, scannable brief (2-3 minutes to read).
