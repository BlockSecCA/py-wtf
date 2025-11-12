# Windows Terminal + SSH Setup Guide

## The Problem

When you SSH from Windows Terminal to Ubuntu, sometimes `TERM` is set to `dumb`, which breaks curses.

## Quick Fix - Use The Helper Script

```bash
cd ~/code/py-wtf
./run.sh monitors/system.py
```

The helper script automatically sets TERM correctly!

---

## Permanent Fix (Recommended)

Your `~/.bashrc` has been updated. Reload it:

```bash
source ~/.bashrc
```

Now check TERM:
```bash
echo $TERM
```

Should show `xterm-256color` (not `dumb`).

Then monitors work normally:
```bash
cd ~/code/py-wtf
source venv/bin/activate
python monitors/system.py
```

---

## Windows Terminal Configuration (Best Solution)

Configure Windows Terminal to set TERM automatically:

1. Open Windows Terminal Settings (Ctrl+,)
2. Find your SSH profile
3. Add environment variable

Or edit `settings.json`:

```json
{
    "profiles": {
        "list": [
            {
                "name": "Ubuntu SSH",
                "commandline": "ssh user@host",
                "environment": {
                    "TERM": "xterm-256color"
                }
            }
        ]
    }
}
```

---

## Quick Test

```bash
# Set TERM for this session
export TERM=xterm-256color

# Run monitor
cd ~/code/py-wtf
source venv/bin/activate
python monitors/system.py
```

**Press 'q' to exit**

If this works, the issue was TERM!

---

*Windows Terminal is perfect for curses - just needs TERM set correctly!* 🚀
