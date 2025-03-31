import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

# Simulation parameters
LANE_LENGTH = 60
NUM_CARS = 15
HISTORY_LENGTH = 30  # Number of past steps to keep


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


# Initialize cars
cars = initialize_cars()
history = [cars_to_lane(cars)] * HISTORY_LENGTH  # Start with identical history

# Setup Matplotlib Figure
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(-0.5, LANE_LENGTH - 0.5)
ax.set_ylim(-0.5, HISTORY_LENGTH - 0.5)

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
running = True


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

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=100, interval=500, repeat=False)

plt.show()
