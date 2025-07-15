from command import Command
import numpy as np
from buttons import Buttons
# from data_collector import GameDataCollector
from ml_model import GameMLP
import csv
import os
from datetime import datetime

class Bot:

    def __init__(self):
        # Initialize ML model
        self.ml_model = GameMLP()
        if not self.ml_model.load_model():
            # Train the model if no trained model exists
            print("No trained model found. Training new model...")
            if not self.ml_model.train():
                raise Exception("Failed to train ML model. Please ensure training data exists.")
            print("Model trained successfully.")
        
        # Initialize data collector
        # self.data_collector = GameDataCollector()
        
        # Initialize command tracking
        self.prev_command = None
        self.prev2_command = None
        self.prev3_command = None
        self.current_command = None
        
        # Initialize buttons
        self.my_command = Command()
        self.buttn = Buttons()
        self.remaining_code = []

    def fight(self, current_game_state, player):
        if player == "1":
            # Always use ML predictions
            prev_commands = [self.prev_command, self.prev2_command, self.prev3_command]
            predicted_command = self.ml_model.predict(current_game_state, prev_commands)
            self.run_command([predicted_command], current_game_state.player1)
            
            # Update command history
            self.prev3_command = self.prev2_command
            self.prev2_command = self.prev_command
            self.prev_command = self.current_command
            self.current_command = self._get_current_command()
            
            # Save game state data
            # self.data_collector.collect_frame_data(current_game_state, self.current_command)
            
            self.my_command.player_buttons = self.buttn
            
        return self.my_command

    def _get_current_command(self):
        """Helper method to get the current command as a string"""
        if not self.remaining_code:
            return "neutral"
        return self.remaining_code[0]

    def run_command(self, com, player):
        if len(self.remaining_code) == 0:
            self.remaining_code = com.copy()
            
        if len(self.remaining_code) > 0:
            cmd = self.remaining_code[0]
            
            # First release all buttons
            self._release_button("v")
            self._release_button("<")
            self._release_button(">")
            self._release_button("^")
            self._release_button("A")
            self._release_button("B")
            self._release_button("Y")
            self._release_button("R")
            self._release_button("L")
            
            # Then handle the new command
            if "+" in cmd:
                buttons = cmd.split("+")
                for btn in buttons:
                    if btn.startswith("!"):
                        self._release_button(btn[1:])
                    else:
                        self._press_button(btn)
            else:
                if cmd.startswith("!"):
                    self._release_button(cmd[1:])
                else:
                    self._press_button(cmd)
                    
            self.remaining_code = self.remaining_code[1:]
            
    def _press_button(self, btn):
        if btn == "v":
            self.buttn.down = True
        elif btn == "<":
            self.buttn.left = True
        elif btn == ">":
            self.buttn.right = True
        elif btn == "^":
            self.buttn.up = True
        elif btn == "A":
            self.buttn.A = True
        elif btn == "B":
            self.buttn.B = True
        elif btn == "Y":
            self.buttn.Y = True
        elif btn == "R":
            self.buttn.R = True
        elif btn == "L":
            self.buttn.L = True
            
    def _release_button(self, btn):
        if btn == "v":
            self.buttn.down = False
        elif btn == "<":
            self.buttn.left = False
        elif btn == ">":
            self.buttn.right = False
        elif btn == "^":
            self.buttn.up = False
        elif btn == "A":
            self.buttn.A = False
        elif btn == "B":
            self.buttn.B = False
        elif btn == "Y":
            self.buttn.Y = False
        elif btn == "R":
            self.buttn.R = False
        elif btn == "L":
            self.buttn.L = False
