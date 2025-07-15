# Street-Fighter-Game-Bot
🎮 Game Bot with MLP
This project is a machine learning–based game bot that predicts player actions using a Multi-Layer Perceptron (MLP). It processes real-time game state data—like player position, velocity, and health—to generate in-game commands for a fighting game scenario (e.g., Street Fighter Turbo).

📂 Main Components
bot.py – Main controller integrating predictions and actions

ml_model.py – MLP model with training and prediction logic

game_state.py – Maintains the current state of the game

player.py – Handles player attributes like health and movement

command.py – Manages command generation logic

buttons.py – Tracks button press and release states

controller.py – High-level logic for bot control

data_collector.py – Captures gameplay data

generate_game_data.py – Creates synthetic data for training

analyze_data.py – Visualizes trends and statistics

.png files – Visual outputs (e.g., health over time, command durations)

✨ Features
Modular and easy-to-extend architecture
Each component (bot, model, game state, commands) is organized into separate files, making it easy to update or add new features without breaking the whole system.

MLP with configurable layers, adaptive learning rate, and early stopping
The machine learning model is a customizable Multi-Layer Perceptron. It supports tuning of layer sizes, uses an adaptive optimizer, and includes early stopping to prevent overfitting.

Real-time game state tracking and prediction
Tracks important variables like player health, position, and movement speed, and uses them to predict the next best action in real time.

Command system supports combos and history tracking
Generates complex button combinations based on the predicted action and maintains a command history to ensure smooth and intelligent gameplay.

Built-in tools for data collection and analysis
Includes scripts for generating synthetic gameplay data, analyzing model performance, and visualizing trends (e.g., command duration, health over time).



📬 Contact
Bilal Bashir
📧 bilalbashir584@gmail.com
