import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def load_data():
    """Load the training data from CSV"""
    data_path = Path('training_data/training_data.csv')
    if not data_path.exists():
        raise FileNotFoundError("Training data file not found. Please run the bot first to collect data.")
    
    df = pd.read_csv(data_path)
    print(f"\nLoaded {len(df)} rows of training data")
    return df

def analyze_basic_stats(df):
    """Analyze basic statistics of the data"""
    print("\n=== Basic Statistics ===")
    print("\nNumerical Columns Statistics:")
    print(df.describe())
    
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    print("\nUnique Commands:")
    print(df['current_command'].value_counts())

def analyze_health_patterns(df):
    """Analyze health patterns and damage"""
    print("\n=== Health Analysis ===")
    
    # Calculate average damage per command
    damage_by_command = df.groupby('current_command').agg({
        'damage_dealt': 'mean',
        'damage_taken': 'mean'
    }).round(2)
    
    print("\nAverage Damage by Command:")
    print(damage_by_command)
    
    # Plot health over time
    plt.figure(figsize=(12, 6))
    plt.plot(df['timer'], df['player1_health'], label='Player 1 Health')
    plt.plot(df['timer'], df['player2_health'], label='Player 2 Health')
    plt.title('Health Over Time')
    plt.xlabel('Timer')
    plt.ylabel('Health')
    plt.legend()
    plt.savefig('health_over_time.png')
    plt.close()

def analyze_movement_patterns(df):
    """Analyze movement patterns"""
    print("\n=== Movement Analysis ===")
    
    # Calculate average distance by command
    distance_by_command = df.groupby('current_command')['distance'].mean().round(2)
    print("\nAverage Distance by Command:")
    print(distance_by_command)
    
    # Plot distance distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='distance', bins=30)
    plt.title('Distribution of Distance Between Players')
    plt.xlabel('Distance')
    plt.ylabel('Count')
    plt.savefig('distance_distribution.png')
    plt.close()

def analyze_command_patterns(df):
    """Analyze command patterns and sequences"""
    print("\n=== Command Pattern Analysis ===")
    
    # Analyze command sequences
    command_sequences = df[['prev3_command', 'prev2_command', 'prev_command', 'current_command']]
    
    # Most common command sequences
    print("\nMost Common Command Sequences:")
    sequence_counts = command_sequences.value_counts().head(10)
    print(sequence_counts)
    
    # Command transition matrix
    transitions = pd.crosstab(df['prev_command'], df['current_command'])
    print("\nCommand Transition Matrix:")
    print(transitions)

def analyze_command_duration(df):
    """Analyze command duration patterns"""
    print("\n=== Command Duration Analysis ===")
    
    # Average duration by command
    duration_by_command = df.groupby('current_command')['command_duration'].mean().round(2)
    print("\nAverage Duration by Command:")
    print(duration_by_command)
    
    # Plot command duration distribution
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='current_command', y='command_duration')
    plt.title('Command Duration Distribution')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('command_duration.png')
    plt.close()

def main():
    # Load data
    df = load_data()
    
    # Perform analysis
    analyze_basic_stats(df)
    analyze_health_patterns(df)
    analyze_movement_patterns(df)
    analyze_command_patterns(df)
    analyze_command_duration(df)
    
    print("\nAnalysis complete! Check the generated plots for visualizations.")
    print("Generated plots:")
    print("- health_over_time.png")
    print("- distance_distribution.png")
    print("- command_duration.png")

if __name__ == "__main__":
    main() 