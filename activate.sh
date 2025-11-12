#!/bin/bash
# Helper script to activate venv and show available monitors

source venv/bin/activate

echo "=========================================="
echo "py-wtf Virtual Environment Activated"
echo "=========================================="
echo ""
echo "Available monitors:"
echo ""
for monitor in monitors/*.py; do
    if [ -f "$monitor" ] && [ "$(basename $monitor)" != "__init__.py" ]; then
        echo "  python $(basename $monitor)"
    fi
done
echo ""
echo "Examples:"
echo "  python monitors/system.py"
echo "  python monitors/gpu.py"
echo "  python monitors/processes.py --sort mem"
echo ""
echo "To deactivate: deactivate"
echo "=========================================="
