import csv
import os
from datetime import datetime

class GameDataCollector:
    def __init__(self, csv_file="training_data.csv"):
        # Get absolute path for the CSV file
        self.data_dir = 'training_data'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        # Use a single CSV file
        self.csv_file = os.path.join(self.data_dir, 'training_data.csv')
        
        self.headers = [
            'timer', 'player1_x', 'player1_y', 'player1_health', 'player1_prev_health',
            'player2_x', 'player2_y', 'player2_health', 'player2_prev_health',
            'distance', 'relative_x', 'relative_y',
            'current_command', 'prev_command', 'prev2_command', 'prev3_command',
            'damage_dealt', 'damage_taken', 'command_duration'
        ]
        
        # Initialize tracking variables
        self.prev_p1_health = 100
        self.prev_p2_health = 100
        self.prev_command = None
        self.prev2_command = None
        self.prev3_command = None
        self.command_start_time = None
        self.current_command = None
        
        # Create file with headers only if it doesn't exist
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()

    def collect_frame_data(self, game_state, current_command):
        """Collect data from a single frame of the game state"""
        # Only record if both players have health > 0
        if game_state.player1.health <= 0 or game_state.player2.health <= 0:
            return
            
        # Calculate distances and relative positions
        distance = ((game_state.player1.x_coord - game_state.player2.x_coord) ** 2 + 
                   (game_state.player1.y_coord - game_state.player2.y_coord) ** 2) ** 0.5
        relative_x = game_state.player2.x_coord - game_state.player1.x_coord
        relative_y = game_state.player2.y_coord - game_state.player1.y_coord
        
        # Calculate damage dealt and taken
        damage_dealt = self.prev_p2_health - game_state.player2.health
        damage_taken = self.prev_p1_health - game_state.player1.health
        
        # Calculate command duration
        command_duration = 0
        if self.command_start_time is not None:
            command_duration = game_state.timer - self.command_start_time
            
        # Update command history
        if current_command != self.current_command:
            self.prev3_command = self.prev2_command
            self.prev2_command = self.prev_command
            self.prev_command = self.current_command
            self.current_command = current_command
            self.command_start_time = game_state.timer
            
        # Prepare row data
        row = {
            'timer': game_state.timer,
            'player1_x': game_state.player1.x_coord,
            'player1_y': game_state.player1.y_coord,
            'player1_health': game_state.player1.health,
            'player1_prev_health': self.prev_p1_health,
            'player2_x': game_state.player2.x_coord,
            'player2_y': game_state.player2.y_coord,
            'player2_health': game_state.player2.health,
            'player2_prev_health': self.prev_p2_health,
            'distance': distance,
            'relative_x': relative_x,
            'relative_y': relative_y,
            'current_command': current_command,
            'prev_command': self.prev_command,
            'prev2_command': self.prev2_command,
            'prev3_command': self.prev3_command,
            'damage_dealt': damage_dealt,
            'damage_taken': damage_taken,
            'command_duration': command_duration
        }
        
        # Append to CSV
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(row)
            
        # Update previous health values
        self.prev_p1_health = game_state.player1.health
        self.prev_p2_health = game_state.player2.health 