#!/bin/bash
# Helper script to run monitors with proper TERM setting

# Ensure TERM is set for curses
if [ "$TERM" = "dumb" ] || [ -z "$TERM" ]; then
    export TERM=xterm-256color
fi

# Activate venv
source venv/bin/activate

# Run the monitor
if [ $# -eq 0 ]; then
    echo "Usage: ./run.sh <monitor>"
    echo ""
    echo "Available monitors:"
    ls monitors/*.py | grep -v __pycache__ | sed 's/monitors\//  /'
    echo ""
    echo "Examples:"
    echo "  ./run.sh monitors/system.py"
    echo "  ./run.sh monitors/processes.py --sort mem"
else
    python "$@"
fi
