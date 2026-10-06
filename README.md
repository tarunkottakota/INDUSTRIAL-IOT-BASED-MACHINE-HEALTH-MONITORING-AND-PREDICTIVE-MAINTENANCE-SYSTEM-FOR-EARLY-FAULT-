# Industrial IoT-Based Machine Health Monitoring and Predictive Maintenance System

## Project Overview

This project implements a comprehensive Industrial IoT-Based Machine Health Monitoring and Predictive Maintenance System for early fault detection. The system simulates continuous monitoring of industrial machinery using IoT sensors and generates automated predictive maintenance alerts based on real-time equipment condition analysis.

## System Features

- **Multi-Sensor Integration**: Simulates realistic IoT industrial sensors for vibration, temperature, and electrical current monitoring
- **Machine Profile Management**: Supports different machine types (pumps, motors, compressors, conveyors) with type-specific operational patterns
- **Intelligent Fault Detection**: Generates alerts with severity levels (warning, critical) based on industrial thresholds
- **Real-Time Monitoring**: Continuous 24-hour simulation with 15-minute interval data collection
- **Comprehensive Analytics**: Generates visualizations for machine health trends, alert distributions, and daily performance metrics
- **Data Export**: Exports simulation results to CSV and JSON formats for further analysis

## Project Structure

```
machine_monitoring_project/
├── machine_monitoring_system.py      # Main system implementation
├── generate_report.py                # Word document report generator
├── monitoring_data.csv               # Simulation data (output)
├── system_report.json                # System statistics (output)
├── fig_health_metrics.png            # Health metrics analysis chart
├── fig_fault_analysis.png            # Fault detection analysis chart
├── fig_system_architecture.png       # System architecture diagram
├── fig_daily_performance.png         # Daily performance metrics
├── fig_health_heatmap.png            # Machine health heatmap
└── README.md                         # This file
```

## Core Classes

### 1. VibrationSensor Class

Simulates IoT vibration monitoring sensors with realistic characteristics.

**Key Methods:**
- `read_vibration(base_vibration, load_factor=0, fault_factor=0)`: Reads vibration with sensor noise and modifiers

**Attributes:**
- `sensor_id`: Unique sensor identifier
- `machine_id`: Associated machine ID
- `axis`: Monitoring axis (X, Y, or Z)
- `current_reading`: Latest measurement value (mm/s)
- `measurement_history`: Historical measurements

### 2. TemperatureSensor Class

Simulates IoT temperature monitoring sensors for industrial equipment.

**Key Methods:**
- `read_temperature(base_temp, load_factor=0, fault_factor=0)`: Reads temperature with realistic noise

**Attributes:**
- `sensor_id`: Unique sensor identifier
- `machine_id`: Associated machine ID
- `location`: Sensor location (bearing, motor, gearbox)
- `current_reading`: Latest measurement value (°C)
- `measurement_history`: Historical measurements

### 3. CurrentSensor Class

Simulates IoT electrical current monitoring sensors.

**Key Methods:**
- `read_current(base_current, load_factor=0, fault_factor=0)`: Reads electrical current with realistic noise

**Attributes:**
- `sensor_id`: Unique sensor identifier
- `machine_id`: Associated machine ID
- `phase`: Electrical phase (A, B, or C)
- `current_reading`: Latest measurement value (Amperes)
- `measurement_history`: Historical measurements

### 4. FaultDetectionEngine Class

Manages fault detection and predictive maintenance alerts with industrial thresholds.

**Key Methods:**
- `evaluate_vibration(machine_id, measured_value, current_time)`: Evaluates vibration against thresholds
- `evaluate_temperature(machine_id, measured_value, current_time)`: Evaluates temperature against thresholds
- `evaluate_current(machine_id, measured_value, current_time)`: Evaluates electrical current against thresholds

**Alert Severity Levels:**
- **Medium**: Mild deviation from normal range
- **High**: Significant deviation requiring attention
- **Critical**: Emergency condition requiring immediate intervention

