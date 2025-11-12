#!/usr/bin/env python3
"""
Process Monitor
Displays top processes by CPU or memory usage
"""
import subprocess
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor import Monitor


class ProcessMonitor(Monitor):
    """Monitor top processes"""
    
    DASHBOARD_META = {
        'name': 'Top Processes',
        'size': 'large',
        'category': 'system',
        'priority': 'medium'
    }
    
    def __init__(self, sort_by='cpu', limit=10):
        """
        Args:
            sort_by: 'cpu' or 'mem'
            limit: Number of processes to show
        """
        super().__init__("Process Monitor", refresh_interval=3)
        self.sort_by = sort_by
        self.limit = limit
    
    def fetch_data(self):
        """Fetch top processes"""
        try:
            # Use ps to get process info
            sort_flag = '-pcpu' if self.sort_by == 'cpu' else '-pmem'
            
            result = subprocess.run(
                ['ps', 'aux', '--sort=' + sort_flag],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            lines = result.stdout.strip().split('\n')
            
            # Parse header
            header = lines[0] if lines else ""
            
            # Parse processes (skip header, take top N)
            processes = []
            for line in lines[1:self.limit + 1]:
                parts = line.split(None, 10)  # Split into max 11 parts
                if len(parts) >= 11:
                    processes.append({
                        'user': parts[0],
                        'pid': parts[1],
                        'cpu': float(parts[2]),
                        'mem': float(parts[3]),
                        'vsz': parts[4],
                        'rss': parts[5],
                        'tty': parts[6],
                        'stat': parts[7],
                        'start': parts[8],
                        'time': parts[9],
                        'command': parts[10]
                    })
            
            return processes
            
        except Exception as e:
            raise Exception(f"Failed to fetch processes: {e}")
    
    def format_output(self, processes):
        """Format process list for display"""
        if not processes:
            return self.colorize("No processes found", 'yellow')
        
        output = []
        sort_label = self.sort_by.upper()
        output.append(f"Sorted by: {self.colorize(sort_label, 'cyan')}\n")
        
        # Header
        header = f"{'PID':<8} {'CPU%':<6} {'MEM%':<6} {'COMMAND':<50}"
        output.append(self.colorize(header, 'cyan'))
        output.append("-" * 70)
        
        # Processes
        for proc in processes:
            # Color code based on usage
            cpu_color = 'red' if proc['cpu'] > 50 else 'yellow' if proc['cpu'] > 20 else 'white'
            mem_color = 'red' if proc['mem'] > 50 else 'yellow' if proc['mem'] > 20 else 'white'
            
            # Truncate command if too long
            cmd = proc['command'][:47] + '...' if len(proc['command']) > 50 else proc['command']
            
            # Format each field separately to avoid nested f-string issues
            pid_field = f"{proc['pid']:<8}"
            cpu_value = f"{proc['cpu']:>5.1f}"
            cpu_field = self.colorize(cpu_value, cpu_color)
            mem_value = f"{proc['mem']:>5.1f}"
            mem_field = self.colorize(mem_value, mem_color)
            
            line = f"{pid_field} {cpu_field} {mem_field} {cmd}"
            output.append(line)
        
        return '\n'.join(output)


if __name__ == "__main__":
    # Can customize via command line args
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor top processes')
    parser.add_argument('--sort', choices=['cpu', 'mem'], default='cpu',
                       help='Sort by CPU or memory (default: cpu)')
    parser.add_argument('--limit', type=int, default=10,
                       help='Number of processes to show (default: 10)')
    
    args = parser.parse_args()
    
    ProcessMonitor(sort_by=args.sort, limit=args.limit).run()
