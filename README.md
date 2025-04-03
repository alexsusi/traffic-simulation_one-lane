# Traffic Simulation Programs

This repository contains two Python programs that simulate traffic flow using simple rules. Both programs represent a single-lane road where cars move based on predefined traffic rules.

1. is a one-lane road where cars autonomously accelerate, decelerate, or "daydream" based on traffic rules, visualized as a grid with interactive controls for car density and behavior.
2. is a simplified version where cars accelerate and adapt to traffic in front.

## 1. traffic_sim.py

This project implements a simple traffic simulation model using Python. The simulation represents a one-lane road where cars move from left to right, following specific rules for acceleration, deceleration, and random "daydreaming" behavior. The simulation is visualized using `matplotlib`.

### Features

- **One-Lane Traffic Simulation**: Cars move in a circular one-lane road of fixed length (`LANE_LENGTH`).
- **Car Behavior**:
  - Cars have three states: stopped (red), slow (yellow), and fast (green).
  - Cars accelerate or decelerate based on the gap to the next car.
  - Cars may randomly "daydream" and reduce their speed based on a probability (`DAY_DREAM_PROB`).
- **Visualization**:
  - The simulation is displayed as a grid where the bottom row represents the current state of the cars.
  - The rows above show the history of the simulation over time.
- **Interactive Controls**:
  - A **Setup** button allows users to configure the car density (`NUM_CARS`) and daydream probability (`DAY_DREAM_PROB`) via a pop-up window.
  - A **Play/Pause** button starts or pauses the simulation.

### How to Use

1. **Run the Program**:
   - Execute the script using Python. Ensure you have the required dependencies installed (see below).

2. **Setup Simulation**:
   - Click the **Setup** button to open a pop-up window.
   - Enter the desired car density (number of cars) and daydream probability (a value between 0 and 1).
   - Click **Submit** to apply the changes and reinitialize the simulation.

3. **Start/Pause Simulation**:
   - Click the **Play/Pause** button to start or pause the simulation.

4. **Visualization**:
   - The bottom row of the grid shows the current state of the cars.
   - The rows above show the history of the simulation over time.

### Simulation Parameters

- `LANE_LENGTH`: The length of the one-lane road (default: 60).
- `NUM_CARS`: The number of cars on the road (default: 15).
- `HISTORY_LENGTH`: The number of past time steps displayed in the visualization (default: 30).
- `DAY_DREAM_PROB`: The probability of a car randomly reducing its speed (default: 0.1).

### Dependencies

The following Python libraries are required to run the simulation:

- `matplotlib`
- `tkinter` (built into Python)

## 2. Simplification `traffic_sim_simple-print.py`

This is a simpler, text-based version of the traffic simulation.

#### Features

- **Console Output**: The traffic state is printed to the terminal at each step.
- **Simplified Rules**: Cars move forward based on predefined conditions and change colors accordingly.
- **Configurable Steps**: The simulation runs for a set number of steps with a delay between updates.

#### Dependencies

- Standard Python libraries (`random`, `time`)

#### How to Run

```bash
python traffic_sim_simple-print.py
```

## Traffic Rules

Both programs follow these basic traffic rules:

1. Red cars (R) move to Yellow (Y) if there is enough space ahead.
2. Yellow cars (Y) move to Green (G) if there is even more space.
3. Green cars (G) continue moving but slow down if obstacles appear.
4. If a car encounters another car directly in front, it stops and turns Red (R).

![image](https://github.com/user-attachments/assets/d7a4954b-9d76-4ab8-bd13-0585390b7750)

## License

This project is released under the MIT License.

## Author

Alex Susi