**Industrial Thresholds:**
- Vibration: Low < 2.5 mm/s, Warning 2.5-3.0 mm/s, Critical > 5.0 mm/s
- Temperature: Low < 65°C, Warning 65-70°C, Critical > 85°C
- Current: Low < 16A, Warning 16-18A, Critical > 22A

### 5. MachineProfile Class

Represents an individual industrial machine with health monitoring capabilities.

**Key Methods:**
- `add_sensor(sensor_id, sensor_type, **kwargs)`: Adds a sensor to the machine
- `evaluate_machine_health(current_time)`: Evaluates overall machine health status

**Machine Condition Types:**
- **Pump**: Baseline vibration 1.2 mm/s, temperature 45°C, current 10A
- **Motor**: Baseline vibration 1.5 mm/s, temperature 50°C, current 12A
- **Compressor**: Baseline vibration 1.8 mm/s, temperature 55°C, current 14A
- **Conveyor**: Baseline vibration 0.8 mm/s, temperature 35°C, current 8A

### 6. PredictiveMaintenanceSystem Class

Main system class that orchestrates the entire monitoring platform.

**Key Methods:**
- `add_machine(machine_id, machine_name, machine_type)`: Adds a machine to the system
- `simulate_monitoring_day(date, num_intervals)`: Simulates a full day of monitoring
- `get_system_report()`: Generates comprehensive system statistics

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- Required packages: numpy, pandas, matplotlib, seaborn

### Installation Steps

1. Install required packages:
```bash
pip install numpy pandas matplotlib seaborn
```

2. Navigate to the project directory:
```bash
cd machine_monitoring_project
```

## Usage Examples

### Basic System Initialization

```python
from machine_monitoring_system import PredictiveMaintenanceSystem

# Create system instance
system = PredictiveMaintenanceSystem("Industrial Machine Health Monitoring System")

# Add a machine
system.add_machine('MACH-001', 'Centrifugal Pump A', 'pump')

# Add sensors to machine
machine = system.machines['MACH-001']
machine.add_sensor('MACH-001-VIB-X', 'vibration', axis='X')
machine.add_sensor('MACH-001-TEMP-B', 'temperature', location='bearing')
machine.add_sensor('MACH-001-CURR-A', 'current', phase='A')
```

### Running a Simulation

```python
from datetime import datetime

# Simulate a day of monitoring
simulation_date = datetime.now().date()
daily_data = system.simulate_monitoring_day(simulation_date)

# Get system report
report = system.get_system_report()
print(f"Total Alerts: {report['total_alerts']}")
print(f"Critical Events: {report['critical_alerts']}")
```

### Accessing Simulation Results

```python
# Access alert history
for alert in system.all_alerts[:5]:
    print(f"{alert['timestamp']}: {alert['message']}")

# Access machine data
df = pd.read_csv('monitoring_data.csv')
print(df.head())
```

### Generating Visualizations

```python
from machine_monitoring_system import generate_visualizations

# Generate all visualizations
generate_visualizations(system, daily_data)
```

## Simulation Parameters

### Operational Load Patterns

The system generates realistic machine load patterns based on shift schedules:

1. **Day Shift (6 AM - 6 PM)**: 60-95% load
2. **Evening Shift (6 PM - 10 PM)**: 40-80% load
3. **Night Shift (10 PM - 6 AM)**: 10-50% load

### Data Collection Interval

- **Frequency**: Every 15 minutes
- **Daily Data Points**: 96 per machine
- **Weekly Data Points**: 672 per machine

### Fault Development

The system simulates progressive fault development over time, with a fault factor that increases gradually from 0 to 1 over the simulation period, representing equipment degradation.

## Output Files

### CSV Export (monitoring_data.csv)

