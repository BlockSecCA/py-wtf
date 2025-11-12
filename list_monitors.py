#!/usr/bin/env python3
"""
List all available monitors with their metadata
"""
import sys
import importlib.util
from pathlib import Path

def load_monitor_meta(script_path):
    """Load DASHBOARD_META from a monitor script"""
    try:
        spec = importlib.util.spec_from_file_location("monitor", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Look for monitor class
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, type) and 
                hasattr(obj, 'DASHBOARD_META') and 
                name.endswith('Monitor')):
                return obj.DASHBOARD_META
    except Exception as e:
        return None
    
    return None

def main():
    monitors_dir = Path(__file__).parent / 'monitors'
    
    print("=" * 70)
    print("Available Monitors")
    print("=" * 70)
    print()
    
    monitors = []
    for script in sorted(monitors_dir.glob('*.py')):
        if script.name.startswith('_'):
            continue
        
        meta = load_monitor_meta(script)
        monitors.append({
            'file': script.name,
            'meta': meta
        })
    
    for m in monitors:
        print(f"📊 {m['file']}")
        if m['meta']:
            print(f"   Name:     {m['meta'].get('name', 'N/A')}")
            print(f"   Size:     {m['meta'].get('size', 'N/A')}")
            print(f"   Category: {m['meta'].get('category', 'N/A')}")
        print(f"   Run:      python monitors/{m['file']}")
        print()
    
    print("=" * 70)
    print(f"Total monitors: {len(monitors)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
