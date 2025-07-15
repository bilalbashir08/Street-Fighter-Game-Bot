import pandas as pd
import numpy as np
import random
from datetime import datetime

def generate_game_data(num_frames=1000, output_file='synthetic_game_data.csv'):
    # Initialize lists to store data
    data = []
    
    # Game state parameters
    screen_width = 400
    screen_height = 300
    max_health = 176
    min_health = 0
    timer = 99
    
    # Initialize player positions and states
    p1_x = random.randint(50, 150)
    p1_y = 192  # Ground level
    p2_x = random.randint(250, 350)
    p2_y = 192  # Ground level
    p1_health = max_health
    p2_health = max_health
    
    # Movement parameters
    move_speed = 5
    jump_height = 30
    jump_duration = 10
    
    # State tracking
    p1_is_jumping = False
    p1_jump_counter = 0
    p1_is_crouching = False
    p1_is_in_move = False
    p2_is_jumping = False
    p2_jump_counter = 0
    p2_is_crouching = False
    p2_is_in_move = False
    
    # Define move sequences from the bot
    move_sequences = {
        'approach_right': [">", "-", "!>", "v+>", "-", "!v+!>", "v", "-", "!v", "v+<", "-", "!v+!<", "<+Y", "-", "!<+!Y"],
        'approach_left': ["<", "-", "!<", "v+<", "-", "!v+!<", "v", "-", "!v", "v+>", "-", "!v+!>", ">+Y", "-", "!>+!Y"],
        'jump_attack_right': [">+^+B", ">+^+B", "!>+!^+!B"],
        'jump_attack_left': ["<+^+B", "<+^+B", "!<+!^+!B"],
        'close_combat': ["v+R", "v+R", "v+R", "!v+!R"],
        'back_off_right': [">", ">", "!>"],
        'back_off_left': ["<", "<", "!<"]
    }
    
    current_sequence = []
    sequence_index = 0
    sequence_delay = 0
    
    # Generate frames
    for frame in range(num_frames):
        # Calculate distance between players
        distance = abs(p1_x - p2_x)
        diff = p2_x - p1_x
        
        # Initialize button states
        buttons = {
            'p1_up': False,
            'p1_down': False,
            'p1_right': False,
            'p1_left': False,
            'p1_Y': False,
            'p1_B': False,
            'p1_X': False,
            'p1_A': False,
            'p1_L': False,
            'p1_R': False
        }
        
        # Select and execute move sequences based on distance
        if len(current_sequence) == 0:
            if diff > 60:
                toss = random.randint(0, 2)
                if toss == 0:
                    current_sequence = move_sequences['approach_right'].copy()
                elif toss == 1:
                    current_sequence = move_sequences['jump_attack_right'].copy()
                else:
                    current_sequence = move_sequences['approach_left'].copy()
            elif diff < -60:
                toss = random.randint(0, 2)
                if toss == 0:
                    current_sequence = move_sequences['approach_left'].copy()
                elif toss == 1:
                    current_sequence = move_sequences['jump_attack_left'].copy()
                else:
                    current_sequence = move_sequences['approach_right'].copy()
            else:
                toss = random.randint(0, 1)
                if toss == 1:
                    if diff > 0:
                        current_sequence = move_sequences['back_off_left'].copy()
                    else:
                        current_sequence = move_sequences['back_off_right'].copy()
                else:
                    current_sequence = move_sequences['close_combat'].copy()
        
        # Execute current move in sequence
        if len(current_sequence) > 0:
            current_move = current_sequence[0]
            
            # Parse and execute the move
            if "+" in current_move:
                parts = current_move.split("+")
                for part in parts:
                    if part == "v":
                        buttons['p1_down'] = True
                    elif part == "!v":
                        buttons['p1_down'] = False
                    elif part == "<":
                        buttons['p1_left'] = True
                    elif part == "!<":
                        buttons['p1_left'] = False
                    elif part == ">":
                        buttons['p1_right'] = True
                    elif part == "!>":
                        buttons['p1_right'] = False
                    elif part == "^":
                        buttons['p1_up'] = True
                    elif part == "!^":
                        buttons['p1_up'] = False
                    elif part == "Y":
                        buttons['p1_Y'] = True
                    elif part == "!Y":
                        buttons['p1_Y'] = False
                    elif part == "B":
                        buttons['p1_B'] = True
                    elif part == "!B":
                        buttons['p1_B'] = False
                    elif part == "R":
                        buttons['p1_R'] = True
                    elif part == "!R":
                        buttons['p1_R'] = False
            else:
                if current_move == "v":
                    buttons['p1_down'] = True
                elif current_move == "!v":
                    buttons['p1_down'] = False
                elif current_move == "<":
                    buttons['p1_left'] = True
                elif current_move == "!<":
                    buttons['p1_left'] = False
                elif current_move == ">":
                    buttons['p1_right'] = True
                elif current_move == "!>":
                    buttons['p1_right'] = False
                elif current_move == "^":
                    buttons['p1_up'] = True
                elif current_move == "!^":
                    buttons['p1_up'] = False
            
            # Update positions based on button presses
            if buttons['p1_right']:
                p1_x += move_speed
            if buttons['p1_left']:
                p1_x -= move_speed
            if buttons['p1_up']:
                p1_y -= jump_height / jump_duration
            if buttons['p1_down']:
                p1_y += jump_height / jump_duration
            
            # Remove the executed move
            current_sequence.pop(0)
        
        # Random opponent movement
        p2_x += random.randint(-3, 3)
        p2_x = max(50, min(screen_width - 50, p2_x))
        
        # Calculate movement speeds
        p1_speed = move_speed if buttons['p1_right'] or buttons['p1_left'] else 0
        p2_speed = abs(p2_x - (p2_x - random.randint(-3, 3)))
        
        # Create row data
        row = {
            'p1_id': 0,
            'p1_health': p1_health,
            'p1_x': p1_x,
            'p1_y': p1_y,
            'p1_is_jumping': buttons['p1_up'],
            'p1_is_crouching': buttons['p1_down'],
            'p1_is_in_move': buttons['p1_right'] or buttons['p1_left'],
            'p1_up': buttons['p1_up'],
            'p1_down': buttons['p1_down'],
            'p1_right': buttons['p1_right'],
            'p1_left': buttons['p1_left'],
            'p1_Y': buttons['p1_Y'],
            'p1_B': buttons['p1_B'],
            'p1_X': buttons['p1_X'],
            'p1_A': buttons['p1_A'],
            'p1_L': buttons['p1_L'],
            'p1_R': buttons['p1_R'],
            'p2_id': 7,
            'p2_health': p2_health,
            'p2_x': p2_x,
            'p2_y': p2_y,
            'distance_between_players': distance,
            'health_difference': p1_health - p2_health,
            'p1_winning': p1_health > p2_health,
            'p2_winning': p2_health > p1_health,
            'time_remaining': timer - (frame // 60),
            'p1_movement_speed': p1_speed,
            'p2_movement_speed': p2_speed
        }
        
        data.append(row)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Generated {num_frames} frames of game data and saved to {output_file}")

if __name__ == "__main__":
    generate_game_data() 