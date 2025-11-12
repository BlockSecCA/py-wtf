# Project Structure Explained 📁

## The Two Directories

```
monitors/
├── system.py           ← YOUR MONITORS (the actual tools you run)
├── gpu.py
├── processes.py
├── claude_status.py
├── resize_demo.py
└── lib/                ← BASE CLASSES (the foundation/library)
    ├── monitor.py
    ├── monitor_clean.py
    ├── monitor_curses.py
    ├── monitor_resize.py
    ├── monitor_with_status.py
    └── monitor_blink.py
```

---

## `monitors/` (Top Level)

**What:** Actual executable monitors you run

**Examples:**
- `system.py` - Shows CPU, memory, disk
- `gpu.py` - Shows GPU stats
- `claude_status.py` - Shows Claude service status
- `processes.py` - Shows top processes

**How to use:**
```bash
python monitors/system.py        # Run directly!
python monitors/claude_status.py # Run directly!
```

**Think of these as:** Applications, programs, the actual tools

---

## `monitors/lib/` (Library)

**What:** Base classes that monitors inherit from

**Purpose:** Shared code that every monitor uses

**Files:**
- `monitor.py` - **The one you use** (currently = monitor_clean.py)
- `monitor_clean.py` - Clean version, uses full screen
- `monitor_curses.py` - Original curses implementation
- `monitor_resize.py` - With status line at bottom
- `monitor_with_status.py` - Same as resize
- `monitor_blink.py` - Old ANSI version (blinks)

**How monitors use them:**
```python
# Inside system.py
from lib.monitor import Monitor  # Import the base class

class SystemMonitor(Monitor):    # Inherit from it
    def fetch_data(self):
        # Your custom code here
```

**Think of these as:** The framework, the foundation, the library

---

## The Relationship

```
┌─────────────────────────────────────────┐
│  monitors/system.py                     │
│  (Your actual monitor)                  │
│                                         │
│  from lib.monitor import Monitor        │
│         ↓                               │
│  Uses base class for:                   │
│  - Curses setup                         │
│  - Resize handling                      │
│  - Color support                        │
│  - Keyboard input                       │
│                                         │
│  You only implement:                    │
│  - fetch_data() - Get your data        │
│  - format_output() - Display it        │
└─────────────────────────────────────────┘
           ↓ imports from
┌─────────────────────────────────────────┐
│  monitors/lib/monitor.py                │
│  (Base class / framework)               │
│                                         │
│  Handles:                               │
│  - Terminal management                  │
│  - Event loop                           │
│  - Resize detection                     │
│  - Color rendering                      │
│  - Error handling                       │
└─────────────────────────────────────────┘
```

---

## Real World Analogy

**monitors/** = Your recipes
- `system.py` = Recipe for chocolate cake
- `gpu.py` = Recipe for apple pie
- `claude_status.py` = Recipe for cookies

**monitors/lib/** = Your cooking techniques/methods
- `monitor.py` = "How to use an oven"
- Common techniques all recipes use
- Don't run these directly!

---

## Why This Structure?

### Without lib/ (BAD):
```python
# system.py
# 200 lines of curses setup code
# 50 lines of resize handling
# 30 lines of color management
# 20 lines of your actual system monitoring code
```

```python
# gpu.py  
# 200 lines of curses setup code (DUPLICATED!)
# 50 lines of resize handling (DUPLICATED!)
# 30 lines of color management (DUPLICATED!)
# 20 lines of your actual GPU monitoring code
```

**Problem:** Tons of duplication! Every monitor repeats same code.

### With lib/ (GOOD):
```python
# lib/monitor.py
# 200 lines of curses setup
# 50 lines of resize handling
# 30 lines of color management
# (Written ONCE, used by everyone!)
```

```python
# system.py
from lib.monitor import Monitor
# 20 lines of your actual system monitoring code
# That's it!
```

```python
# gpu.py
from lib.monitor import Monitor
# 20 lines of your actual GPU monitoring code
# That's it!
```

**Benefit:** Write the hard stuff once, reuse everywhere!

---

## Which Files Do You Care About?

### For USING the monitors:
**Only care about `monitors/*.py`** (top level files)
```bash
python monitors/system.py
python monitors/claude_status.py
```

### For CREATING new monitors:
1. Copy an existing monitor (e.g., `system.py`)
2. Change `fetch_data()` and `format_output()`
3. The `lib/` stuff just works (don't touch it!)

### For CUSTOMIZING the framework:
**Only then** look at `monitors/lib/monitor.py`
- Want different colors?
- Want different resize behavior?
- Want different base features?

But 99% of the time, you don't need to touch `lib/`!

---

## The Current State

**Default base class:** `monitor.py` (which is currently = `monitor_clean.py`)
- ✅ Curses-based (smooth, no blink)
- ✅ Resize detection (automatic)
- ✅ Uses full screen (no reserved space)
- ✅ Color support
- ✅ Press 'q' to quit

**All your monitors use this automatically** when they do:
```python
from lib.monitor import Monitor
```

---

## Summary

| Location | What | Run Directly? | Edit Often? |
|----------|------|---------------|-------------|
| `monitors/*.py` | Your actual monitors | ✅ Yes! | ✅ Yes - this is your code |
| `monitors/lib/*.py` | Base classes/framework | ❌ No | ❌ Rarely - it just works |

**TL;DR:**
- **Run** files in `monitors/`
- **Inherit from** files in `monitors/lib/`
- **Create new** monitors in `monitors/` (copy existing one)
- **Rarely touch** `monitors/lib/` (the framework is done!)

---

*Standard Python pattern: lib/ contains reusable code, top-level contains applications!* 📚