Contains raw simulation data with columns:
- `date`: Simulation date
- `time`: Time of measurement (HH:MM format)
- `hour`: Hour of day (0-23)
- `machine_id`: Machine identifier
- `machine_name`: Machine name
- `machine_type`: Machine type (pump, motor, compressor, conveyor)
- `machine_status`: Current health status (healthy/degraded/critical)
- `health_score`: Machine health percentage (0-100)
- `maintenance_due`: Boolean indicating if maintenance is required
- `active_alerts`: Number of active alerts

### JSON Export (system_report.json)

Contains system statistics:
- Total machines monitored
- Total alerts generated
- Critical events detected
- Average daily alerts
- Daily statistics breakdown

### Visualizations

1. **fig_health_metrics.png**: 4-panel analysis of health scores, status distribution, maintenance requirements, and active alerts
2. **fig_fault_analysis.png**: Alert types distribution, hourly trends, severity distribution, and machine-wise alert count
3. **fig_system_architecture.png**: System component diagram showing data flow
4. **fig_daily_performance.png**: Daily alert trends and critical events
5. **fig_health_heatmap.png**: Machine health score heatmap by hour

## Industrial Thresholds and Alert Logic

The system uses evidence-based industrial thresholds for alert generation:

### Vibration Monitoring (mm/s)
- **Normal Range**: 0.5-2.5 mm/s
- **Warning**: 2.5-3.0 mm/s
- **Critical**: > 5.0 mm/s

### Temperature Monitoring (°C)
- **Normal Range**: 35-65°C
- **Warning**: 65-70°C
- **Critical**: > 85°C

### Electrical Current Monitoring (Amperes)
- **Normal Range**: 5-16A
- **Warning**: 16-18A
- **Critical**: > 22A

## Performance Metrics

### System Capabilities

- **Data Processing**: Processes 3,360 data points (5 machines × 96 intervals × 7 days) in < 5 seconds
- **Alert Generation**: Generates ~1,370 alerts per day across all machines
- **Scalability**: Supports up to 100+ machines with minimal performance impact

### Simulation Results (7-Day Period)

- **Total Alerts**: 9,592
- **Critical Events**: 3,353
- **Average Daily Alerts**: 1,370.3
- **Machines Monitored**: 5
- **Data Points Generated**: 3,360

## Future Enhancements

1. **Real IoT Integration**: Connect to actual industrial sensors via MQTT, OPC UA, or Modbus
2. **Machine Learning**: Implement predictive analytics for Remaining Useful Life (RUL) prediction
3. **Mobile Application**: Develop cross-platform app for real-time notifications
4. **ERP Integration**: Connect with Enterprise Resource Planning systems for automated work orders
5. **Advanced Sensors**: Add acoustic emission, oil analysis, and ultrasonic leak detection
6. **Cloud Deployment**: Deploy on AWS/Azure for scalable industrial services

## Troubleshooting

### Common Issues

**Issue**: Matplotlib visualization errors
- **Solution**: Ensure matplotlib backend is properly configured: `matplotlib.use('Agg')`

**Issue**: Memory errors with large datasets
- **Solution**: Reduce simulation period or number of machines

**Issue**: Missing CSV/JSON files
- **Solution**: Ensure write permissions in the project directory

## Security Considerations

In a production environment, the following security measures should be implemented:

- End-to-end encryption for sensor data transmission
- Secure API authentication (OAuth 2.0, JWT)
- Role-based access control for maintenance personnel
- Audit logging for all system access and alerts
- Regular security audits and penetration testing
- Compliance with industrial cybersecurity standards (IEC 62443)

## References

1. IEEE Standards for Industrial IoT Devices and Systems
2. ISO 13373-1: Condition Monitoring and Diagnostics
3. ISO 13379-1: Condition Monitoring and Diagnostics - Data Interpretation
4. MQTT Protocol Specification for Industrial IoT
5. Predictive Maintenance Best Practices in Manufacturing

## License

This project is provided for educational and research purposes.

## Contact and Support

For questions or support regarding this project, please refer to the internship report documentation.

---

**Project Developed**: July 2026
**Programming Language**: Python 3.11
**Last Updated**: July 13, 2026
