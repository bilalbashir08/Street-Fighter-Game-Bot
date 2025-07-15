import socket
import json
from game_state import GameState
from bot import Bot
from data_collector import GameDataCollector
import sys
import os
import time

def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    print(f"Waiting for game connection on port {port}...")
    (client_socket, _) = server_socket.accept()
    print("Connected to game!")
    return client_socket

def send(client_socket, command):
    #This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    #receive the game state and return game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)
    return game_state

def main():
    # Initialize connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 9999))
    sock.listen(1)
    
    # Initialize bot and data collector
    bot = Bot()
    data_collector = GameDataCollector()
    
    # Wait for game connection
    print("Waiting for game connection on port 9999...")
    conn, addr = sock.accept()
    print("Connected to game!")
    
    # Start game loop
    print("Starting game loop...")
    print("Waiting for game state...")
    
    frame_count = 0
    last_size = 0
    
    while True:
        # Receive game state
        data = conn.recv(1024)
        if not data:
            break
            
        # Parse game state
        game_state = GameState(json.loads(data.decode()))
        
        # Get bot command
        if game_state.has_round_started and not game_state.is_round_over:
            # Get bot command for player 1
            command = bot.fight(game_state, "1")
            
            # Get current command for data collection
            current_command = bot._get_current_command()
            
            # Collect data
            data_collector.collect_frame_data(game_state, current_command)
            
            # Update frame count and print progress
            frame_count += 1
            if frame_count % 100 == 0:
                current_size = os.path.getsize(data_collector.csv_file)
                if current_size != last_size:
                    print(f"Collected data for frame {frame_count}")
                    print(f"CSV file size: {current_size} bytes")
                    last_size = current_size
        else:
            # Send neutral command when round hasn't started
            command = bot.fight(game_state, "1")  # This will return a neutral command
        
        # Always send a command
        conn.sendall(json.dumps(command.object_to_dict()).encode())
        
        # Small delay to prevent overwhelming the game
        time.sleep(0.01)
    
    # Clean up
    conn.close()
    sock.close()

if __name__ == '__main__':
   main()
