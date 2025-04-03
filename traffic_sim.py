import random
import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

# Simulation parameters
LANE_LENGTH = 60
NUM_CARS = 15
HISTORY_LENGTH = 30  # Number of past steps to keep
DAY_DREAM_PROB = 0.1  # Probability of a car daydreaming (not moving)


class Car:
    def __init__(self, position, velocity=0, color='R'):
        self.position = position
        self.velocity = velocity
        self.color = color


def initialize_cars():
    positions = random.sample(range(LANE_LENGTH), NUM_CARS)
    return [Car(pos, velocity=0, color='R') for pos in sorted(positions)]


def compute_gap(car, next_car):
    return (next_car.position - car.position - 1) % LANE_LENGTH


def update_cars(cars):
    cars.sort(key=lambda car: car.position)
    new_states = []

    for i, car in enumerate(cars):
        next_car = cars[(i + 1) % len(cars)]  # Circular lane
        gap = compute_gap(car, next_car)
        new_velocity, new_color = car.velocity, car.color

        # Update rules
        if car.color == 'R' and gap >= 2:
            new_velocity, new_color = 1, 'Y'
        elif car.color == 'Y' and gap >= 4:
            new_velocity, new_color = 2, 'G'
        elif car.color == 'G':
            if gap == 0:
                new_velocity, new_color = 0, 'R'
            elif gap < 2:
                new_velocity, new_color = 1, 'Y'
        elif car.color == 'Y' and gap == 0:
            new_velocity, new_color = 0, 'R'

        # Apply day-dream-prob (random chance to reduce speed)
        if random.random() < DAY_DREAM_PROB:
            if new_velocity == 2:
                new_velocity, new_color = 1, 'Y'
            elif new_velocity == 1:
                new_velocity, new_color = 0, 'R'

        # Ensure no crash after daydreaming
        if new_velocity > 0:
            predicted_position = (car.position + new_velocity) % LANE_LENGTH
            if predicted_position == next_car.position:
                new_velocity, new_color = 0, 'R'  # Stop to avoid collision

        new_states.append((new_velocity, new_color))

    # Apply new states and move cars
    for i, car in enumerate(cars):
        car.velocity, car.color = new_states[i]
        car.position = (car.position + car.velocity) % LANE_LENGTH

    return cars


# Color mapping
color_dict = {'R': (1, 0, 0), 'Y': (1, 1, 0), 'G': (0, 1, 0), '_': (1, 1, 1)}


def cars_to_lane(cars):
    lane = ['_'] * LANE_LENGTH
    for car in cars:
        lane[car.position] = car.color
    return lane


# Function to show a pop-up window for user input
def show_setup_popup():
    global NUM_CARS, DAY_DREAM_PROB

    # Create a pop-up window
    popup = tk.Tk()
    popup.title("Setup Simulation")

    # Labels and input fields
    tk.Label(popup, text="Car Density (1-60):").grid(row=0, column=0, padx=10, pady=5)
    car_density_entry = tk.Entry(popup)
    car_density_entry.insert(0, str(NUM_CARS))  # Default value
    car_density_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(popup, text="Daydream Probability (0-1):").grid(row=1, column=0, padx=10, pady=5)
    daydream_prob_entry = tk.Entry(popup)
    daydream_prob_entry.insert(0, str(DAY_DREAM_PROB))  # Default value
    daydream_prob_entry.grid(row=1, column=1, padx=10, pady=5)

    # Submit button
    def submit():
        nonlocal car_density_entry, daydream_prob_entry
        try:
            # Get user input
            NUM_CARS = int(car_density_entry.get())
            DAY_DREAM_PROB = float(daydream_prob_entry.get())

            # Validate input
            if NUM_CARS < 1 or NUM_CARS > LANE_LENGTH:
                print("Error: Car density must be between 1 and", LANE_LENGTH)
                return
            if DAY_DREAM_PROB < 0 or DAY_DREAM_PROB > 1:
                print("Error: Daydream probability must be between 0 and 1")
                return

            # Close the pop-up window
            popup.destroy()

            # Reinitialize cars and history
            setup_simulation()
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    tk.Button(popup, text="Submit", command=submit).grid(row=2, column=0, columnspan=2, pady=10)

    # Run the pop-up window
    popup.mainloop()


# Function to reinitialize the simulation
def setup_simulation():
    global cars, history

    # Reinitialize cars and history
    cars = initialize_cars()
    history = [['_'] * LANE_LENGTH for _ in range(HISTORY_LENGTH - 1)] + [cars_to_lane(cars)]

    # Update the plot to reflect the new setup
    for y in range(HISTORY_LENGTH):
        for x in range(LANE_LENGTH):
            rects[y][x].set_facecolor(color_dict[history[y][x]])


# Initialize cars
cars = initialize_cars()
history = [['_'] * LANE_LENGTH for _ in range(HISTORY_LENGTH - 1)] + [cars_to_lane(cars)]

# Setup Matplotlib Figure
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(-0.5, LANE_LENGTH + 0.5)
ax.set_ylim(-0.5, HISTORY_LENGTH + 0.5)

# Draw history rectangles
rects = []
for y in range(HISTORY_LENGTH):
    row = []
    for x in range(LANE_LENGTH):
        color = color_dict[history[y][x]]
        rect = ax.add_patch(plt.Rectangle((x, y), 1, 1, facecolor=color, edgecolor="black"))
        row.append(rect)
    rects.append(row)

# Animation Control
running = False


def animate(frame):
    global cars, history, running
    if not running:
        return

    # Update cars
    cars = update_cars(cars)
    new_lane = cars_to_lane(cars)

    # Update history (scroll up)
    history.append(new_lane)  # Newest step at the bottom
    history.pop(0)  # Remove oldest step at the top

    # Update rectangle colors
    for y in range(HISTORY_LENGTH):
        for x in range(LANE_LENGTH):
            rects[y][x].set_facecolor(color_dict[history[y][x]])


# Play/Pause Buttons
def toggle_animation(event):
    global running
    running = not running


ax_play = plt.axes([0.8, 0.02, 0.1, 0.05])
btn_play = Button(ax_play, "Play/Pause")
btn_play.on_clicked(toggle_animation)

# Add a "Setup" button to trigger the pop-up
ax_setup = plt.axes([0.65, 0.02, 0.1, 0.05])
btn_setup = Button(ax_setup, "Setup")
btn_setup.on_clicked(lambda event: show_setup_popup())

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=100, interval=500, repeat=False)

plt.show()
