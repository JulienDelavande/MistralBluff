import os
import re
import random
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = ROOT_DIR / 'data/1_raw_data'
CLEANED_DATA_DIR = ROOT_DIR / 'data/2_cleaned_data'
PREPARED_DATA_DIR = ROOT_DIR / 'data/3_prepared_data'

def separate_games(file_content):
    """Separate games from the file content. Games are separated by the string 'Game started'."""
    games = file_content.split('Game started')
    return ['Game started' + game for game in games if game.strip()]

def remove_game_started_at(game):
    """Remove the line that contains the game start time."""
    return re.sub(r'Game started at: .*', 'Game started', game)

def remove_muck(game):
    """Remove the lines that contain muck information."""
    game_lines = game.split('\n')
    return '\n'.join([line for line in game_lines if 'received a card' not in line])

def check_IlxxxlI_result(game):
    """Check if IlxxxlI won or lost the game."""
    for line in game.split('\n'):
        if line.startswith('Player IlxxxlI'):
            if 'Wins:' in line : # Si IlxxxlI n'a rien fait c'est Wins:0
                return 'win'
            elif 'Loses:' in line and float(line[:-1].split('Loses:')[1]) >= 0:
                return 'lose'
      

def remove_received_card_and_muck_lines(game):
    """Remove the lines that contain information about receiving a card and mucking."""
    game_lines = game.split('\n')
    return '\n'.join([line for line in game_lines if 'received a card' not in line and 'mucks' not in line and 'timed' not in line])

def remove_summary(game):
    """Remove the summary section of the game."""
    lines = game.split('\n')
    summary_start = None
    for i, line in enumerate(lines):
        if line.strip() == '------ Summary ------':
            summary_start = i
            break
    
    if summary_start is not None:
        return '\n'.join(lines[:summary_start])

def process_file(input_file, output_file):
    """Process a file, remove unnecessary information, and write the result to another file."""
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        file_content = infile.read()
        games = separate_games(file_content)
        
        for game in games:
            game = remove_game_started_at(game)
            game = remove_received_card_and_muck_lines(game)
            
            result = check_IlxxxlI_result(game)
            
            if result == 'win' or (result == 'lose' and random.random() < 0.5):
                game = remove_summary(game)
                outfile.write(game + '\n\n')
            

def process_directory(input_dir, output_dir):
    """Process all files in a directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            process_file(input_path, output_path)
            print(f"Processed {filename}")


if __name__ == '__main__':
    input_directory = RAW_DATA_DIR
    output_directory = CLEANED_DATA_DIR
    process_directory(input_directory, output_directory)
    