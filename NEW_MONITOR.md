# 🆕 New Monitor: Claude Status!

## What It Does

Monitors Claude service status in real-time using the official status.claude.com API!

Shows:
- ✅ Overall system status
- 📊 Individual service status (claude.ai, API, Claude Code, etc.)
- 🚨 Recent incidents (if any)

---

## Try It Now!

```bash
cd ~/code/py-wtf
source venv/bin/activate
python monitors/claude_status.py
```

**Press 'q' to exit**

Updates every 30 seconds (perfect refresh rate for status monitoring).

---

## What You'll See

### When Everything is Operational:
```
✅ All Systems Operational

Services:
  [✓] claude.ai
  [✓] platform.claude.com
  [✓] Claude API
  [✓] Claude Code

No recent incidents
```

### When There's an Issue:
```
⚠️ Minor Service Disruption

Services:
  [⚠] claude.ai
  [✓] Claude API
  [✓] Claude Code

Recent Incidents:
  ⚠ Elevated errors on Claude.ai
     Status: monitoring | 2025-11-11 21:30 UTC
```

---

## The API Behind It

Uses the official Statuspage API (same backend as GitHub Status, etc.):

- **Status**: `https://status.claude.com/api/v2/status.json`
- **Components**: `https://status.claude.com/api/v2/components.json`
- **Incidents**: `https://status.claude.com/api/v2/incidents.json`

All public, no auth needed!

---

## Your Four Monitors

You now have:

1. **system.py** - System resources (CPU, memory, disk)
2. **gpu.py** - NVIDIA GPU stats
3. **processes.py** - Top processes
4. **claude_status.py** - Claude service status ⭐ NEW!

All smooth, zero blink, WTF-quality!

---

## Idea: Use With tmux

Create a monitoring dashboard:

```bash
tmux new -s claude-monitor
tmux split-window -h
tmux select-pane -t 0
tmux send-keys 'cd ~/code/py-wtf && source venv/bin/activate && python monitors/system.py' C-m
tmux select-pane -t 1
tmux send-keys 'cd ~/code/py-wtf && source venv/bin/activate && python monitors/claude_status.py' C-m
tmux attach
```

Now you have system stats + Claude status side-by-side! 🚀

---

*This is exactly the kind of monitor that's easy to add with the pattern we built!*
