#!/usr/bin/env python3
"""
GPU Monitor
Displays NVIDIA GPU stats using nvidia-smi
"""
import subprocess
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor import Monitor


class GPUMonitor(Monitor):
    """Monitor NVIDIA GPU usage"""
    
    # Optional: Metadata for future dashboard launcher
    DASHBOARD_META = {
        'name': 'GPU Stats',
        'size': 'medium',
        'category': 'hardware',
        'priority': 'high'
    }
    
    def __init__(self):
        super().__init__("GPU Monitor", refresh_interval=1)
    
    def fetch_data(self):
        """Fetch GPU stats using nvidia-smi"""
        try:
            result = subprocess.run(
                ['nvidia-smi', 
                 '--query-gpu=index,name,utilization.gpu,temperature.gpu,memory.used,memory.total,power.draw',
                 '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode != 0:
                raise Exception("nvidia-smi failed")
            
            # Parse output (can be multiple GPUs)
            gpus = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 6:
                        gpus.append({
                            'index': parts[0],
                            'name': parts[1],
                            'utilization': float(parts[2]),
                            'temperature': float(parts[3]),
                            'memory_used': float(parts[4]),
                            'memory_total': float(parts[5]),
                            'power': float(parts[6]) if len(parts) > 6 else None
                        })
            
            return gpus
            
        except FileNotFoundError:
            raise Exception("nvidia-smi not found - is NVIDIA driver installed?")
        except Exception as e:
            raise Exception(f"Failed to fetch GPU stats: {e}")
    
    def format_output(self, gpus):
        """Format GPU stats for display"""
        if not gpus:
            return self.colorize("No GPUs detected", 'yellow')
        
        output = []
        
        for gpu in gpus:
            # GPU header
            gpu_index = gpu['index']
            gpu_name = gpu['name']
            header = f'GPU {gpu_index}: {gpu_name}'
            output.append(f"\n{self.colorize(header, 'cyan')}")
            
            # Utilization (color based on usage)
            util = gpu['utilization']
            util_color = 'green' if util < 50 else 'yellow' if util < 80 else 'red'
            util_text = f'{util:.0f}%'
            output.append(f"  Utilization: {self.colorize(util_text, util_color)}")
            
            # Temperature (color based on heat)
            temp = gpu['temperature']
            temp_color = 'green' if temp < 60 else 'yellow' if temp < 80 else 'red'
            temp_text = f'{temp:.0f}°C'
            output.append(f"  Temperature: {self.colorize(temp_text, temp_color)}")
            
            # Memory (convert MiB to MB for display)
            mem_used_mb = gpu['memory_used'] * 1.04858
            mem_total_mb = gpu['memory_total'] * 1.04858
            mem_percent = (gpu['memory_used'] / gpu['memory_total'] * 100) if gpu['memory_total'] > 0 else 0
            mem_color = 'green' if mem_percent < 70 else 'yellow' if mem_percent < 90 else 'red'
            
            mem_text = f'{mem_used_mb:.0f} MB'
            output.append(f"  Memory:      {self.colorize(mem_text, mem_color)} / {mem_total_mb:.0f} MB ({mem_percent:.0f}%)")
            output.append(f"               {gpu['memory_used']:.0f} MiB / {gpu['memory_total']:.0f} MiB")
            
            # Power (if available)
            if gpu['power'] is not None:
                output.append(f"  Power:       {gpu['power']:.1f} W")
        
        return '\n'.join(output)


if __name__ == "__main__":
    GPUMonitor().run()
