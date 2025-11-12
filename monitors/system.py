#!/usr/bin/env python3
"""
System Resource Monitor - Smooth Version
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor import Monitor


class SystemMonitor(Monitor):
    DASHBOARD_META = {
        'name': 'System Resources',
        'size': 'medium',
        'category': 'system',
        'priority': 'high'
    }
    
    def __init__(self):
        super().__init__("System Resource Monitor", refresh_interval=2)
    
    def fetch_data(self):
        data = {}
        
        # CPU
        try:
            top_output = subprocess.run(['top', '-bn1'], capture_output=True, text=True, timeout=2)
            for line in top_output.stdout.split('\n'):
                if 'Cpu(s)' in line:
                    parts = line.split(',')
                    for part in parts:
                        if 'id' in part:
                            idle = float(part.split()[0])
                            data['cpu_usage'] = 100 - idle
                            break
        except Exception as e:
            data['cpu_usage'] = f"Error: {e}"
        
        # Memory
        try:
            mem_output = subprocess.run(['free', '-h'], capture_output=True, text=True, timeout=2)
            lines = mem_output.stdout.split('\n')
            if len(lines) > 1:
                mem_line = lines[1].split()
                data['mem_total'] = mem_line[1]
                data['mem_used'] = mem_line[2]
                data['mem_available'] = mem_line[6] if len(mem_line) > 6 else mem_line[3]
        except Exception as e:
            data['mem_error'] = str(e)
        
        # Disk
        try:
            df_output = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=2)
            lines = df_output.stdout.split('\n')
            if len(lines) > 1:
                disk_line = lines[1].split()
                data['disk_total'] = disk_line[1]
                data['disk_used'] = disk_line[2]
                data['disk_available'] = disk_line[3]
                data['disk_percent'] = disk_line[4]
        except Exception as e:
            data['disk_error'] = str(e)
        
        return data
    
    def format_output(self, data):
        output = []
        
        # CPU
        if 'cpu_usage' in data:
            cpu = data['cpu_usage']
            if isinstance(cpu, (int, float)):
                color = 'green' if cpu < 70 else 'yellow' if cpu < 90 else 'red'
                cpu_str = self.colorize(f"{cpu:.1f}%", color)
            else:
                cpu_str = str(cpu)
            output.append(f"CPU Usage: {cpu_str}")
        
        # Memory
        if 'mem_total' in data:
            output.append(f"\nMemory:")
            output.append(f"  Total:     {data['mem_total']}")
            output.append(f"  Used:      {data['mem_used']}")
            output.append(f"  Available: {data['mem_available']}")
        
        # Disk
        if 'disk_total' in data:
            output.append(f"\nDisk (/):")
            output.append(f"  Total:     {data['disk_total']}")
            output.append(f"  Used:      {data['disk_used']}")
            output.append(f"  Available: {data['disk_available']}")
            output.append(f"  Usage:     {data['disk_percent']}")
        
        return '\n'.join(output)


if __name__ == "__main__":
    SystemMonitor().run()
