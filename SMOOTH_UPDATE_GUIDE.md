# Smooth Updates - How WTF Does It

## The Problem

ANSI escape codes (`\033[2J`, `\033[H`) cause visible screen blink because they:
1. Clear the entire screen buffer
2. Redraw everything from scratch
3. Terminal sees this as two separate operations

## How WTF Avoids Blinking

WTF uses `tview` (Go's TUI library) which does **double buffering**:

```go
widget.View.Clear()           // Clear internal buffer
widget.View.SetText(content)  // Update buffer
widget.RedrawChan <- true     // Signal to render
// Library handles efficient terminal update
```

The library:
- Maintains an **off-screen buffer**
- Calculates **difference** between old and new content
- Only sends **changed characters** to terminal
- Uses **cursor positioning** to minimize updates

## Python Equivalent: curses

Python's `curses` library does the same thing:

```python
stdscr.clear()      # Clear internal buffer
stdscr.addstr(...)  # Add to buffer
stdscr.refresh()    # Efficiently update terminal
```

## Three Versions Available

### 1. Simple ANSI (Blinks)
**File:** `monitors/lib/monitor_blink.py`

```python
from lib.monitor_blink import Monitor
```

**Pros:**
- Simple code
- Works everywhere
- No dependencies

**Cons:**
- ❌ Visible blink/flicker
- ❌ Distracting on fast updates

**Use when:** You're okay with blinking

---

### 2. ANSI with Cursor Positioning (Less Blink)
**File:** `monitors/lib/monitor.py` (default)

```python
from lib.monitor import Monitor
```

**Pros:**
- No full screen clear
- Fairly smooth
- Simple code

**Cons:**
- ⚠️ Footer still blinks (Ctrl+C message)
- ⚠️ May leave artifacts if output shrinks

**Use when:** You want simple smooth updates

---

### 3. Curses (Perfectly Smooth - Like WTF!)
**File:** `monitors/lib/monitor_curses.py`

```python
from lib.monitor_curses import Monitor
```

**Pros:**
- ✅ **Zero flicker** - just like WTF!
- ✅ Efficient terminal updates
- ✅ Footer never blinks
- ✅ Proper color support
- ✅ Keyboard handling (press 'q' to quit)

**Cons:**
- More complex code
- Requires curses (standard library, but may not work in all terminals)

**Use when:** You want WTF-quality smoothness

---

## Comparison

### Visual Blink Test

```bash
# Most blink - distracting
python monitors/system.py  # (if using monitor_blink.py)

# Less blink - footer blinks
python monitors/system_noblink.py

# Zero blink - perfectly smooth!
python monitors/system_smooth.py  # Press 'q' to quit
```

### Code Comparison

**Simple ANSI:**
```python
def run(self):
    while True:
        print("\033[2J\033[H")  # Clear & home - BLINKS!
        print(self.render())
        time.sleep(interval)
```

**Curses (WTF-style):**
```python
def run(self):
    curses.wrapper(self._run_curses)

def _run_curses(self, stdscr):
    while True:
        stdscr.clear()      # Buffer clear - no blink
        stdscr.addstr(...)  # Update buffer
        stdscr.refresh()    # Efficient update - smooth!
        time.sleep(interval)
```

---

## Making All Monitors Smooth

To convert any monitor to smooth mode:

### Change the import:
```python
# FROM:
from lib.monitor import Monitor

# TO:
from lib.monitor_curses import Monitor
```

### Change quit method:
```python
# OLD: Ctrl+C to quit
# NEW: Press 'q' to quit (or Ctrl+C still works)
```

That's it! Everything else stays the same.

---

## Why Curses is Better

| Feature | ANSI | Curses |
|---------|------|--------|
| Screen clear | Visible blink | Buffer only |
| Footer updates | Redraws (blinks) | Static (no blink) |
| Color support | ANSI codes | Native colors |
| Terminal compat | Universal | Most terminals |
| Code complexity | Simple | Moderate |
| WTF-quality | ❌ | ✅ |

---

## Recommendation

**Use curses version (`monitor_curses.py`) as your base!**

It's how WTF achieves smooth updates, and it's the proper way to do TUI in Python.

Update `monitors/lib/monitor.py` to be the curses version:

```bash
cd ~/code/py-wtf/monitors/lib
cp monitor.py monitor_ansi.py     # Backup
cp monitor_curses.py monitor.py   # Make curses default
```

Now all new monitors get smooth updates by default!

---

## Example: Creating Smooth Monitor

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor import Monitor  # Uses curses now!

class MyMonitor(Monitor):
    def __init__(self):
        super().__init__("My Monitor", refresh_interval=1)
    
    def fetch_data(self):
        return "Hello"
    
    def format_output(self, data):
        # Color support works!
        return self.colorize(data, 'green')

if __name__ == "__main__":
    MyMonitor().run()  # Smooth, no blink!
```

**Press 'q' to quit** (not Ctrl+C, though that still works)

---

## Technical Details: How Curses Works

Curses maintains **two buffers**:

1. **Virtual screen** - What curses thinks is on screen
2. **Physical screen** - What's actually on terminal

On `refresh()`:
1. Compare virtual vs physical
2. Calculate minimal changes
3. Send only differences to terminal
4. Update physical screen state

This is **exactly** how WTF's `tview` works - and why it's so smooth!

---

*Now you have WTF-quality smoothness in Python!* 🚀
