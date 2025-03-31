import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

# Simulation parameters
LANE_LENGTH = 60
NUM_CARS = 15


class Car:
    def __init__(self, position, velocity=0, color='R'):
        self.position = position
        self.velocity = velocity
        self.color = color

    def __repr__(self):
        return f"Car(pos={self.position}, vel={self.velocity}, color={self.color})"


def initialize_cars(lane_length=LANE_LENGTH, num_cars=NUM_CARS):
    positions = random.sample(range(lane_length), num_cars)
    cars = [Car(pos, velocity=0, color='R') for pos in positions]
    cars.sort(key=lambda car: car.position)
    return cars


def compute_gap(car, next_car, lane_length=LANE_LENGTH):
    if next_car.position > car.position:
        return next_car.position - car.position - 1
    else:
        return lane_length - car.position + next_car.position - 1


def update_cars(cars, lane_length=LANE_LENGTH):
    cars.sort(key=lambda car: car.position)
    num_cars = len(cars)
    new_states = []

    for i, car in enumerate(cars):
        next_car = cars[(i + 1) % num_cars]  # Circular lane
        gap = compute_gap(car, next_car, lane_length)
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
        car.position = (car.position + car.velocity) % lane_length

    return cars


# Color mapping
color_dict = {'R': (1, 0, 0), 'Y': (1, 1, 0), 'G': (0, 1, 0), '_': (1, 1, 1)}


def cars_to_lane(cars, lane_length=LANE_LENGTH):
    lane = ['_'] * lane_length
    for car in cars:
        lane[car.position] = car.color
    return lane


# Setup Matplotlib Figure
fig, ax = plt.subplots(figsize=(12, 3))
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(-0.5, LANE_LENGTH - 0.5)
ax.set_ylim(-0.5, 0.5)

# Initialize cars
cars = initialize_cars()
rects = []

# Draw initial lane
lane = cars_to_lane(cars)
for x in range(LANE_LENGTH):
    color = color_dict[lane[x]]
    rect = ax.add_patch(plt.Rectangle((x, 0), 1, 1, facecolor=color, edgecolor="black"))
    rects.append(rect)

# Animation Control
running = True


def animate(frame):
    global cars, running
    if not running:
        return

    # Update cars
    cars = update_cars(cars)
    lane = cars_to_lane(cars)

    # Update rectangle colors
    for x in range(LANE_LENGTH):
        rects[x].set_facecolor(color_dict[lane[x]])


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
