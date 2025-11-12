#!/bin/bash
# Diagnostic script to check your terminal setup

echo "=========================================="
echo "Terminal Diagnostics"
echo "=========================================="
echo ""
echo "TERM variable: $TERM"
echo "COLORTERM: $COLORTERM"
echo "Terminal size: $(tput cols)x$(tput lines) 2>/dev/null || echo 'Unable to detect'"
echo "SSH_TTY: $SSH_TTY"
echo "SSH_CLIENT: $SSH_CLIENT"
echo ""
echo "Testing curses support..."
python3 << 'PYTHON'
import sys
try:
    import curses
    print("✅ curses module available")
    try:
        curses.setupterm()
        print("✅ Terminal is curses-capable")
    except:
        print("❌ Terminal does NOT support curses")
        print("   TERM may be set incorrectly")
except ImportError:
    print("❌ curses module not found")
PYTHON
echo ""
echo "=========================================="
echo "If you see '✅ Terminal is curses-capable',"
echo "then py-wtf monitors should work perfectly!"
echo ""
echo "If you see errors, check WINDOWS_TERMINAL.md"
echo "=========================================="
