"""
Base Monitor class with resize support - NO status line
Clean version that uses 100% of terminal space
"""
import curses
import signal
import time
import sys
from abc import ABC, abstractmethod
from datetime import datetime


class Monitor(ABC):
    """
    Base class for monitors with resize support - clean version
    """
    
    def __init__(self, name, refresh_interval=5):
        self.name = name
        self.refresh_interval = refresh_interval
        self._running = False
        self.stdscr = None
        self._needs_resize = False
    
    @abstractmethod
    def fetch_data(self):
        pass
    
    @abstractmethod
    def format_output(self, data):
        pass
    
    def get_timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def render_header(self):
        timestamp = self.get_timestamp()
        width = curses.COLS if self.stdscr else 60
        separator = "=" * min(width, 120)
        return [
            separator,
            self.name,
            f"Time: {timestamp}",
            separator,
            ""
        ]
    
    def _setup_colors(self):
        """Initialize color pairs for curses"""
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)
            curses.init_pair(2, curses.COLOR_GREEN, -1)
            curses.init_pair(3, curses.COLOR_YELLOW, -1)
            curses.init_pair(4, curses.COLOR_BLUE, -1)
            curses.init_pair(5, curses.COLOR_CYAN, -1)
            curses.init_pair(6, curses.COLOR_MAGENTA, -1)
            curses.init_pair(7, curses.COLOR_WHITE, -1)
    
    def _get_color_pair(self, color_name):
        """Get curses color pair number from color name"""
        color_map = {
            'red': 1,
            'green': 2,
            'yellow': 3,
            'blue': 4,
            'cyan': 5,
            'magenta': 6,
            'white': 7
        }
        return curses.color_pair(color_map.get(color_name, 7))
    
    def colorize(self, text, color):
        """Return text with color marker"""
        return f"<{color.upper()}:{text}>"
    
    def _render_line(self, stdscr, line, row):
        """Render a line with color support"""
        if row >= curses.LINES:
            return
            
        col = 0
        pos = 0
        
        while pos < len(line) and col < curses.COLS - 1:
            if line[pos:pos+1] == '<':
                end_marker = line.find(':', pos)
                if end_marker != -1:
                    close_marker = line.find('>', end_marker)
                    if close_marker != -1:
                        color_name = line[pos+1:end_marker].lower()
                        text = line[end_marker+1:close_marker]
                        
                        render_text = text[:curses.COLS - col - 1]
                        try:
                            stdscr.addstr(row, col, render_text, self._get_color_pair(color_name))
                        except curses.error:
                            pass
                        
                        col += len(render_text)
                        pos = close_marker + 1
                        continue
            
            try:
                stdscr.addch(row, col, line[pos])
            except curses.error:
                pass
            col += 1
            pos += 1
    
    def _handle_resize(self, signum, frame):
        """Handle SIGWINCH (terminal resize signal)"""
        self._needs_resize = True
    
    def _run_curses(self, stdscr):
        """Main loop running inside curses"""
        self.stdscr = stdscr
        self._setup_colors()
        
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(100)
        
        signal.signal(signal.SIGWINCH, self._handle_resize)
        
        self._running = True
        last_refresh = 0
        
        while self._running:
            current_time = time.time()
            
            if self._needs_resize:
                self._needs_resize = False
                stdscr.clear()
                stdscr.refresh()
            
            if current_time - last_refresh >= self.refresh_interval or self._needs_resize:
                try:
                    stdscr.clear()
                    
                    max_y, max_x = stdscr.getmaxyx()
                    
                    # Render header
                    header_lines = self.render_header()
                    for i, line in enumerate(header_lines):
                        if i >= max_y:
                            break
                        try:
                            display_line = line[:max_x-1]
                            stdscr.addstr(i, 0, display_line)
                        except curses.error:
                            pass
                    
                    row = len(header_lines)
                    
                    # Fetch and render data
                    try:
                        data = self.fetch_data()
                        output = self.format_output(data)
                        
                        for line in output.split('\n'):
                            if row >= max_y:
                                # No truncation message - just stop
                                break
                            self._render_line(stdscr, line, row)
                            row += 1
                    
                    except Exception as e:
                        error_msg = self.colorize(f"Error: {e}", 'red')
                        if row < max_y:
                            self._render_line(stdscr, error_msg, row)
                    
                    # NO status line at bottom - use full screen!
                    stdscr.refresh()
                    
                    last_refresh = current_time
                
                except Exception as e:
                    stdscr.clear()
                    stdscr.addstr(0, 0, f"Fatal error: {e}"[:curses.COLS-1] if curses.COLS > 0 else "Error")
                    stdscr.refresh()
                    time.sleep(2)
                    break
            
            try:
                key = stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == curses.KEY_RESIZE:
                    self._needs_resize = True
            except:
                pass
            
            time.sleep(0.05)
    
    def run(self):
        """Run the monitor with curses wrapper"""
        try:
            curses.wrapper(self._run_curses)
        except KeyboardInterrupt:
            pass
        finally:
            print("\nExiting...")
    
    def stop(self):
        self._running = False
