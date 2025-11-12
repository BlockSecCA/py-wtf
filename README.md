# py-wtf - Python Terminal Monitoring Framework

A lightweight, extensible terminal monitoring framework inspired by [WTF Terminal Dashboard](https://wtfutil.com/), but built with Python's simplicity and ease of use.

**WTF-quality smoothness** using `curses`, but without the Go compilation headaches!

## Features

- ✅ **Smooth, flicker-free updates** using curses double buffering
- ✅ **Automatic terminal resize detection** via SIGWINCH
- ✅ **Easy to extend** - copy a monitor, edit 2 methods, done!
- ✅ **No compilation needed** - just Python
- ✅ **Works everywhere** - SSH, tmux, Windows Terminal, etc.
- ✅ **Full screen usage** - no wasted space

## Quick Start

```bash
# Clone and setup
git clone <this-repo>
cd py-wtf
python3 -m venv venv
source venv/bin/activate

# Run a monitor
python monitors/system.py

# Press 'q' to exit
```

## Included Monitors

- **system.py** - CPU, memory, disk usage
- **gpu.py** - NVIDIA GPU stats (requires nvidia-smi)
- **processes.py** - Top processes by CPU/memory
- **claude_status.py** - Claude service status from status.claude.com API
- **resize_demo.py** - Demonstrates terminal resize detection

## Creating Your Own Monitor

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor import Monitor

class MyMonitor(Monitor):
    def __init__(self):
        super().__init__("My Monitor", refresh_interval=5)
    
    def fetch_data(self):
        # Get your data here
        return {"value": 42}
    
    def format_output(self, data):
        # Format for display
        return self.colorize(f"Value: {data['value']}", 'green')

if __name__ == "__main__":
    MyMonitor().run()
```

Save as `monitors/mymonitor.py`, then `python monitors/mymonitor.py` - it just works!

## Architecture

```
py-wtf/
├── monitors/           # Your actual monitors (run these!)
│   ├── system.py
│   ├── gpu.py
│   └── lib/           # Base classes (framework)
│       └── monitor.py  # Main base class
├── venv/              # Python virtual environment
└── README.md
```

**Key principle:** `monitors/` contains runnable tools, `monitors/lib/` contains the reusable framework.

## Documentation

- **QUICKSTART.md** - Detailed getting started guide
- **STRUCTURE_EXPLAINED.md** - Project structure and design
- **WINDOWS_TERMINAL.md** - Windows Terminal + SSH setup
- **RESIZE_SUPPORT.md** - How terminal resize detection works
- **TERMINAL_ARCHAEOLOGY.md** - Deep dive into terminal/TTY history
- **SMOOTH_UPDATE_GUIDE.md** - Technical details on curses smoothness

## Why py-wtf?

**WTF Terminal Dashboard** is excellent but has drawbacks:
- Requires Go toolchain
- Need to edit 3 files + recompile to add a widget
- Complex configuration
- No longer actively maintained

**py-wtf** provides:
- Same smooth, flicker-free updates (curses)
- Same resize detection (SIGWINCH)
- But: Python (not Go), single file per monitor, no compilation

## Requirements

- Python 3.8+
- Linux/macOS (uses curses)
- Works via SSH, in tmux/screen, Windows Terminal

## Philosophy

> Start simple, evolve as needed.

- **Phase 1:** Individual monitors work standalone ← *You are here*
- **Phase 2:** Shared patterns via base class ← *Done!*
- **Phase 3:** Optional dashboard launcher ← *Future, if needed*

Don't build the dashboard until you need it!

## License

MIT - Do whatever you want with it!

## Credits

Inspired by [WTF Terminal Dashboard](https://github.com/wtfutil/wtf) by Chris Cummer.

Built with:
- Python's `curses` library (ncurses)
- Standard Unix signals (SIGWINCH)
- 40+ years of terminal technology 🏛️
