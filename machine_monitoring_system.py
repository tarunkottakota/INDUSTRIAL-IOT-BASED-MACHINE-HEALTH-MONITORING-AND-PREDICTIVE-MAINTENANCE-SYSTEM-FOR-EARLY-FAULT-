"""
Industrial IoT-Based Machine Health Monitoring and Predictive Maintenance System
For Early Fault Detection and Optimal Equipment Performance
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 10

class VibrationSensor:
    """Simulates IoT vibration monitoring sensors"""
    
    def __init__(self, sensor_id, machine_id, axis='X'):
        self.sensor_id = sensor_id
        self.machine_id = machine_id
        self.axis = axis  # X, Y, or Z axis
        self.current_reading = 0.0
        self.measurement_history = []
        self.sensor_status = 'normal'  # normal, warning, critical
        self.normal_range = (0.5, 2.0)  # mm/s
        
    def read_vibration(self, base_vibration, load_factor=0, fault_factor=0):
        """
        Read vibration level with realistic sensor characteristics
        base_vibration: baseline vibration level
        load_factor: machine load (0-1)
        fault_factor: fault development stage (0-1)
        Returns: measured_vibration (float)
        """
        # Simulate sensor noise
        noise = np.random.normal(0, 0.1)
        
        # Calculate affected reading based on load and fault
        affected_reading = base_vibration + (load_factor * 1.5) + (fault_factor * 3.0) + noise
        affected_reading = max(0.1, affected_reading)
        
        self.current_reading = affected_reading
        
        self.measurement_history.append({
            'timestamp': datetime.now(),
            'value': affected_reading,
            'sensor_id': self.sensor_id,
            'machine_id': self.machine_id,
            'axis': self.axis
        })
        
        return affected_reading


class TemperatureSensor:
    """Simulates IoT temperature monitoring sensors"""
    
    def __init__(self, sensor_id, machine_id, location='bearing'):
        self.sensor_id = sensor_id
        self.machine_id = machine_id
        self.location = location  # bearing, motor, gearbox
        self.current_reading = 0.0
        self.measurement_history = []
        self.sensor_status = 'normal'
        self.normal_range = (20, 60)  # Celsius
        
    def read_temperature(self, base_temp, load_factor=0, fault_factor=0):
        """
        Read temperature with realistic sensor characteristics
        base_temp: baseline temperature
        load_factor: machine load (0-1)
        fault_factor: fault development stage (0-1)
        Returns: measured_temperature (float)
        """
        # Simulate sensor noise
        noise = np.random.normal(0, 0.5)
        
        # Calculate affected reading
        affected_reading = base_temp + (load_factor * 8) + (fault_factor * 15) + noise
        affected_reading = max(15, affected_reading)
        
        self.current_reading = affected_reading
        
        self.measurement_history.append({
            'timestamp': datetime.now(),
            'value': affected_reading,
            'sensor_id': self.sensor_id,
            'machine_id': self.machine_id,
            'location': self.location
        })
        
        return affected_reading


class CurrentSensor:
    """Simulates IoT current/power monitoring sensors"""
    
    def __init__(self, sensor_id, machine_id, phase='A'):
        self.sensor_id = sensor_id
        self.machine_id = machine_id
        self.phase = phase  # A, B, C
        self.current_reading = 0.0
        self.measurement_history = []
        self.sensor_status = 'normal'
        self.normal_range = (5, 15)  # Amperes
        
    def read_current(self, base_current, load_factor=0, fault_factor=0):
        """
        Read electrical current with realistic sensor characteristics
        base_current: baseline current
        load_factor: machine load (0-1)
        fault_factor: fault development stage (0-1)
        Returns: measured_current (float)
        """
        # Simulate sensor noise
        noise = np.random.normal(0, 0.2)
        
        # Calculate affected reading
        affected_reading = base_current + (load_factor * 3) + (fault_factor * 4) + noise
        affected_reading = max(1, affected_reading)
        
        self.current_reading = affected_reading
        
        self.measurement_history.append({
            'timestamp': datetime.now(),
            'value': affected_reading,
            'sensor_id': self.sensor_id,
            'machine_id': self.machine_id,
            'phase': self.phase
        })
        
        return affected_reading


class FaultDetectionEngine:
    """Manages fault detection and predictive maintenance alerts"""
    
    def __init__(self, vibration_threshold=None, temp_threshold=None, current_threshold=None):
        self.vibration_threshold = vibration_threshold or {'warning': 3.0, 'critical': 5.0}
        self.temp_threshold = temp_threshold or {'warning': 70, 'critical': 85}
        self.current_threshold = current_threshold or {'warning': 18, 'critical': 22}
        self.alerts = []
        self.alert_history = []
        self.fault_predictions = []
        
    def evaluate_vibration(self, machine_id, measured_value, current_time):
        """Evaluate vibration and generate alerts"""
        alert_info = None
        severity = 'normal'
        
        if measured_value > self.vibration_threshold['critical']:
            severity = 'critical'
        elif measured_value > self.vibration_threshold['warning']:
            severity = 'high'
        elif measured_value > 2.5:
            severity = 'medium'
            
        if severity != 'normal':
            alert_info = {
                'timestamp': current_time,
                'machine_id': machine_id,
                'sensor_type': 'vibration',
                'measured_value': measured_value,
                'severity': severity,
                'message': f"{severity.upper()} ALERT: Machine {machine_id} - Vibration is {measured_value:.2f} mm/s"
            }
            
            self.alerts.append(alert_info)
            self.alert_history.append(alert_info)
        
        return alert_info
    
    def evaluate_temperature(self, machine_id, measured_value, current_time):
        """Evaluate temperature and generate alerts"""
        alert_info = None
        severity = 'normal'
        
        if measured_value > self.temp_threshold['critical']:
            severity = 'critical'
        elif measured_value > self.temp_threshold['warning']:
            severity = 'high'
        elif measured_value > 65:
            severity = 'medium'
            
        if severity != 'normal':
            alert_info = {
                'timestamp': current_time,
                'machine_id': machine_id,
                'sensor_type': 'temperature',
                'measured_value': measured_value,
                'severity': severity,
                'message': f"{severity.upper()} ALERT: Machine {machine_id} - Temperature is {measured_value:.1f}°C"
            }
            
            self.alerts.append(alert_info)
            self.alert_history.append(alert_info)
        
        return alert_info
    
    def evaluate_current(self, machine_id, measured_value, current_time):
        """Evaluate electrical current and generate alerts"""
        alert_info = None
        severity = 'normal'
        
        if measured_value > self.current_threshold['critical']:
            severity = 'critical'
        elif measured_value > self.current_threshold['warning']:
            severity = 'high'
        elif measured_value > 16:
            severity = 'medium'
            
        if severity != 'normal':
            alert_info = {
                'timestamp': current_time,
                'machine_id': machine_id,
                'sensor_type': 'current',
                'measured_value': measured_value,
                'severity': severity,
                'message': f"{severity.upper()} ALERT: Machine {machine_id} - Current is {measured_value:.2f} A"
            }
            
            self.alerts.append(alert_info)
            self.alert_history.append(alert_info)
        
        return alert_info


class MachineProfile:
    """Represents an industrial machine with health monitoring"""
    
    def __init__(self, machine_id, machine_name, machine_type='pump'):
        self.machine_id = machine_id
        self.machine_name = machine_name
        self.machine_type = machine_type  # pump, motor, compressor, conveyor
        self.sensors = {}
        self.fault_engine = FaultDetectionEngine()
        self.machine_status = 'healthy'  # healthy, degraded, critical
        self.health_score = 100.0
        self.maintenance_due = False
        self.total_alerts = 0
        self.fault_development = 0.0  # 0-1 scale
        
    def add_sensor(self, sensor_id, sensor_type, **kwargs):
        """Add a sensor to the machine"""
        if sensor_type == 'vibration':
            self.sensors[sensor_id] = VibrationSensor(sensor_id, self.machine_id, kwargs.get('axis', 'X'))
        elif sensor_type == 'temperature':
            self.sensors[sensor_id] = TemperatureSensor(sensor_id, self.machine_id, kwargs.get('location', 'bearing'))
        elif sensor_type == 'current':
            self.sensors[sensor_id] = CurrentSensor(sensor_id, self.machine_id, kwargs.get('phase', 'A'))
    
    def evaluate_machine_health(self, current_time):
        """Evaluate overall machine health status"""
        active_alerts = len([a for a in self.fault_engine.alerts if 
                           (current_time - a['timestamp']).total_seconds() < 600])
        
        # Calculate health score based on alerts
        if active_alerts == 0:
            self.health_score = 100.0
            self.machine_status = 'healthy'
        elif active_alerts < 3:
            self.health_score = 80.0 - (active_alerts * 5)
            self.machine_status = 'degraded'
        else:
            self.health_score = max(20.0, 60.0 - (active_alerts * 8))
            self.machine_status = 'critical'
        
        # Determine if maintenance is due
        critical_alerts = len([a for a in self.fault_engine.alerts if 
                             a['severity'] == 'critical' and 
                             (current_time - a['timestamp']).total_seconds() < 600])
        
        self.maintenance_due = critical_alerts > 0 or self.health_score < 40


class PredictiveMaintenanceSystem:
    """Main system managing industrial machine health monitoring"""
    
    def __init__(self, system_name='Machine Health Monitoring System'):
        self.system_name = system_name
        self.machines = {}
        self.system_status = 'operational'  # operational, maintenance, offline
        self.daily_statistics = []
        self.all_alerts = []
        self.maintenance_schedule = []
        
    def add_machine(self, machine_id, machine_name, machine_type='pump'):
        """Add a machine to the monitoring system"""
        self.machines[machine_id] = MachineProfile(machine_id, machine_name, machine_type)
        
    def simulate_monitoring_day(self, date=None, num_intervals=96):
        """
        Simulate a full day of machine monitoring with 15-minute intervals
        """
        if date is None:
            date = datetime.now().date()
        
        daily_data = []
        total_alerts = 0
        critical_alerts = 0
        maintenance_required = 0
        
        for interval in range(num_intervals):
            quarter_hour = (interval * 15) / 60
            hour = int(quarter_hour)
            minutes = int((quarter_hour % 1) * 60)
            
            current_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=quarter_hour)
            
            for machine_id, machine in self.machines.items():
                # Generate realistic operating parameters based on time of day
                load_factor = self._generate_load_factor(hour)
                
                # Simulate fault development over time (for demonstration)
                machine.fault_development = min(1.0, machine.fault_development + np.random.uniform(0, 0.01))
                
                # Process each sensor for the machine
                for sensor_id, sensor in machine.sensors.items():
                    if isinstance(sensor, VibrationSensor):
                        base_vib = self._get_base_vibration(machine.machine_type)
                        measured_vib = sensor.read_vibration(base_vib, load_factor, machine.fault_development)
                        alert = machine.fault_engine.evaluate_vibration(machine_id, measured_vib, current_time)
                        if alert:
                            total_alerts += 1
                            if alert['severity'] == 'critical':
                                critical_alerts += 1
                            self.all_alerts.append(alert)
                            
                    elif isinstance(sensor, TemperatureSensor):
                        base_temp = self._get_base_temperature(machine.machine_type)
                        measured_temp = sensor.read_temperature(base_temp, load_factor, machine.fault_development)
                        alert = machine.fault_engine.evaluate_temperature(machine_id, measured_temp, current_time)
                        if alert:
                            total_alerts += 1
                            if alert['severity'] == 'critical':
                                critical_alerts += 1
                            self.all_alerts.append(alert)
                            
                    elif isinstance(sensor, CurrentSensor):
                        base_current = self._get_base_current(machine.machine_type)
                        measured_current = sensor.read_current(base_current, load_factor, machine.fault_development)
                        alert = machine.fault_engine.evaluate_current(machine_id, measured_current, current_time)
                        if alert:
                            total_alerts += 1
                            if alert['severity'] == 'critical':
                                critical_alerts += 1
                            self.all_alerts.append(alert)
                
                # Evaluate machine health
                machine.evaluate_machine_health(current_time)
                if machine.maintenance_due:
                    maintenance_required += 1
                
                daily_data.append({
                    'date': date,
                    'time': f"{hour:02d}:{minutes:02d}",
                    'hour': hour,
                    'machine_id': machine_id,
                    'machine_name': machine.machine_name,
                    'machine_type': machine.machine_type,
                    'machine_status': machine.machine_status,
                    'health_score': machine.health_score,
                    'maintenance_due': machine.maintenance_due,
                    'active_alerts': len(machine.fault_engine.alerts)
                })
        
        self.daily_statistics.append({
            'date': date,
            'total_alerts': total_alerts,
            'critical_alerts': critical_alerts,
            'maintenance_required': maintenance_required,
            'num_machines': len(self.machines),
            'system_status': self.system_status
        })
        
        return pd.DataFrame(daily_data)
    
    def _generate_load_factor(self, hour):
        """Generate realistic machine load patterns"""
        if 6 <= hour < 18:  # Day shift
            return np.random.uniform(0.6, 0.95)
        elif 18 <= hour < 22:  # Evening shift
            return np.random.uniform(0.4, 0.8)
        else:  # Night shift
            return np.random.uniform(0.1, 0.5)
    
    def _get_base_vibration(self, machine_type):
        """Get baseline vibration for machine type"""
        vibration_map = {
            'pump': np.random.normal(1.2, 0.2),
            'motor': np.random.normal(1.5, 0.3),
            'compressor': np.random.normal(1.8, 0.3),
            'conveyor': np.random.normal(0.8, 0.2)
        }
        return vibration_map.get(machine_type, 1.0)
    
    def _get_base_temperature(self, machine_type):
        """Get baseline temperature for machine type"""
        temp_map = {
            'pump': np.random.normal(45, 3),
            'motor': np.random.normal(50, 4),
            'compressor': np.random.normal(55, 5),
            'conveyor': np.random.normal(35, 2)
        }
        return temp_map.get(machine_type, 40)
    
    def _get_base_current(self, machine_type):
        """Get baseline current for machine type"""
        current_map = {
            'pump': np.random.normal(10, 1),
            'motor': np.random.normal(12, 1.5),
            'compressor': np.random.normal(14, 2),
            'conveyor': np.random.normal(8, 1)
        }
        return current_map.get(machine_type, 10)
    
    def get_system_report(self):
        """Generate comprehensive system report"""
        report = {
            'system_name': self.system_name,
            'total_machines': len(self.machines),
            'total_alerts': len(self.all_alerts),
            'critical_alerts': len([a for a in self.all_alerts if a['severity'] == 'critical']),
            'simulation_days': len(self.daily_statistics),
            'system_status': self.system_status,
            'avg_daily_alerts': np.mean([stat['total_alerts'] for stat in self.daily_statistics]) if self.daily_statistics else 0
        }
        return report


def generate_visualizations(system, daily_data):
    """Generate comprehensive visualizations for the report"""
    
    # 1. Machine Health Metrics
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Industrial Machine Health Monitoring - Performance Metrics', 
                 fontsize=16, fontweight='bold')
    
    # Health score by hour
    health_by_hour = daily_data.groupby('hour')['health_score'].mean()
    axes[0, 0].plot(health_by_hour.index, health_by_hour.values, marker='o', linewidth=2, 
                    markersize=6, color='#2ECC71', label='Health Score')
    axes[0, 0].axhline(y=80, color='orange', linestyle='--', linewidth=2, label='Degradation Threshold')
    axes[0, 0].axhline(y=40, color='red', linestyle='--', linewidth=2, label='Critical Threshold')
    axes[0, 0].fill_between(health_by_hour.index, health_by_hour.values, alpha=0.3, color='#2ECC71')
    axes[0, 0].set_title('Machine Health Score by Hour', fontweight='bold')
    axes[0, 0].set_ylabel('Health Score (%)')
    axes[0, 0].set_xlabel('Hour of Day')
    axes[0, 0].set_ylim([0, 105])
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Machine status distribution
    status_counts = daily_data['machine_status'].value_counts()
    colors_status = {'healthy': '#2ECC71', 'degraded': '#F39C12', 'critical': '#E74C3C'}
    colors = [colors_status.get(status, 'gray') for status in status_counts.index]
    
    axes[0, 1].bar(status_counts.index, status_counts.values, color=colors, edgecolor='black')
    axes[0, 1].set_title('Machine Status Distribution', fontweight='bold')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_xlabel('Machine Status')
    for i, v in enumerate(status_counts.values):
        axes[0, 1].text(i, v + 20, str(v), ha='center', fontweight='bold')
    
    # Maintenance requirements by hour
    maintenance_by_hour = daily_data.groupby('hour')['maintenance_due'].sum()
    axes[1, 0].bar(maintenance_by_hour.index, maintenance_by_hour.values, color='#E74C3C', 
                   edgecolor='black', alpha=0.7)
    axes[1, 0].set_title('Maintenance Requirements by Hour', fontweight='bold')
    axes[1, 0].set_ylabel('Machines Requiring Maintenance')
    axes[1, 0].set_xlabel('Hour of Day')
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Active alerts by hour
    alerts_by_hour = daily_data.groupby('hour')['active_alerts'].mean()
    axes[1, 1].plot(alerts_by_hour.index, alerts_by_hour.values, marker='s', linewidth=2.5, 
                    markersize=7, color='#E74C3C', label='Active Alerts')
    axes[1, 1].fill_between(alerts_by_hour.index, alerts_by_hour.values, alpha=0.3, color='#E74C3C')
    axes[1, 1].set_title('Average Active Alerts by Hour', fontweight='bold')
    axes[1, 1].set_ylabel('Number of Alerts')
    axes[1, 1].set_xlabel('Hour of Day')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/machine_monitoring_project/fig_health_metrics.png', dpi=300, bbox_inches='tight')
    print("Saved: fig_health_metrics.png")
    plt.close()
    
    # 2. Fault Detection Analysis
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Fault Detection and Alert Analysis', fontsize=16, fontweight='bold')
    
    # Alert types distribution
    alert_types = [a['sensor_type'] for a in system.all_alerts]
    alert_counts = pd.Series(alert_types).value_counts()
    colors_map = {'vibration': '#E74C3C', 'temperature': '#F39C12', 'current': '#3498DB'}
    colors = [colors_map.get(alert, 'gray') for alert in alert_counts.index]
    
    axes[0, 0].bar(alert_counts.index, alert_counts.values, color=colors, edgecolor='black')
    axes[0, 0].set_title('Alert Types Distribution', fontweight='bold')
    axes[0, 0].set_ylabel('Count')
    axes[0, 0].set_xlabel('Sensor Type')
    for i, v in enumerate(alert_counts.values):
        axes[0, 0].text(i, v + 10, str(v), ha='center', fontweight='bold')
    
    # Alerts by hour
    alerts_by_hour = daily_data.groupby('hour')['active_alerts'].sum()
    axes[0, 1].bar(alerts_by_hour.index, alerts_by_hour.values, color='#E74C3C', edgecolor='black', alpha=0.7)
    axes[0, 1].set_title('Total Alerts by Hour', fontweight='bold')
    axes[0, 1].set_ylabel('Number of Alerts')
    axes[0, 1].set_xlabel('Hour of Day')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Alert severity distribution
    alert_severities = [a['severity'] for a in system.all_alerts]
    severity_counts = pd.Series(alert_severities).value_counts()
    colors_severity = {'medium': '#F39C12', 'high': '#E67E22', 'critical': '#E74C3C'}
    colors = [colors_severity.get(sev, 'gray') for sev in severity_counts.index]
    
    axes[1, 0].pie(severity_counts.values, labels=severity_counts.index, autopct='%1.1f%%',
                   colors=colors, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    axes[1, 0].set_title('Alert Severity Distribution', fontweight='bold')
    
    # Machine-wise alert count
    machine_alerts = daily_data.groupby('machine_name')['active_alerts'].sum()
    axes[1, 1].barh(machine_alerts.index, machine_alerts.values, color='#E74C3C', edgecolor='black')
    axes[1, 1].set_title('Total Alerts by Machine', fontweight='bold')
    axes[1, 1].set_xlabel('Number of Alerts')
    for i, v in enumerate(machine_alerts.values):
        axes[1, 1].text(v + 5, i, str(int(v)), va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/machine_monitoring_project/fig_fault_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: fig_fault_analysis.png")
    plt.close()
    
    # 3. System Architecture Diagram
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    ax.text(0.5, 0.95, 'Industrial IoT Machine Health Monitoring System Architecture', 
            ha='center', fontsize=16, fontweight='bold', transform=ax.transAxes)
    
    components = [
        ('Vibration\nSensor', 0.15, 0.75),
        ('Temperature\nSensor', 0.5, 0.75),
        ('Current\nSensor', 0.85, 0.75),
        ('IoT\nCommunication\nModule', 0.5, 0.55),
        ('Cloud\nServer', 0.15, 0.35),
        ('Fault\nDetection', 0.5, 0.35),
        ('Maintenance\nScheduler', 0.85, 0.35),
    ]
    
    for label, x, y in components:
        bbox = dict(boxstyle='round,pad=0.6', facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.text(x, y, label, ha='center', va='center', fontsize=11, fontweight='bold',
                transform=ax.transAxes, bbox=bbox)
    
    connections = [
        ((0.25, 0.75), (0.4, 0.75)),
        ((0.6, 0.75), (0.75, 0.75)),
        ((0.5, 0.65), (0.5, 0.60)),
        ((0.25, 0.65), (0.25, 0.60)),
        ((0.75, 0.65), (0.75, 0.60)),
    ]
    
    for start, end in connections:
        ax.annotate('', xy=end, xytext=start, transform=ax.transAxes,
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    features_text = 'Key Features:\n• Real-time Machine Condition Monitoring\n• Multi-sensor Data Fusion\n• Predictive Fault Detection\n• Automated Maintenance Scheduling\n• Industry 4.0 Compliance'
    ax.text(0.5, 0.15, features_text, ha='center', va='top', fontsize=10,
            transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='lightyellow', 
            edgecolor='black', linewidth=1.5))
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/machine_monitoring_project/fig_system_architecture.png', dpi=300, bbox_inches='tight')
    print("Saved: fig_system_architecture.png")
    plt.close()
    
    # 4. Daily Performance
    fig, ax = plt.subplots(figsize=(12, 6))
    
    daily_stats = pd.DataFrame(system.daily_statistics)
    
    x = np.arange(len(daily_stats))
    width = 0.35
    
    ax.bar(x - width/2, daily_stats['total_alerts'], width, label='Total Alerts', 
           color='#F39C12', edgecolor='black')
    ax2 = ax.twinx()
    ax2.bar(x + width/2, daily_stats['critical_alerts'], width, label='Critical Alerts', 
            color='#E74C3C', alpha=0.7, edgecolor='black')
    
    ax.set_xlabel('Day', fontweight='bold')
    ax.set_ylabel('Total Alerts', fontweight='bold', color='#F39C12')
    ax2.set_ylabel('Critical Alerts', fontweight='bold', color='#E74C3C')
    ax.set_title('Daily System Performance and Alert Trends', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([f"Day {i+1}" for i in range(len(daily_stats))])
    ax.grid(True, alpha=0.3, axis='y')
    
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/machine_monitoring_project/fig_daily_performance.png', dpi=300, bbox_inches='tight')
    print("Saved: fig_daily_performance.png")
    plt.close()
    
    # 5. Machine Condition Heatmap
    fig, ax = plt.subplots(figsize=(12, 6))
    
    machine_activity = daily_data.pivot_table(values='health_score', index='machine_name', 
                                             columns='hour', aggfunc='mean', fill_value=0)
    
    sns.heatmap(machine_activity, cmap='RdYlGn', annot=True, fmt='.0f', cbar_kws={'label': 'Health Score'},
                ax=ax, linewidths=0.5, linecolor='gray', vmin=0, vmax=100)
    ax.set_title('Machine Health Score Heatmap - Health by Machine and Hour', fontweight='bold', fontsize=14)
    ax.set_xlabel('Hour of Day', fontweight='bold')
    ax.set_ylabel('Machine Name', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/machine_monitoring_project/fig_health_heatmap.png', dpi=300, bbox_inches='tight')
    print("Saved: fig_health_heatmap.png")
    plt.close()


def main():
    """Main execution function"""
    print("=" * 70)
    print("INDUSTRIAL IOT-BASED MACHINE HEALTH MONITORING SYSTEM SIMULATION")
    print("=" * 70)
    
    # Initialize system
    system = PredictiveMaintenanceSystem("Industrial Machine Health Monitoring System")
    
    # Add machines with different types
    machines_config = {
        'MACH-001': {'name': 'Centrifugal Pump A', 'type': 'pump'},
        'MACH-002': {'name': 'Electric Motor B', 'type': 'motor'},
        'MACH-003': {'name': 'Air Compressor C', 'type': 'compressor'},
        'MACH-004': {'name': 'Conveyor System D', 'type': 'conveyor'},
        'MACH-005': {'name': 'Rotary Pump E', 'type': 'pump'},
    }
    
    for machine_id, config in machines_config.items():
        system.add_machine(machine_id, config['name'], config['type'])
        machine = system.machines[machine_id]
        
        # Add sensors to each machine
        machine.add_sensor(f"{machine_id}-VIB-X", 'vibration', axis='X')
        machine.add_sensor(f"{machine_id}-VIB-Y", 'vibration', axis='Y')
        machine.add_sensor(f"{machine_id}-TEMP-B", 'temperature', location='bearing')
        machine.add_sensor(f"{machine_id}-CURR-A", 'current', phase='A')
    
    print(f"\nSystem initialized with {len(machines_config)} machines:")
    for machine_id, config in machines_config.items():
        print(f"  - {machine_id}: {config['name']} ({config['type']})")
    
    # Simulate 7 days
    print("\nSimulating 7 days of machine monitoring...")
    all_data = []
    
    for day in range(7):
        simulation_date = datetime.now().date() - timedelta(days=6-day)
        daily_data = system.simulate_monitoring_day(simulation_date)
        all_data.append(daily_data)
        
        daily_stats = system.daily_statistics[-1]
        print(f"Day {day+1}: Alerts={daily_stats['total_alerts']}, "
              f"Critical={daily_stats['critical_alerts']}, "
              f"Maintenance={daily_stats['maintenance_required']}")
    
    # Combine all data
    combined_data = pd.concat(all_data, ignore_index=True)
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    generate_visualizations(system, combined_data)
    
    # Generate report data
    report = system.get_system_report()
    
    print("\n" + "=" * 70)
    print("SYSTEM REPORT")
    print("=" * 70)
    print(f"System Name: {report['system_name']}")
    print(f"Total Machines Monitored: {report['total_machines']}")
    print(f"Total Alerts Generated: {report['total_alerts']}")
    print(f"Critical Alerts: {report['critical_alerts']}")
    print(f"Average Daily Alerts: {report['avg_daily_alerts']:.1f}")
    print(f"System Status: {report['system_status']}")
    print(f"Simulation Period: {report['simulation_days']} days")
    print("=" * 70)
    
    # Save data to CSV
    combined_data.to_csv('/home/ubuntu/machine_monitoring_project/monitoring_data.csv', index=False)
    print("\nMonitoring data saved to: monitoring_data.csv")
    
    # Save report to JSON
    report_json = {
        'system_report': report,
        'machines': list(machines_config.keys()),
        'simulation_date': datetime.now().isoformat(),
        'daily_statistics': system.daily_statistics,
        'total_alerts': len(system.all_alerts)
    }
    
    with open('/home/ubuntu/machine_monitoring_project/system_report.json', 'w') as f:
        json.dump(report_json, f, indent=2, default=str)
    
    print("System report saved to: system_report.json")
    
    return system, combined_data


if __name__ == "__main__":
    system, data = main()
