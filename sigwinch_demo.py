#!/usr/bin/env python3
"""
Demo showing exactly how SIGWINCH works
Run this, then resize your terminal to see signals in action!
"""
import signal
import sys
import time
import struct
import fcntl
import termios

# Global counter
resize_count = 0

def get_terminal_size():
    """Ask the kernel: What's the terminal size?"""
    # This is the actual system call curses uses!
    # TIOCGWINSZ = Terminal I/O Control, Get Window Size
    data = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, b'\x00' * 8)
    rows, cols = struct.unpack('HHHH', data)[:2]
    return rows, cols

def sigwinch_handler(signum, frame):
    """This function is called when terminal resizes"""
    global resize_count
    resize_count += 1
    
    # Get new size from kernel
    rows, cols = get_terminal_size()
    
    timestamp = time.strftime('%H:%M:%S')
    
    print(f"\n[{timestamp}] 🔔 SIGWINCH received! (resize #{resize_count})")
    print(f"   New size: {cols} columns × {rows} rows")
    print(f"   Signal number: {signum}")
    print(f"   Process ID: {os.getpid()}")
    print()

def main():
    import os
    
    print("=" * 70)
    print("SIGWINCH Demo - Understanding Terminal Resize")
    print("=" * 70)
    print()
    print("This program shows EXACTLY what happens when you resize terminal:")
    print()
    
    # Show initial size
    rows, cols = get_terminal_size()
    print(f"Initial terminal size: {cols} × {rows}")
    print(f"Process ID: {os.getpid()}")
    print()
    
    # Register signal handler
    print("Registering SIGWINCH handler...")
    signal.signal(signal.SIGWINCH, sigwinch_handler)
    print("✅ Handler registered!")
    print()
    
    print("=" * 70)
    print("NOW: Resize your terminal window!")
    print("=" * 70)
    print()
    print("Watch what happens:")
    print("  1. You drag corner")
    print("  2. Terminal emulator detects change")
    print("  3. Kernel sends SIGWINCH signal")
    print("  4. This program receives it")
    print("  5. Handler prints new dimensions")
    print()
    print("Press Ctrl+C to exit")
    print("=" * 70)
    print()
    
    # Wait forever, handling signals
    try:
        while True:
            # Show we're alive
            print(f"Waiting for resize... (count: {resize_count})", end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        print(f"Total resizes detected: {resize_count}")

if __name__ == "__main__":
    main()
