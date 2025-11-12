"""
Base Monitor class for py-wtf
All monitors inherit from this to get consistent behavior
"""
import time
import sys
from abc import ABC, abstractmethod
from datetime import datetime


class Monitor(ABC):
    """
    Base class for all monitors.
    
    Subclasses must implement:
    - fetch_data(): Retrieve the data to display
    - format_output(data): Format data for display
    
    Optional metadata (for future dashboard launcher):
    - DASHBOARD_META dict with name, size, category, priority
    """
    
    def __init__(self, name, refresh_interval=5):
        """
        Args:
            name: Display name for this monitor
            refresh_interval: Seconds between updates
        """
        self.name = name
        self.refresh_interval = refresh_interval
        self._running = False
    
    @abstractmethod
    def fetch_data(self):
        """
        Fetch data to display. Override this in subclass.
        
        Returns:
            Any data structure your monitor needs
        
        Raises:
            Exception: If data fetch fails
        """
        pass
    
    @abstractmethod
    def format_output(self, data):
        """
        Format data for display. Override this in subclass.
        
        Args:
            data: The data returned by fetch_data()
        
        Returns:
            str: Formatted string to display
        """
        pass
    
    def clear_screen(self):
        """Clear terminal screen"""
        print("\033[2J\033[H", end="")
    
    def colorize(self, text, color):
        """
        Add ANSI color to text
        
        Args:
            text: Text to colorize
            color: One of 'red', 'green', 'yellow', 'blue', 'cyan', 'magenta'
        
        Returns:
            str: Colored text with reset code
        """
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'magenta': '\033[95m',
            'white': '\033[97m',
            'reset': '\033[0m'
        }
        return f"{colors.get(color, '')}{text}{colors['reset']}"
    
    def get_timestamp(self):
        """Get formatted current timestamp"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def render_header(self):
        """Render the monitor header"""
        timestamp = self.get_timestamp()
        separator = "=" * 60
        
        return f"""{separator}
{self.name}
Time: {timestamp}
{separator}
"""
    
    def run(self):
        """
        Main loop - renders monitor continuously.
        Press Ctrl+C to exit.
        """
        self._running = True
        
        try:
            while self._running:
                self.clear_screen()
                print(self.render_header())
                
                try:
                    data = self.fetch_data()
                    output = self.format_output(data)
                    print(output)
                except Exception as e:
                    error_msg = self.colorize(f"Error: {e}", 'red')
                    print(error_msg)
                
                print(f"\n{self.colorize('Refresh interval: ' + str(self.refresh_interval) + 's', 'cyan')}")
                print(self.colorize("Press Ctrl+C to exit", 'cyan'))
                
                time.sleep(self.refresh_interval)
                
        except KeyboardInterrupt:
            self._running = False
            print("\n" + self.colorize("Exiting...", 'yellow'))
            sys.exit(0)
    
    def stop(self):
        """Stop the monitor loop"""
        self._running = False
