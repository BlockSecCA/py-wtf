# py-wtf Quick Start

## First Time Setup

```bash
cd ~/code/py-wtf
source venv/bin/activate
```

Or use the helper:
```bash
cd ~/code/py-wtf
source activate.sh
```

## Try the Monitors

### System Monitor
```bash
python monitors/system.py
```
Shows CPU, memory, and disk usage. Updates every 2 seconds.

### GPU Monitor
```bash
python monitors/gpu.py
```
Shows NVIDIA GPU stats (requires nvidia-smi). Updates every 1 second.

### Process Monitor
```bash
# Top CPU consumers
python monitors/processes.py

# Top memory consumers
python monitors/processes.py --sort mem

# Show top 20 processes
python monitors/processes.py --limit 20
```

**Press Ctrl+C to exit any monitor.**

## Create Your First Monitor

Let's make a simple clock monitor:

```bash
cat > monitors/clock.py << 'PYTHON'
#!/usr/bin/env python3
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor import Monitor

class ClockMonitor(Monitor):
    DASHBOARD_META = {
        'name': 'Clock',
        'size': 'small',
        'category': 'utils'
    }
    
    def __init__(self):
        super().__init__("Clock", refresh_interval=1)
    
    def fetch_data(self):
        return datetime.now()
    
    def format_output(self, dt):
        time_str = dt.strftime('%H:%M:%S')
        date_str = dt.strftime('%A, %B %d, %Y')
        
        return f"""
{self.colorize(time_str, 'cyan')}
{date_str}
        """

if __name__ == "__main__":
    ClockMonitor().run()
PYTHON

chmod +x monitors/clock.py
python monitors/clock.py
```

## Next Steps

1. **Explore the code**: Look at `monitors/lib/monitor.py` to see the base class
2. **Copy and modify**: Use an existing monitor as a template
3. **Add features**: The base class supports colors, timestamps, error handling
4. **Share monitors**: Each monitor is just a standalone Python script

## The Pattern

Every monitor follows this pattern:

```python
class YourMonitor(Monitor):
    def __init__(self):
        super().__init__("Monitor Name", refresh_interval=5)
    
    def fetch_data(self):
        # Get your data here
        return data
    
    def format_output(self, data):
        # Format for display
        return formatted_string
```

That's it! The base class handles:
- Screen clearing
- Refresh loop
- Error display
- Keyboard interrupts
- Timestamps
- Colors

## Evolution Path

**Now (Phase 1)**: Individual monitors work great standalone

**Later (Phase 2)**: If you create many monitors, the shared pattern prevents duplication

**Future (Phase 3)**: If you want, add a dashboard launcher that arranges monitors in a grid

But you don't need Phase 3 yet! Start simple, evolve as needed.

---

## 🎨 Smooth Updates (No Blink!)

### The Problem
The original monitors blink on every update. This is distracting!

### The Solution
Use the **curses-based monitor** (like WTF does):

```bash
python monitors/system_smooth.py
```

**Press 'q' to quit** (or Ctrl+C)

### Why It's Better
- ✅ Zero flicker - perfectly smooth updates
- ✅ Footer doesn't blink
- ✅ Just like WTF's smoothness
- ✅ Uses Python's `curses` library (same concept as WTF's `tview`)

### Make All Monitors Smooth
To make curses the default:

```bash
cd ~/code/py-wtf/monitors/lib
cp monitor.py monitor_ansi.py      # Backup old version
cp monitor_curses.py monitor.py    # Use curses as default
```

Now all new monitors are smooth by default!

See **SMOOTH_UPDATE_GUIDE.md** for technical details on how this works.
