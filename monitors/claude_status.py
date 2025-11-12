#!/usr/bin/env python3
"""
Claude Status Monitor
Displays Claude service status from status.claude.com API
"""
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor import Monitor


class ClaudeStatusMonitor(Monitor):
    """Monitor Claude service status"""
    
    DASHBOARD_META = {
        'name': 'Claude Status',
        'size': 'large',
        'category': 'services',
        'priority': 'high'
    }
    
    def __init__(self):
        super().__init__("Claude Status Monitor", refresh_interval=30)
        self.api_base = "https://status.claude.com/api/v2"
    
    def fetch_data(self):
        """Fetch Claude status from API"""
        data = {}
        
        # Get overall status
        try:
            result = subprocess.run(
                ['curl', '-s', f'{self.api_base}/status.json'],
                capture_output=True,
                text=True,
                timeout=5
            )
            status_data = json.loads(result.stdout)
            data['overall'] = status_data.get('status', {})
        except Exception as e:
            data['overall_error'] = str(e)
        
        # Get component statuses
        try:
            result = subprocess.run(
                ['curl', '-s', f'{self.api_base}/components.json'],
                capture_output=True,
                text=True,
                timeout=5
            )
            comp_data = json.loads(result.stdout)
            data['components'] = comp_data.get('components', [])
        except Exception as e:
            data['components_error'] = str(e)
        
        # Get recent incidents
        try:
            result = subprocess.run(
                ['curl', '-s', f'{self.api_base}/incidents.json?per_page=3'],
                capture_output=True,
                text=True,
                timeout=5
            )
            inc_data = json.loads(result.stdout)
            data['incidents'] = inc_data.get('incidents', [])
        except Exception as e:
            data['incidents_error'] = str(e)
        
        return data
    
    def format_output(self, data):
        """Format status for display"""
        output = []
        
        # Overall Status
        if 'overall' in data:
            overall = data['overall']
            indicator = overall.get('indicator', 'unknown')
            description = overall.get('description', 'Unknown')
            
            # Color based on indicator
            if indicator == 'none':
                status_color = 'green'
                status_icon = '✅'
            elif indicator == 'minor':
                status_color = 'yellow'
                status_icon = '⚠️'
            elif indicator in ['major', 'critical']:
                status_color = 'red'
                status_icon = '🔴'
            else:
                status_color = 'white'
                status_icon = '❓'
            
            status_text = f"{status_icon} {description}"
            output.append(self.colorize(status_text, status_color))
            output.append("")
        
        # Component Statuses
        if 'components' in data:
            output.append(self.colorize("Services:", 'cyan'))
            for comp in data['components']:
                name = comp.get('name', 'Unknown')
                status = comp.get('status', 'unknown')
                
                # Status icon and color
                if status == 'operational':
                    icon = '✓'
                    color = 'green'
                elif status == 'degraded_performance':
                    icon = '⚠'
                    color = 'yellow'
                elif status == 'partial_outage':
                    icon = '!'
                    color = 'yellow'
                elif status == 'major_outage':
                    icon = '✗'
                    color = 'red'
                else:
                    icon = '?'
                    color = 'white'
                
                status_display = f"  [{icon}] {name}"
                output.append(self.colorize(status_display, color))
            
            output.append("")
        
        # Recent Incidents
        if 'incidents' in data and data['incidents']:
            output.append(self.colorize("Recent Incidents:", 'cyan'))
            
            for incident in data['incidents'][:3]:
                name = incident.get('name', 'Unknown')
                status = incident.get('status', 'unknown')
                impact = incident.get('impact', 'unknown')
                created = incident.get('created_at', '')
                
                # Parse timestamp
                try:
                    dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    time_str = dt.strftime('%Y-%m-%d %H:%M UTC')
                except:
                    time_str = created
                
                # Status color
                if status == 'resolved':
                    status_color = 'green'
                elif status == 'monitoring':
                    status_color = 'yellow'
                else:
                    status_color = 'red'
                
                # Impact indicator
                if impact == 'minor':
                    impact_icon = '⚠'
                elif impact in ['major', 'critical']:
                    impact_icon = '🔴'
                else:
                    impact_icon = 'ℹ'
                
                inc_text = f"  {impact_icon} {name}"
                output.append(self.colorize(inc_text, status_color))
                output.append(f"     Status: {status} | {time_str}")
            
            output.append("")
        elif 'incidents' in data:
            output.append(self.colorize("No recent incidents", 'green'))
            output.append("")
        
        # Errors
        if 'overall_error' in data:
            output.append(self.colorize(f"Status Error: {data['overall_error']}", 'red'))
        if 'components_error' in data:
            output.append(self.colorize(f"Components Error: {data['components_error']}", 'red'))
        if 'incidents_error' in data:
            output.append(self.colorize(f"Incidents Error: {data['incidents_error']}", 'red'))
        
        return '\n'.join(output)


if __name__ == "__main__":
    ClaudeStatusMonitor().run()
