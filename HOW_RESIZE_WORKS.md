# How Terminal Resize Actually Works 🔍

## The Magic Explained

You resize terminal → Python magically knows. How?!

---

## The Players

### 1. **Terminal Emulator** (Windows Terminal)
- Draws the terminal window
- Handles mouse/keyboard input
- Maintains a character grid (e.g., 80×24 cells)

### 2. **TTY Driver** (in Linux kernel)
- Connects your terminal to processes
- Manages terminal state
- **Sends signals to processes**

### 3. **Your Python Process**
- Receives signals
- Responds to SIGWINCH
- Redraws content

---

## The Signal Flow Diagram

```
┌─────────────────────┐
│  Windows Terminal   │  You drag corner
│  (on Windows)       │  
└──────────┬──────────┘
           │ SSH connection
           │
           ▼
┌─────────────────────┐
│   SSH Daemon        │  Terminal size escape sequence
│  (on Ubuntu)        │  sent over SSH
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   PTY (Pseudo-TTY)  │  Kernel receives size change
│   /dev/pts/0        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  TTY Driver         │  Sends SIGWINCH signal
│  (kernel)           │  kill_pgrp(SIGWINCH)
└──────────┬──────────┘
           │ Signal 28 (SIGWINCH)
           ▼
┌─────────────────────┐
│  Python Process     │  Signal handler runs!
│  (your monitor)     │  _handle_resize()
└─────────────────────┘
```

---

## The System Calls Involved

### 1. Terminal Tells Kernel New Size

```c
// In SSH daemon (sshd) when it receives resize from client
struct winsize ws = {
    .ws_row = 30,     // New height
    .ws_col = 100     // New width
};
ioctl(pty_fd, TIOCSWINSZ, &ws);  // "Set window size"
```

This updates the kernel's TTY driver state.

### 2. Kernel Sends Signal

```c
// Inside kernel (drivers/tty/tty_io.c)
void tty_do_resize(struct tty_struct *tty, struct winsize *ws) {
    // Update internal state
    tty->winsize = *ws;
    
    // Send signal to all processes in foreground group
    kill_pgrp(tty->pgrp, SIGWINCH, 1);
}
```

SIGWINCH is signal number **28** on most systems.

### 3. Python Receives Signal

```python
import signal

def handler(signum, frame):
    # signum = 28 (SIGWINCH)
    # This runs ASYNCHRONOUSLY!
    print("Terminal resized!")

signal.signal(signal.SIGWINCH, handler)
```

### 4. Program Queries New Size

```python
import fcntl
import termios
import struct

# This is what curses does internally
data = fcntl.ioctl(
    sys.stdout.fileno(),  # File descriptor for stdout
    termios.TIOCGWINSZ,   # "Get window size" ioctl
    b'\x00' * 8           # Buffer for result
)

rows, cols = struct.unpack('HHHH', data)[:2]
print(f"New size: {cols}×{rows}")
```

---

## Why It's Asynchronous

**Key insight:** Signal handlers run **asynchronously** (interrupting normal code flow).

```python
# Your code is running here...
for i in range(1000000):
    print(i)
    # <-- SIGNAL ARRIVES HERE!
    #     Normal execution pauses
    #     Signal handler runs
    #     Then returns here
```

**That's why we use a flag:**

```python
_needs_resize = False

def handle_signal(sig, frame):
    global _needs_resize
    # Can't do much here - keep it simple!
    _needs_resize = True

# Main loop (safe, synchronous)
while True:
    if _needs_resize:
        _needs_resize = False
        redraw_everything()  # Safe to do complex work here
```

---

## The Windows Terminal → Ubuntu Flow

### On Windows Side:
1. You drag Windows Terminal corner
2. Windows Terminal detects mouse event
3. Terminal calculates new grid size (e.g., 100×30)
4. Terminal sends **escape sequence** over SSH:
   ```
   ESC[8;30;100t
   ```
   (Meaning: "Terminal is now 30 rows × 100 columns")

### On Ubuntu Side:
1. SSH daemon receives escape sequence
2. Parses new dimensions
3. Calls `ioctl(pty, TIOCSWINSZ, ...)` 
4. Kernel updates TTY state
5. Kernel sends SIGWINCH to your Python process
6. Your signal handler runs!

---

## Try It Yourself

### Demo 1: See SIGWINCH in Action

```bash
cd py-wtf
python sigwinch_demo.py
```

Then resize your terminal - watch it detect every resize!

### Demo 2: Manual Size Query

```bash
python3 << 'EOF'
import fcntl, termios, struct, sys
data = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, b'\x00'*8)
rows, cols = struct.unpack('HHHH', data)[:2]
print(f"Terminal size: {cols} columns × {rows} rows")
