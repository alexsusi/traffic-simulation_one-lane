import random
import time

def initialize_lane(length=60, num_cars=15):
    lane = ['_'] * length
    positions = random.sample(range(length), num_cars)
    for pos in positions:
        lane[pos] = 'R'  # Red cars (stopped)
    return lane

def print_lane(lane):
    print(''.join(lane))

def update_lane(lane):
    length = len(lane)
    new_lane = lane[:]
    car_positions = [i for i, c in enumerate(lane) if c in {'R', 'Y', 'G'}]
    
    for pos in car_positions:
        car = lane[pos]
        next_pos = (pos + 1) % length
        next2_pos = (pos + 2) % length
        next4_pos = (pos + 4) % length

        if car == 'R' and lane[next_pos] == '_' and lane[next2_pos] == '_':
            new_lane[pos] = '_'
            new_lane[next_pos] = 'Y'  # Becomes yellow
        elif car == 'Y' and lane[next_pos] == '_' and lane[next2_pos] == '_' and lane[next4_pos] == '_':
            new_lane[pos] = '_'
            new_lane[next2_pos] = 'G'  # Becomes green (fast)
        elif car == 'G':
            if lane[next_pos] != '_' and lane[next2_pos] == '_':
                new_lane[pos] = '_'
                new_lane[next_pos] = 'Y'  # Brakes to yellow
            elif lane[next_pos] != '_':
                new_lane[pos] = 'R'  # Brakes to red
        elif car == 'Y' and lane[next_pos] != '_':
            new_lane[pos] = 'R'  # Brakes to red
    
    return new_lane

def simulate(steps=20, delay=0.5):
    lane = initialize_lane()
    for _ in range(steps):
        print_lane(lane)
        lane = update_lane(lane)
        time.sleep(delay)
        print("\n")

# Run the simulation
simulate()
