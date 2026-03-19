# 🔄 Terminal Resize Support - Just Like WTF!

## Yes, Curses Detects Terminal Changes!

The `curses` library has had resize detection since the 1980s - it's one of its core features!

---

## How It Works

### Signal-Based Detection
When you resize a terminal, the OS sends **SIGWINCH** (Window Change signal):

```python
import signal

def handle_resize(signum, frame):
    # Terminal was resized!
    redraw_everything()

signal.signal(signal.SIGWINCH, handle_resize)
```

### Curses Built-in
Curses also provides **KEY_RESIZE**:

```python
key = stdscr.getch()
if key == curses.KEY_RESIZE:
    # Terminal was resized!
    # curses.LINES and curses.COLS are automatically updated
```

---

## Demo: See It In Action

### Try the Resize Demo:

```bash
cd py-wtf
source venv/bin/activate
python monitors/resize_demo.py
```

**Then resize your terminal window** - watch it adapt instantly!

The demo shows:
- Current terminal dimensions
- Visual bar that scales with width
- Warnings for small terminals
- Everything updates automatically

---

## What Happens During Resize

1. **OS sends SIGWINCH** → Your terminal changed size!
2. **Signal handler sets flag** → `_needs_resize = True`
3. **Main loop detects flag** → Time to redraw
4. **Curses updates LINES/COLS** → New dimensions available
5. **Content re-renders** → Fits new size perfectly
6. **Screen refreshes** → Smooth transition!

Just like WTF, but simpler code!

---

## Key Features

### ✅ Automatic Width Adjustment
Headers, separators, content - all adapt to new width:

```python
def render_header(self):
    width = curses.COLS  # Automatically updated!
    separator = "=" * min(width, 120)
    return separator
```

### ✅ Content Truncation
Content that's too wide gets truncated automatically:

```python
# Display line, but don't exceed terminal width
display_line = line[:curses.COLS-1]
stdscr.addstr(row, 0, display_line)
```

### ✅ Height Awareness
Shows "... output truncated" if terminal is too short:

```python
if row >= curses.LINES - 1:
    stdscr.addstr(row, 0, "... (output truncated - resize terminal)")
    break
```

---

## Using Resize Support in Your Monitors

### Option 1: Use the Resize-Aware Base Class

```bash
# Make resize support the default
cd py-wtf/monitors/lib
cp monitor.py monitor_no_resize.py
cp monitor_resize.py monitor.py
```

Now all new monitors automatically resize!

### Option 2: Keep Per-Monitor

```python
# Monitors that need resize
from lib.monitor_resize import Monitor

# Simple monitors (current default)
from lib.monitor import Monitor
```

---

## Comparison: WTF vs py-wtf Resize

| Feature | WTF | py-wtf |
|---------|-----|--------|
| **Detects resize** | ✅ (via tview) | ✅ (via curses) |
| **Auto-reflow** | ✅ | ✅ |
| **Grid layout resize** | ✅ (complex) | ⏳ (Phase 3) |
| **Widget resize** | ✅ | ✅ (content adapts) |
| **Terminal size** | Shows in status | Shows in footer |
| **Code complexity** | High | Low |

For **individual monitors**, curses resize is just as good as WTF!

For **grid layouts**, you'd need the Phase 3 dashboard launcher.

---

## Technical Details

### SIGWINCH Signal
- Sent by kernel when terminal size changes
- Standard on Unix/Linux (since 1980s)
- Works in SSH sessions
- Works in tmux/screen
- Works in Windows Terminal (via WSL)

### Curses Variables
After resize, these auto-update:
- `curses.LINES` - New height
- `curses.COLS` - New width  
- `stdscr.getmaxyx()` - Returns (height, width)

### Race Conditions
The resize handler sets a flag, main loop checks it:

```python
# Signal handler (async)
def _handle_resize(self, signum, frame):
    self._needs_resize = True

# Main loop (sync)
if self._needs_resize:
    self._needs_resize = False
    redraw_everything()
```

No race conditions, no blocking!

---

## Why This Is Cool

**WTF's resize was impressive** - widgets smoothly adapted to new terminal size.

**Your monitors do the same thing** - using standard Unix signals that have worked since the 1980s!

The difference:
- WTF: Complex Go/tview library magic
- py-wtf: Standard Unix + curses (simpler, more transparent)

---

## Try It Now

1. **Run the demo:**
   ```bash
   python monitors/resize_demo.py
   ```

2. **Grab terminal corner and drag**
   
3. **Watch it adapt in real-time!**

4. **Try your other monitors:**
   ```bash
   python monitors/system.py
   # Resize terminal - header adapts!
   ```

---

*Curses has had resize detection since before you were born - and it still works perfectly!* 🔄
