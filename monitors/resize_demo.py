#!/usr/bin/env python3
"""
Resize Demo Monitor
Demonstrates automatic terminal resize handling
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor_resize import Monitor


class ResizeDemoMonitor(Monitor):
    """Demo monitor showing resize capabilities"""
    
    def __init__(self):
        super().__init__("Resize Demo - Try resizing your terminal!", refresh_interval=1)
        self.resize_count = 0
    
    def fetch_data(self):
        """Fetch some demo data"""
        import curses
        return {
            'width': curses.COLS,
            'height': curses.LINES,
            'area': curses.COLS * curses.LINES
        }
    
    def format_output(self, data):
        """Format demo output"""
        output = []
        
        width = data['width']
        height = data['height']
        
        output.append(self.colorize("Terminal Size Information:", 'cyan'))
        output.append("")
        output.append(f"Width (columns):  {self.colorize(str(width), 'green')}")
        output.append(f"Height (rows):    {self.colorize(str(height), 'green')}")
        output.append(f"Total cells:      {self.colorize(str(data['area']), 'green')}")
        output.append("")
        
        output.append(self.colorize("Resize Instructions:", 'yellow'))
        output.append("1. Drag the corner of your terminal window")
        output.append("2. Watch the values update automatically!")
        output.append("3. The content adapts to the new size")
        output.append("")
        
        # Show a visual bar that scales with width
        bar_length = min(width - 10, 80)
        bar = "█" * bar_length
        output.append(self.colorize("Width indicator:", 'cyan'))
        output.append(self.colorize(bar, 'blue'))
        output.append("")
        
        # Show size categories
        if width < 80:
            size_msg = "Terminal is NARROW - consider widening!"
            size_color = 'red'
        elif width < 120:
            size_msg = "Terminal is MEDIUM size - good for most tasks"
            size_color = 'yellow'
        else:
            size_msg = "Terminal is WIDE - excellent for monitoring!"
            size_color = 'green'
        
        output.append(self.colorize(size_msg, size_color))
        output.append("")
        
        if height < 24:
            height_msg = "Terminal is SHORT - some content may be truncated"
            height_color = 'red'
        elif height < 40:
            height_msg = "Terminal height is GOOD"
            height_color = 'yellow'
        else:
            height_msg = "Terminal is TALL - plenty of room!"
            height_color = 'green'
        
        output.append(self.colorize(height_msg, height_color))
        
        return '\n'.join(output)


if __name__ == "__main__":
    ResizeDemoMonitor().run()
