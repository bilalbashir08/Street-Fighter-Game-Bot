import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import joblib
import os
from tqdm import tqdm
import time

class GameMLP:
    def __init__(self):
        self.model = MLPClassifier(
            hidden_layer_sizes=(128, 64, 32),  # Deeper network
            activation='relu',
            solver='adam',
            learning_rate='adaptive',
            max_iter=1000,  # More training iterations
            batch_size='auto',
            early_stopping=True,
            validation_fraction=0.2,  # More validation data
            n_iter_no_change=20,  # More patience
            random_state=42,
            verbose=True
        )
        self.scaler = StandardScaler()
        self.command_mapping = None
        self.is_trained = False
        
    def prepare_features(self, game_state, prev_commands):
        """Prepare features for the model"""
        features = [
            game_state.player1.x_coord,
            game_state.player1.y_coord,
            game_state.player1.health,
            game_state.player2.x_coord,
            game_state.player2.y_coord,
            game_state.player2.health,
            game_state.timer,
            # Relative positions
            game_state.player2.x_coord - game_state.player1.x_coord,  # relative_x
            game_state.player2.y_coord - game_state.player1.y_coord,  # relative_y
            # Distance
            ((game_state.player1.x_coord - game_state.player2.x_coord) ** 2 + 
             (game_state.player1.y_coord - game_state.player2.y_coord) ** 2) ** 0.5,
            # Velocity (if available)
            game_state.player1.x_velocity if hasattr(game_state.player1, 'x_velocity') else 0,
            game_state.player1.y_velocity if hasattr(game_state.player1, 'y_velocity') else 0,
            game_state.player2.x_velocity if hasattr(game_state.player2, 'x_velocity') else 0,
            game_state.player2.y_velocity if hasattr(game_state.player2, 'y_velocity') else 0,
        ]
        
        # Add previous commands as one-hot encoded features
        for cmd in prev_commands:
            if cmd in self.command_mapping:
                cmd_idx = self.command_mapping[cmd]
                cmd_features = [0] * len(self.command_mapping)
                cmd_features[cmd_idx] = 1
                features.extend(cmd_features)
            else:
                features.extend([0] * len(self.command_mapping))
                
        return np.array(features).reshape(1, -1)
    
    def train(self, csv_file='training_data/training_data.csv'):
        """Train the model on collected data"""
        if not os.path.exists(csv_file):
            print("No training data found!")
            return False
            
        print("Loading training data...")
        df = pd.read_csv(csv_file)
        
        print("Preparing command mapping...")
        # Get all unique commands from training data
        all_commands = set(df['current_command'].unique())
        self.command_mapping = {cmd: idx for idx, cmd in enumerate(sorted(all_commands))}
        
        print(f"Found {len(self.command_mapping)} unique commands")
        print("Available commands:", list(self.command_mapping.keys()))
        
        print("Preparing features and labels...")
        X = []
        y = []
        
        # Use tqdm for progress bar
        for i in tqdm(range(len(df)), desc="Processing training data"):
            features = [
                df.iloc[i]['player1_x'],
                df.iloc[i]['player1_y'],
                df.iloc[i]['player1_health'],
                df.iloc[i]['player2_x'],
                df.iloc[i]['player2_y'],
                df.iloc[i]['player2_health'],
                df.iloc[i]['timer'],
                df.iloc[i]['relative_x'],
                df.iloc[i]['relative_y'],
                df.iloc[i]['distance']
            ]
            
            # Add velocity features if available
            if 'player1_x_velocity' in df.columns:
                features.extend([
                    df.iloc[i]['player1_x_velocity'],
                    df.iloc[i]['player1_y_velocity'],
                    df.iloc[i]['player2_x_velocity'],
                    df.iloc[i]['player2_y_velocity']
                ])
            else:
                features.extend([0, 0, 0, 0])
            
            # Add previous commands
            prev_commands = [
                df.iloc[i]['prev_command'],
                df.iloc[i]['prev2_command'],
                df.iloc[i]['prev3_command']
            ]
            
            for cmd in prev_commands:
                if cmd in self.command_mapping:
                    cmd_idx = self.command_mapping[cmd]
                    cmd_features = [0] * len(self.command_mapping)
                    cmd_features[cmd_idx] = 1
                    features.extend(cmd_features)
                else:
                    features.extend([0] * len(self.command_mapping))
            
            X.append(features)
            y.append(self.command_mapping[df.iloc[i]['current_command']])
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"Training data shape: {X.shape}")
        print("Scaling features...")
        X = self.scaler.fit_transform(X)
        
        print("\nStarting model training...")
        print("Training progress will be shown below:")
        print("-" * 50)
        
        start_time = time.time()
        self.model.fit(X, y)
        training_time = time.time() - start_time
        
        print("-" * 50)
        print(f"Training completed in {training_time:.2f} seconds")
        self.is_trained = True
        
        print("Saving model and related files...")
        joblib.dump(self.model, 'game_model.joblib')
        joblib.dump(self.scaler, 'game_scaler.joblib')
        joblib.dump(self.command_mapping, 'command_mapping.joblib')
        
        print("Training completed successfully!")
        return True
    
    def predict(self, game_state, prev_commands):
        """Predict next command based on game state and previous commands"""
        # Prepare features
        features = self.prepare_features(game_state, prev_commands)
        features = self.scaler.transform(features)
        
        # Get predictions
        probabilities = self.model.predict_proba(features)[0]
        
        # Create reverse mapping for easier lookup
        reverse_mapping = {v: k for k, v in self.command_mapping.items()}
        
        print("\n=== Model Prediction Debug ===")
        print(f"Distance to opponent: {abs(game_state.player2.x_coord - game_state.player1.x_coord)}")
        print(f"Relative position: {'right' if game_state.player2.x_coord > game_state.player1.x_coord else 'left'}")
        
        print("\nInitial probabilities:")
        for i, prob in enumerate(probabilities):
            if prob > 0.01:  # Only show significant probabilities
                print(f"{reverse_mapping[i]}: {prob:.4f}")
        
        # Get the most likely command
        predicted_idx = np.argmax(probabilities)
        predicted_cmd = reverse_mapping[predicted_idx]
        
        print(f"\nPredicted command: {predicted_cmd}")
        print("=" * 30)
        
        # Fallback to neutral if prediction is invalid
        if predicted_cmd not in self.command_mapping:
            print(f"Warning: Invalid command predicted: {predicted_cmd}")
            return "neutral"
        
        return predicted_cmd
    
    def load_model(self):
        """Load a trained model"""
        self.model = joblib.load('game_model.joblib')
        self.scaler = joblib.load('game_scaler.joblib')
        self.command_mapping = joblib.load('command_mapping.joblib')
        self.is_trained = True
        return True

if __name__ == "__main__":
    print("Starting ML model training...")
    model = GameMLP()
    if model.train():
        print("Model trained and saved successfully!")
    else:
        print("Failed to train model. Please ensure training data exists in training_data/training_data.csv") 