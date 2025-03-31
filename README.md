# Traffic Simulation Programs

This repository contains two Python programs that simulate traffic flow using simple rules. Both programs represent a single-lane road where cars move based on predefined traffic rules.

## Files Overview

### 1. `traffic_sim.py`
This program provides a graphical simulation of traffic movement using Matplotlib. Cars are represented in three states:
- **Red (R)**: Stopped
- **Yellow (Y)**: Slow-moving
- **Green (G)**: Fast-moving

#### Features:
- **Animated Visualization**: The simulation runs in a Matplotlib window, showing traffic evolution over time.
- **Color-Coded Cars**: Cars change color based on speed and proximity to the next car.
- **Play/Pause Button**: Users can control the simulation with a button.
- **Circular Lane**: Cars move in a loop, simulating a closed circuit.

#### Dependencies:
- `numpy`
- `matplotlib`

#### How to Run:
```bash
python traffic_sim.py
```

### 2. `traffic_sim_simple-print.py`
This is a simpler, text-based version of the traffic simulation.

#### Features:
- **Console Output**: The traffic state is printed to the terminal at each step.
- **Simplified Rules**: Cars move forward based on predefined conditions and change colors accordingly.
- **Configurable Steps**: The simulation runs for a set number of steps with a delay between updates.

#### Dependencies:
- Standard Python libraries (`random`, `time`)

#### How to Run:
```bash
python traffic_sim_simple-print.py
```

## Traffic Rules
Both programs follow these basic traffic rules:
1. Red cars (R) move to Yellow (Y) if there is enough space ahead.
2. Yellow cars (Y) move to Green (G) if there is even more space.
3. Green cars (G) continue moving but slow down if obstacles appear.
4. If a car encounters another car directly in front, it stops and turns Red (R).

## License
This project is released under the MIT License.

## Author
Alex Susi
